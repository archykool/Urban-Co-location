import pandas as pd
import google.generativeai as genai
import json
import os
import time
from tqdm import tqdm

# --- CONFIGURATION ---
# TODO: Place your Gemini API Key here.
API_KEY = 'AIzaSyD80B-6tnomLoYgCUQ9kmKE6pVUyI0_TFY'
MODEL_NAME = 'gemini-2.0-flash'

# --- 输入和输出文件路径 ---
AGENT_PROFILE_CSV = 'lunch_agent_profile_1004.csv'
POI_CATEGORY_CSV = 'lunch_poi_1004.csv'
OUTPUT_JSON_PATH = 'generated_lunch_personas_1004.json'

# 每个Cluster需要生成的Agent数量
CLUSTER_COUNTS = {
    0: 83,
    1: 33,
    2: 40,
    3: 23,
    4: 9
}

# --- 2. 初始化Gemini模型 ---
try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
    print(f"Successfully initialized Gemini model '{MODEL_NAME}'.")
except Exception as e:
    print(f"Error initializing model. Check API Key and model name. Details: {e}")
    exit()


def load_and_prepare_data():
    """
    加载agent_profile.csv和宽格式的poi_main_category.csv，
    正确处理它们，并合并成每个cluster的综合档案。
    """
    try:
        agent_profile_df = pd.read_csv(AGENT_PROFILE_CSV)
        poi_category_df_wide = pd.read_csv(POI_CATEGORY_CSV)

        # 使用pandas.melt()将宽格式POI数据转换为长格式
        poi_category_df_long = poi_category_df_wide.melt(
            id_vars=['cluster'],
            var_name='main_category',
            value_name='weight'
        )

        # 按cluster对POI类别进行分组，并聚合成一个排序后的列表
        poi_grouped = poi_category_df_long.groupby('cluster').apply(
            lambda x: x.sort_values('weight', ascending=False).to_dict('records')
        ).rename('poi_category_preferences')

        # 合并POI类别数据和agent档案数据
        cluster_profiles_df = pd.merge(agent_profile_df, poi_grouped, on='cluster')

        print("Successfully loaded and processed agent profile and POI category files.")
        return cluster_profiles_df.set_index('cluster')
    except FileNotFoundError as e:
        print(f"Error: File not found: {e.filename}. Please ensure CSV files are in the same directory.")
        return None
    except KeyError as e:
        print(f"---")
        print(f"KeyError: Could not find the column {e} in your CSV file.")
        print(f"Please check the column headers in the script and your CSV files to ensure they match.")
        print(f"---")
        return None


def create_persona_prompt(cluster_profile):
    """
    生成一个高度定制化的prompt，专注于午餐时间的决策行为。
    """
    # 从提供的列中动态计算本科及以上学历的比例
    bachelor_or_higher_pct = (
        cluster_profile.get('bachelors_degree_share_mean', 0) +
        cluster_profile.get('masters_degree_share_mean', 0) +
        cluster_profile.get('professional_school_degree_share_mean', 0) +
        cluster_profile.get('doctorate_degree_share_mean', 0)
    )

    # 为prompt格式化POI偏好列表
    top_poi_categories = [
        {"category": item['main_category'], "preference": item['weight']}
        for item in cluster_profile['poi_category_preferences'][:10]
    ]

    prompt = f"""
    You are a behavioral analyst and persona generator specializing in urban mobility during **lunch hours**.
    Your task is to create a detailed persona for a single individual, focusing specifically on the factors that influence their **lunchtime decisions**.

    **SIMULATION CONTEXT:**
    - **Time of Day:** Weekday lunchtime.
    - **Location:** The agent is currently at or near the NYU Tandon campus in Downtown Brooklyn.
    - **Primary Goal:** The agent needs to find and eat lunch.

    **STATISTICAL CLUSTER PROFILE (Data for the agent's neighborhood):**
    - Median Household Income: ${cluster_profile['median_household_income_median']:,.0f} (Std Dev: ${cluster_profile['median_household_income_std']:,.0f})
    - Median Unemployment Rate: {cluster_profile['unemployment_rate_median'] * 100:.2f}%
    - Education (Bachelor's or Higher, Mean %): {bachelor_or_higher_pct * 100:.1f}%
    - **Lunch-related POI Preferences (Ranked Categories):**
      {json.dumps(top_poi_categories, indent=2)}

    **YOUR TASK:**
    Create a persona for **ONE single, unique individual**. Your response MUST be a single, valid JSON object with NO additional text or markdown.

    **INSTRUCTIONS:**
    1.  **Demographics**: Generate a specific `age`, `estimated_income`, `education_level`, and `employment_status` consistent with the cluster's statistics.
    2.  **Personality Modeling**: Create a `personality_summary` (2-3 sentences) describing the agent's core psychological traits and connect them to their likely food preferences (e.g., adventurous eater vs. prefers routine, budget-conscious vs. quality-focused).
    3.  **Lunch Decision Narrative**: Write a detailed `lunch_decision_narrative` (4-6 sentences). This narrative MUST describe the agent's typical thought process when deciding on lunch. What factors (cost, speed, health, social opportunity, variety) do they weigh most heavily based on their income, job, and personality? Do they prefer a quick bite from a "Limited-Service Restaurant" or a sit-down meal at a "Full-Service Restaurant"?
    4.  **STRICT RULE**: In the narrative, you MUST use ONLY generic category names. **Under no circumstances should you invent or use a real brand name, store name, street name, or other specific place name.**

    **REQUIRED JSON OUTPUT EXAMPLE:**
    {{
      "age": 28,
      "estimated_income": 85000,
      "education_level": "Bachelor's Degree",
      "employment_status": "Employed Full-time",
      "personality_summary": "A highly ambitious and time-conscious individual. They are extroverted but prioritize efficiency in their daily routine. Their food choices are driven by health and speed over cost.",
      "lunch_decision_narrative": "As a consultant with back-to-back meetings, their lunch break is short and precious, rarely more than 30 minutes. They almost never pack a lunch, preferring to buy something quick. Cost is less of a concern than time and nutritional value; they need fuel to stay sharp. They typically opt for a healthy option from a 'Limited-Service Restaurant' where they can customize their order. If they have a rare lunch meeting with a client, they'll choose a reputable 'Full-Service Restaurant' that is known for quick service. They might grab a cold brew from a 'Snack and Nonalcoholic Beverage Bar' on the way back to the office."
    }}
    """
    return prompt

def generate_agent_persona(cluster_profile):
    """
    Calls the Gemini API to generate a single agent persona.
    """
    prompt = create_persona_prompt(cluster_profile)
    for attempt in range(3):
        try:
            response = model.generate_content(prompt)
            cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"\n  - API call or JSON parsing failed on attempt {attempt + 1}. Error: {e}")
            if attempt < 2:
                time.sleep(1.5)
    return None


def main():
    """
    Main execution function to orchestrate the persona generation process.
    """
    cluster_profiles = load_and_prepare_data()
    if cluster_profiles is None:
        return

    all_personas = []
    total_agents_to_generate = sum(CLUSTER_COUNTS.values())

    print(f"\nStarting generation of {total_agents_to_generate} LUNCH-FOCUSED agent personas...")

    with tqdm(total=total_agents_to_generate, desc="Overall Progress") as pbar:
        for cluster_id, count in CLUSTER_COUNTS.items():
            if cluster_id not in cluster_profiles.index:
                print(f"Warning: Profile for Cluster {cluster_id} not found in data. Skipping.")
                pbar.update(count)
                continue

            cluster_profile = cluster_profiles.loc[cluster_id]

            for i in range(count):
                pbar.set_description(f"Generating Agent {i+1}/{count} for Cluster {cluster_id}")
                persona_data = generate_agent_persona(cluster_profile)

                if persona_data:
                    persona_data['cluster_id'] = cluster_id
                    persona_data['agent_id'] = f"cluster_{cluster_id}_agent_{i+1:02d}"
                    all_personas.append(persona_data)
                else:
                    print(f"  - FAILED to generate persona for cluster_{cluster_id}_agent_{i+1:02d} after multiple attempts.")

                pbar.update(1)

    try:
        with open(OUTPUT_JSON_PATH, 'w', encoding='utf-8') as f:
            json.dump(all_personas, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Success! All {len(all_personas)} lunch personas have been saved to: {OUTPUT_JSON_PATH}")
    except Exception as e:
        print(f"\n❌ Error: Could not write results to file {OUTPUT_JSON_PATH}. Details: {e}")

if __name__ == "__main__":
    main()