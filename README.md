
# Grid Watch

**Can one architect with free, public data predict when the Texas power grid will be stressed, a day ahead?**

Grid Watch is a 4-week, built-in-public data and ML project. It pulls ERCOT electricity demand and weather data, runs it through a governed Snowflake pipeline, forecasts tomorrow's hourly demand, and flags likely stress hours on a live dashboard. Every forecast is scored against two baselines, including ERCOT's own day-ahead forecast.

> **Status:** Week 1 of 4, in progress. MVP target: November 1, 2026.
> Follow the build on YouTube: **Datad3v**

## What it will include

- Daily ingestion of ERCOT demand data (EIA API) and Texas weather (Open-Meteo)
- Snowflake bronze, silver, and gold layers, defined with Terraform
- dbt transformations with data quality tests
- A demand forecast tracked in MLflow and served through a FastAPI endpoint
- A Streamlit dashboard showing actual vs. forecast demand and predicted stress hours
- CI/CD with GitHub Actions, least-privilege roles, and no secrets in code

## Tech stack

Python · Snowflake · DuckDB · dbt · Terraform · Docker · GitHub Actions · scikit-learn · MLflow · FastAPI · Streamlit

## Roadmap

- [ ] Week 1: Architecture and first data ingestion
- [ ] Week 2: Pipeline, data quality tests, CI/CD
- [ ] Week 3: Forecast model and evaluation against baselines
- [ ] Week 4: Live dashboard, security review, final write-up

## Data sources

- [U.S. Energy Information Administration Open Data API](https://www.eia.gov/opendata/)
- [Open-Meteo](https://open-meteo.com/), weather data licensed under CC BY 4.0

## Author

**Mauricio Guzman**, Solutions Architect
[Portfolio](https://datad3v.github.io/myPortfolio) · [LinkedIn](https://www.linkedin.com/in/mauricio-guzman-profile)
