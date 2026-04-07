# Dheeraj Chand

**Phone:** 202.550.7110 | **Email:** dheeraj.chand@gmail.com | **Website:** https://www.dheerajchand.com | **LinkedIn:** https://www.linkedin.com/in/dheerajchand/ | **Location:** Austin, TX

## Professional Summary

Data analyst with 20+ years building the analytical infrastructure, not just using it. I designed 37 data models for Census, education, labor, and judicial geographies. I built a federated data warehouse harmonizing behavioral, demographic, econometric, and geographical data from dozens of government agencies into a unified analytical layer. I used feature adoption and usage telemetry to drive product decisions across platforms serving thousands of users. I found systematic demographic coding errors that nobody else had caught — decades of miscoding affecting 50M+ voters — and built ML algorithms that improved classification accuracy from 23% to 64%. My analysis has been cited in Supreme Court proceedings. I don't just find patterns — I make sure the data underneath them is right.

## Key Achievements and Impact

### Impact
- Discovered systematic race coding errors in national voter databases affecting all Black and Asian-American voters — decades of miscoding nobody else had caught. Built geospatial ML algorithms improving classification accuracy from **23%** to **64%**.
- Built cloud-based data warehouse on AWS processing billions of records with **99.94%** accuracy across **178,000**+ precincts. Geospatial query methods returned results in ~**15%** of the time traditional string comparison required.
- Designed ETL pipelines using PySpark, dbt, Databricks, and PostgreSQL/PostGIS — processing large-scale geospatial datasets with automated quality monitoring.
- Redesigned sampling methodologies to achieve stronger sample-to-universe correspondence, producing more representative surveys and more reliable electoral predictions across presidential, gubernatorial, congressional, and senatorial campaigns.

## Core Competencies

• **Programming and Development**
• **Machine Learning & AI**
• **Data Infrastructure**
• **Geospatial Technologies**

## Professional Experience

### Partner
**Siege Analytics | Austin, TX | 2005 - Present**

*Data Science & Political Analytics*

- Discovered systematic race coding errors in national voter databases affecting **50M**+ voters. Built geospatial ML algorithms improving demographic classification accuracy from **23%** to **64%**
- Built a redistricting platform used by **12,847** analysts across 89 organizations during the 2021 cycle, with real-time collaborative editing and Census integration
- Redesigned sampling methodologies to improve sample-to-universe correspondence, producing more representative surveys across electoral campaigns at every level
- Invented trigonometric boundary estimation algorithm that cut mapping costs **73.5%**, saving organizations **$4.7M**
- Built real-time FEC fraud detection and analysis system (live at [elect.info](https://elect.info)) using Python, Pandas, and PySpark — applied the same federated medallion pattern from Civic Graph to campaign finance data from thousands of committees with different reporting formats
- Briefed senior government officials on election integrity and voter sentiment. Data analysis cited in Supreme Court case proceedings

### Data Products Manager
**Helm/Murmuration | Austin, TX | 2021 - 2023**

*Democratic Electoral Technology*

- Designed and built Civic Graph — a federated medallion architecture data warehouse harmonizing behavioral, attitudinal, demographic, econometric, and geographical data from state, federal, and international agencies into a unified analytical layer
- Managed an engineering team of 11 while setting technical direction for data architecture and pipeline modernization
- Modernized legacy ETL processes with dbt, PySpark, Snowflake, and Databricks workflows — cut processing time by **57%**

### Analytics Supervisor
**GSD&M | Austin, TX | 2018 - 2019**

*Advertising Analytics*

- Rebuilt the Decision Sciences Department from scratch — introduced version control, Agile, and spatial analysis to a team that had been doing everything in Excel
- Implemented spatial analysis and consumer segmentation that revealed patterns in existing customer data nobody had seen before
- Built ML-based segmentation and behavioral clustering models for multi-million dollar advertising campaigns

### Senior Analyst
**Myers Research | Austin, TX | 2012 - 2014**

*Political Research & Analysis*

- Designed survey instruments for specialized voting segments and niche markets
- Co-developed a web application managing all aspects of survey operations — instrument design through data collection and analysis
- Introduced geospatial techniques to enhance market segmentation, providing location-based consumer insights the firm had never offered

### Research Director
**PCCC | Washington, DC | August 2011 - August 2012**

*Political Research & Data Analysis*

- Conceived and built FLEEM — a Twilio-based web application emulating a predictive dialer for regulated political surveys, handling **10,000**+ simultaneous calls
- Built IVR polling system supporting early quantitative research for Senators Martin Heinrich and Elizabeth Warren
- Developed reporting system with Python, GeoDjango, PostGIS, and Apache — tabular and graphical outputs for campaign decision-making

## Key Projects

### Geospatial Demographic Classification System
*2014 - Present*

Machine learning system that discovered systematic race coding errors in national voter databases and improved demographic classification accuracy from 23% to 64%. The finding affected all Black and Asian-American voters in the system.

**Technologies:** Python, Scikit-learn, PostGIS, GeoPandas, TensorFlow, PySpark, AWS
**Impact:** Corrected demographic data affecting 50M+ voters nationwide. Improved electoral prediction accuracy by 22%. Analysis cited in Supreme Court proceedings.

### Civic Graph Federated Data Warehouse
*2021 - 2023*

Federated medallion architecture data warehouse harmonizing behavioral, attitudinal, demographic, econometric, and geographical data longitudinally from state agencies, federal agencies (Census, BLS, NCES), and international sources — each with different schemas, encoding systems, and update cadences — into a unified, queryable analytical layer.

**Technologies:** Python, PostgreSQL, PostGIS, PySpark, Databricks, Snowflake, dbt, ETL Pipelines
**Impact:** Created a multi-dimensional dataset representing $1B+ in accumulated investment, measuring socio-economic change across every dimension at every geographic level over time. Foundation architecture directly informed the elect.info federated pipeline design.

### [Siege Utilities](https://github.com/siege-analytics/siege_utilities) — Geospatial Data Sciences Library
*2019 - Present*

Open-source Python library powering all Siege Analytics workflows. 37 GeoDjango models for Census TIGER, NCES, NLRB, and Federal Judicial Districts. 9 population services for demographic analysis. PySpark/Apache Sedona distributed computing utilities. Includes geospatial computation functions that run inside Databricks without Apache Sedona or C library dependencies. Census API integration for ACS, Decennial, and PL 94-171 redistricting data. Hydra + Pydantic configuration system. 1,884+ tests. Dual-licensed AGPLv3/Commercial.

**Technologies:** Python, GeoDjango, PostGIS, PySpark, Apache Sedona, Databricks, Hydra, Pydantic, Snowflake, Census API
**Impact:** Foundation infrastructure for all Siege Analytics projects — every analysis pipeline and data product depends on it. Demonstrates commitment to open-source and rigorous engineering practices.

### National Redistricting Platform
*2020 - 2022*

Cloud-based GeoDjango platform for redistricting analysis with real-time collaborative editing and Census integration, used by 12,847 analysts across 89 organizations during the 2021 redistricting cycle.

**Technologies:** GeoDjango, PostGIS, AWS, Docker, React, Python, Redis, WebSockets
**Impact:** Reduced mapping costs by 73.5%, saving organizations $4.7M. Made redistricting analysis accessible to organizations that previously couldn't afford it.

### High-Performance Geospatial Tile Server
*2010 - 2011*

Custom tile server for WMS integration enabling interactive visualization of CRM and Census data for political campaigns.

**Technologies:** GeoTools, OpenLayers, Java, MySQL, TileMill, JavaScript
**Impact:** Improved contact rates by 53% and segmentation accuracy by 88% through spatial visualization of campaign data.

## Technical Skills

• **Python: 20+ years: NumPy, Pandas, Scikit-learn, TensorFlow, Django/GeoDjango, Flask, GeoPandas, Pydantic, Hydra, Asyncio**
• **R: 12+ years: statistical modeling, ggplot2, dplyr, spatial packages (sf, sp), Shiny**
• **SQL/PostGIS: 20+ years: PostgreSQL/PostGIS, Snowflake, MySQL, complex spatial queries, optimization, database design**
• **JavaScript: 10+ years: React, D3.js, OpenLayers, Leaflet, Node.js, WebSockets, real-time applications**
• **Java: 8+ years: enterprise applications, Spring, GeoTools for geospatial processing**
• **Other Technologies: QML, Shell scripting, Git, Docker, Kubernetes, infrastructure as code**
• **ML Frameworks: Scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM**
• **Geospatial ML: Spatial feature engineering, geographically weighted regression, spatial clustering, demographic classification**
• **Techniques: Classification, regression, ensemble methods, time series, NLP, agent-based modeling**
• **Validation: Cross-validation, A/B testing, statistical significance, model interpretability, bias detection**
• **Processing: Databricks, Apache Spark, PySpark, Apache Sedona, Dask, distributed computing**
• **Pipelines: Airflow, dbt, ETL design, data quality monitoring, automated testing**
• **Storage: Snowflake, data warehousing, data lakes, columnar storage (Parquet), data modeling**
• **Streaming: Kafka, Redis, real-time processing, event-driven architecture**
• **Databases: PostGIS, SpatiaLite, MongoDB with geospatial extensions, Snowflake**
• **Analysis Tools: GDAL/OGR, QGIS, ArcGIS, spatial indexing, coordinate transformations, LiDAR/PointCloud processing and format conversion (LAS, LAZ, E57, PLY, PCD)**
• **Web Mapping: OpenLayers, Leaflet, Mapbox GL JS, custom tile servers, WMS/WFS**
• **Processing: GeoPandas, Shapely, Fiona, rasterio, spatial ETL pipelines, Apache Sedona**
• **Library: siege_utilities: 37 GeoDjango models, 9 population services, Census API integration, PySpark/Sedona distributed computing**

---

**Website:** https://www.dheerajchand.com | **LinkedIn:** https://www.linkedin.com/in/dheerajchand/