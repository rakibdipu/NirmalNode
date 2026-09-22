# Bangladesh Air Quality Datasets - Sources, Metadata & Citation Guide

This document catalogs all real-world Bangladesh air quality datasets collected for the **NirmalNode** research project, including exact download sources, authors, DOI, coverage, and variable schemas.

---

## 1. Mendeley Data & Kaggle: Bangladesh AQI Dataset (2000–2025)
- **Kaggle Title**: *Hourly Air Quality Index (AQI) of Bangladesh (2000-2026)*
- **Mendeley Title**: *Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities*
- **Author**: Tapon Paul
- **DOI**: [10.17632/9j447cynb9.2](https://doi.org/10.17632/9j447cynb9.2)
- **License**: Creative Commons Attribution 4.0 (CC BY 4.0)
- **Local File**: `data/raw/mendeley_bangladesh_aqi_hourly_2000_2025.csv` (93.7 MB)
- **Total Records**: 1,048,551 hourly entries (Dhaka alone: 227,016 entries)
- **Variables**: `city_name`, `lat`, `lon`, `datetime`, `pm10`, `pm2_5`, `carbon_monoxide`, `carbon_dioxide`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `aqi`
- **Thesis Citation Format**:
  > Paul, T. (2026). *Bangladesh Air Quality Index (AQI) Dataset (2000–2025): Historical Hourly Air Pollution Data Across 103 Cities*, Mendeley Data, V2, doi: 10.17632/9j447cynb9.2.

---

## 2. U.S. Department of State / AirNow: Dhaka Reference-Grade PM2.5 Dataset
- **Platforms**: U.S. State Department AirNow / Kaggle (*Dhaka Hourly Air Quality 2016-2022*)
- **Monitoring Location**: U.S. Embassy Dhaka, Madani Avenue, Baridhara, Dhaka (BAM-1020 Met One Beta Attenuation Monitor)
- **Local File**: `data/raw/us_embassy_dhaka_hourly_2016_2021.csv` (3.8 MB)
- **Total Records**: 37,832 hourly validated records (2016–2021)
- **Variables**: `Date (LT)`, `Raw Conc.` (PM2.5 ug/m3), `NowCast Conc.`, `AQI`, `AQI Category`, `QC Name`
- **Thesis Citation Format**:
  > U.S. Department of State & U.S. EPA (2016–2021). *AirNow International Air Quality Monitoring Program: U.S. Embassy Dhaka Monitoring Station*, airnow.gov.

---

## 3. Copernicus CAMS & Open-Meteo: Industrial Hotspots Hourly Multi-Pollutant & Meteorology
- **Source**: Copernicus Atmosphere Monitoring Service (CAMS Global Reanalysis) & Open-Meteo Archive API
- **Locations**:
  - **Dhaka Industrial Zone**: Lat 23.8103, Lon 90.4125 (17,544 hourly records)
  - **Gazipur Industrial Cluster (RMG Hub)**: Lat 23.9999, Lon 90.4203 (17,544 hourly records)
- **Local Files**: `data/raw/dhaka_hourly_2023_2024.csv`, `data/raw/gazipur_hourly_2023_2024.csv`
- **Total Records**: 35,088 hourly records
- **Variables**: `pm2_5`, `pm10`, `carbon_monoxide`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `dust`, `temperature_2m`, `relative_humidity_2m`, `surface_pressure`, `wind_speed_10m`
- **Thesis Citation Format**:
  > Copernicus Atmosphere Monitoring Service (CAMS) & Open-Meteo (2023–2024). *High-Resolution Atmospheric Composition and Meteorological Hourly Time-Series for Dhaka and Gazipur, Bangladesh*.

---

## 4. Department of Environment (DoE) Bangladesh: CASE CAMS Network
- **Source**: Clean Air and Sustainable Environment (CASE) Project, Ministry of Environment, Forest and Climate Change, Bangladesh
- **Locations**: Dhaka (Sangsad Bhaban, Farmgate, Darus Salam), Gazipur, Narayanganj, Savar, Chittagong, Khulna, Rajshahi, Sylhet
- **Local File**: `data/raw/case_doe_bangladesh_cities.csv` (1.0 MB)
- **Total Records**: 24,044 observations
- **Variables**: `Date`, `Location`, `AQI`, `Category`, `CAMS tag`
- **Thesis Citation Format**:
  > Department of Environment (DoE) Bangladesh (2016–2020). *Clean Air and Sustainable Environment (CASE) Project: Continuous Air Quality Monitoring Station (CAMS) Reports*, Government of the People's Republic of Bangladesh.

---

## 5. Zenodo & Kaggle: Dhaka Multi-Pollutant Dataset
- **Platforms**: Zenodo & Kaggle (*Air Quality Dataset for Dhaka*)
- **Authors**: Nitiraj Kulkarni, Jagadish Tawade
- **DOI**: [10.5281/zenodo.18673791](https://doi.org/10.5281/zenodo.18673791)
- **Local File**: `data/raw/zenodo_dhaka_daily_2022_2026.csv`
- **Total Records**: 1,298 daily records (2022–2026)
- **Variables**: `date`, `pm10`, `pm2_5`, `carbon_monoxide`, `nitrogen_dioxide`, `sulphur_dioxide`, `ozone`, `aerosol_optical_depth`, `dust`, `uv_index`, `us_aqi`
- **Thesis Citation Format**:
  > Kulkarni, N., & Tawade, J. (2026). *Air Quality Dataset for Dhaka (2022-08-01 to 2026-02-18)*, Zenodo, doi: 10.5281/zenodo.18673791.

---

## 6. Processed & Merged Master Datasets
1. **`data/processed/bangladesh_air_quality_master.csv`** (35,088 rows):
   - Harmonized multi-pollutant and weather hourly dataset for Dhaka & Gazipur with US EPA AQI.
2. **`data/processed/nirmalnode_streaming_dataset.csv`** (35,088 rows):
   - Formatted into the exact 14 streaming features required by `nirmal_ml_engine.py` (PMS5003 PM & count channels + MQ135, MQ136, MiCS-4514, MP135 gas ADC channels).
