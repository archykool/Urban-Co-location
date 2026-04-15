# Urban Co-location — Research Project

This repository contains the full research pipeline for studying **urban co-location patterns** in London, focusing on Canary Wharf. The project integrates mobility data, POI datasets, and network analysis to understand how different urban activities spatially and temporally co-locate.

---

## 📁 Folder Structure

```
UrbanColocation/
├── Coding/                          # Analysis notebooks (main pipeline)
│   ├── (Archive)/                   # Archived/experimental scripts
│   │
│   ├── AG_01_SafeGraph_Cleaning.ipynb              # Step 1: SafeGraph POI data cleaning
│   ├── AG_02_Co-location_Network.ipynb             # Step 2: Build co-location network
│   ├── AG_03_Viz_HDBSCAN.ipynb                     # Step 3: HDBSCAN clustering visualization
│   ├── AG_04_MobilityAnalysisinCW_Trail1Analysis.ipynb    # Step 4a: Mobility analysis (primary)
│   ├── AG_04_MobilityAnalysisinCW_Trail2Robustness.ipynb  # Step 4b: Mobility analysis (robustness)
│   ├── AG_05_BuildingsFunctionalInference_Trail1Overture.ipynb  # Step 5a: Building inference (Overture)
│   ├── AG_05_BuildingsFunctionalInference_Trail2Safegraph.ipynb # Step 5b: Building inference (SafeGraph)
│   ├── AG_06_Dependency Network by Layers.ipynb    # Step 6: Multi-layer dependency network
│   ├── AG_07_Counterfactual Cascading Impacts Simulation.ipynb  # Step 7: Counterfactual simulation
│   ├── AG_mobility_patterns.ipynb                  # Mobility pattern exploration
│   │
│   ├── Kb_*.ipynb                   # Knowledge-building / supporting analysis notebooks
│   │   ├── Kb_INTERACTIVE SDI.ipynb             # Interactive spatial diversity index
│   │   ├── Kb_TUBE Network.ipynb                # TfL tube network analysis
│   │   ├── Kb_inferred_homelocations.ipynb      # Inferred home location logic
│   │   ├── Kb_residents.ipynb                   # Resident identification
│   │   ├── Kb_shannon diversity index.ipynb     # Shannon diversity index computation
│   │   ├── Kb_temporal_pattern.ipynb            # Temporal visit patterns
│   │   └── Kb_visitorinfo.ipynb                 # Visitor information analysis
│   │
│   ├── R-Li_*.ipynb                 # Data pre-processing notebooks
│   │   ├── R-Li_Locomizer_Filter.ipynb          # Locomizer mobility data filtering
│   │   ├── R-Li_Locomizer_Validation.ipynb      # Mobility data validation
│   │   ├── R-Li_London_LSOA_Selection.ipynb     # London LSOA geographic selection
│   │   ├── R-Li_London_Wards_Selection.ipynb    # London Wards geographic selection
│   │   ├── R-Li_SafeGraph_01_Merge_Filter.ipynb # SafeGraph merge & filter
│   │   ├── R-Li_SafeGraph_02_Category.ipynb     # SafeGraph category mapping
│   │   ├── R-Li_TfL_StationFootfall.ipynb       # TfL station footfall data
│   │   └── R-Li_overture_api_poi_building_analysis.ipynb  # Overture Maps API analysis
│   │
│   └── stable_homes.parquet         # Inferred stable home locations (processed data)
│
└── Viz/                      # Output visualizations (from GitHub)
    └── visualizations/
        ├── Canary_Wharf_Network_Final_V3.html     # Co-location network (Canary Wharf)
        ├── Final_Super_POI_Map.html               # Aggregated POI co-location map
        ├── MAZ.html                               # Multi-Activity Zone visualization
        ├── Static_Urban_Network_Optimized.html    # Optimized static urban network
        └── temporal_mapping.html                  # Temporal activity dynamics
```

---

## 🔬 Research Pipeline

The main analysis follows a sequential pipeline (`AG_01` → `AG_07`):

| Step | Notebook | Description |
|------|----------|-------------|
| 1 | `AG_01` | Clean and filter SafeGraph POI visit data |
| 2 | `AG_02` | Construct the co-location network between POI categories |
| 3 | `AG_03` | Visualize clusters using HDBSCAN |
| 4 | `AG_04` | Analyse mobility patterns in Canary Wharf (two trails) |
| 5 | `AG_05` | Infer building functions from Overture Maps & SafeGraph (two trails) |
| 6 | `AG_06` | Build multi-layer dependency networks |
| 7 | `AG_07` | Run counterfactual cascading impact simulations |

---

## 📊 Data Sources

- **SafeGraph** — POI visit patterns and place attributes
- **Locomizer** — Mobility and home/work location data
- **Overture Maps** — Building footprints and POI data
- **Transport for London (TfL)** — Tube network and station footfall
- **London LSOA / Wards** — Geographic boundary data

---

## 🗺️ Visualizations

Interactive HTML outputs are stored in `Viz/visualizations/`. Open any file directly in a browser (note: `MAZ.html` and `temporal_mapping.html` are ~15–19 MB and may take a moment to load).

---

## 🚀 Getting Started

1. **Install dependencies** — Notebooks use Python with standard geospatial and network analysis libraries (e.g. `pandas`, `geopandas`, `networkx`, `folium`, `hdbscan`)
2. **Run notebooks in order** — Start from `AG_01_SafeGraph_Cleaning.ipynb` and follow the numbered sequence
3. **View outputs** — Open any `.html` file in `Viz/visualizations/` in a browser

---

## 📬 Contact

For questions or contributions, please open an issue or pull request on [GitHub](https://github.com/archykool/Urban-Co-location).
