#!/usr/bin/env python3
"""
Resume Data Generator for ReportLab Script
Creates structured JSON input files for multiple resume versions
"""

import json
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """Create the directory structure for all resume versions"""

    resume_versions = [
        "dheeraj_research_focused",
        "dheeraj_technical_detailed",
        "dheeraj_comprehensive_full",
        "dheeraj_consulting_minimal",
        "dheeraj_software_engineer"
    ]

    base_inputs = Path("inputs")
    base_outputs = Path("outputs")

    for version in resume_versions:
        # Create input directories
        input_dir = base_inputs / version
        input_dir.mkdir(parents=True, exist_ok=True)

        # Create output directories with format subdirs
        output_dir = base_outputs / version
        (output_dir / "pdf").mkdir(parents=True, exist_ok=True)
        (output_dir / "docx").mkdir(parents=True, exist_ok=True)
        (output_dir / "rtf").mkdir(parents=True, exist_ok=True)

        print(f"✅ Created directories for: {version}")

def create_research_focused_data():
    """Create data for research-focused version"""

    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'Director of Research and Analysis',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        },

        'summary': """Research and Data Analytics Leader with 20+ years of experience directing applied research projects from conception to completion focused on economic mobility, community development, and social impact. Proven track record of leading cross-functional teams, translating complex research insights for diverse stakeholders including elected officials and community organizations, and implementing evidence-based solutions that drive meaningful outcomes. Expert in research methodology design, statistical analysis, and community partnership development with extensive experience serving vulnerable populations and addressing systemic poverty challenges.""",

        'competencies': {
            'Applied Research Leadership': [
                'Applied Research Project Management (Conception to Completion)',
                'Research Methodology Design and Implementation',
                'Cross-functional Team Leadership and Mentoring',
                'Stakeholder Communication and Translation of Complex Findings',
                'Evidence-Based Framework Development',
                'Survey Methodology and Consumer Insights',
                'Statistical Analysis and Data Validation'
            ],
            'Technical Proficiency': [
                'Programming: Python (Pandas, SciKit, TensorFlow, Django), R, SQL, Scala',
                'Data Platforms: PostgreSQL, MySQL, Snowflake, Spark, MongoDB, Oracle',
                'Analysis Tools: Excel (Advanced), Tableau, PowerBI, SPSS, SAS',
                'Research Tools: Survey Design, Sampling Methodology, Statistical Modeling',
                'Geospatial Analysis: ESRI ArcGIS, Quantum GIS, PostGIS, OSGeo'
            ],
            'Strategic Operations': [
                'Community Partnership Development',
                'Government Relations and Policy Analysis',
                'Multi-million Dollar Project Management',
                'Performance Measurement and Evaluation',
                'Data-Driven Decision Making for Social Impact',
                'Public Systems Integration',
                'Stakeholder Briefing and Expert Testimony'
            ]
        },

        'experience': [
            {
                'title': 'PARTNER',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Leading Applied Research Projects with Community Development Focus',
                'responsibilities': [
                    'Direct comprehensive applied research projects from conception to completion for organizations focused on economic mobility and community development',
                    'Lead multi-million dollar research initiatives involving sensitive demographic and economic data addressing poverty and community health challenges',
                    'Translate complex research findings for diverse stakeholder groups including elected officials, NGO leadership, and community organizations',
                    'Collaborate with government agencies and research institutions to develop evidence-based solutions addressing systemic poverty',
                    'Manage client relationships across public sector and nonprofit organizations, consistently delivering research that drives strategic decision-making',
                    'Develop custom analytical tools processing billions of records to identify patterns in economic mobility and demographic trends'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Research Team Leadership and Methodology Innovation',
                'responsibilities': [
                    'Led cross-functional team of eleven data engineers and analysts focused on community organizing and social justice research',
                    'Managed national research team of five analysts specializing in community engagement and demographic analysis',
                    'Overhauled organization research methodology and data collection operations, significantly improving accuracy and response rates',
                    'Designed comprehensive data warehouse integrating demographic, economic, and behavioral data for evidence-based decision making',
                    'Developed advanced analytical pipelines enhancing community segmentation and outcome prediction capabilities',
                    'Trained staff in data visualization and communication techniques to improve research deliverable quality'
                ]
            },
            {
                'title': 'ANALYTICS SUPERVISOR',
                'company': 'GSD&M, Austin, TX',
                'dates': '2018 – 2019',
                'subtitle': 'Research Operations and Team Development',
                'responsibilities': [
                    'Restructured research department to scale capabilities from small-scale analysis to comprehensive applied research operations',
                    'Managed three analysts, mentoring them in advanced research techniques and stakeholder communication',
                    'Implemented spatial analysis and segmentation methodologies revealing new insights about community needs',
                    'Introduced version control and Agile project management methodologies, improving delivery timelines by 40%',
                    'Developed standardized research reporting frameworks ensuring consistent, high-quality deliverables'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER',
                'company': 'Mautinoa Technologies, Austin, TX',
                'dates': '2016 – 2018',
                'subtitle': 'Applied Research in Humanitarian Context',
                'responsibilities': [
                    'Conceived and engineered econometric simulation software for measuring humanitarian crisis intervention effectiveness',
                    'Collaborated with data directors at multinational NGOs (UNICEF, IFRC) to develop evidence-based intervention frameworks',
                    'Conducted geospatial analysis on vulnerable populations to assess intervention impact and optimize resource allocation',
                    'Designed research methodologies for measuring complex social outcomes in crisis environments'
                ]
            },
            {
                'title': 'RESEARCH DIRECTOR',
                'company': 'PCCC, Austin, TX',
                'dates': '2011 – 2012',
                'subtitle': 'Large-Scale Applied Research Initiative Leadership',
                'responsibilities': [
                    'Led all aspects of applied research design, implementation, analysis, and reporting for major national studies',
                    'Engineered data collection system facilitating thousands of simultaneous surveys, significantly increasing research scale',
                    'Developed new statistical methods for geographic boundary estimation, enhancing community-level analysis capabilities',
                    'Created data visualization solutions improving stakeholder understanding of complex research findings'
                ]
            }
        ],

        'achievements': {
            'Research Leadership and Community Impact': [
                'Regular expert testimony and consultation on research methodology for journalists, elected officials, and community leaders',
                'Research analysis used in court cases addressing housing, redistricting, and community development with rigorous methodology',
                'Conceived and deployed cloud-based analytical software used by thousands of researchers nationwide for community-focused research'
            ],
            'Systems and Infrastructure Development': [
                'Designed multi-tenant data warehouse tracking decades of demographic, economic, and policy changes affecting vulnerable populations',
                'Developed comprehensive research frameworks for measuring complex social outcomes and community intervention effectiveness',
                'Created scalable research methodologies supporting evidence-based decision making for multi-billion dollar public systems'
            ],
            'Community and Stakeholder Engagement': [
                'Extensive experience briefing elected officials, NGO leadership, and senior staff on research findings and policy implications',
                'Proven track record translating complex research for diverse audiences including community organizations and government agencies',
                'Successfully managed research partnerships across public sector and community-based organizations focused on addressing systemic poverty'
            ]
        },

        '_metadata': {
            'version': 'research_focused',
            'created': datetime.now().isoformat(),
            'description': 'Research-focused version emphasizing applied research leadership and community impact'
        }
    }

    return data

def create_technical_detailed_data():
    """Create data for technical detailed version"""

    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'Senior Geospatial Data Engineer & Technical Architect',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        },

        'summary': """Senior Data Engineer with 20+ years of expertise in geospatial data platforms, big data processing, and distributed systems architecture. Deep specialist in Apache Spark/Sedona for large-scale geospatial analytics, with fluency across ESRI, OSGeo, and SAFE FME technology stacks. Proven track record architecting production systems like BALLISTA and DAMON serving thousands of users, implementing PySpark pipelines processing billions of spatial records, and leading engineering teams. Expert in full-stack geospatial development from PostGIS database optimization to React-based mapping interfaces.""",

        'competencies': {
            'Big Data & Geospatial Processing': [
                'Apache Spark: PySpark, Spark SQL, Scala Spark, Sedona (geospatial), distributed processing',
                'Geospatial Databases: PostGIS (advanced), Oracle Spatial, spatial indexing, query optimization',
                'ETL/ELT: dbt, Informatica, CDAP, custom PySpark pipelines, data governance frameworks',
                'Cloud Platforms: AWS (EC2, RDS, S3), Snowflake, Hadoop clusters, distributed computing',
                'Streaming: Real-time data processing, Kafka integration, event-driven architectures'
            ],
            'GIS Technology Stack': [
                'ESRI: ArcGIS Server, ArcGIS Pro, enterprise geodatabases, ModelBuilder, ArcPy scripting',
                'OSGeo: QGIS, GRASS GIS, GDAL/OGR, GeoServer, spatial analysis workflows',
                'SAFE FME: Data transformation, format conversion, spatial ETL, enterprise integration',
                'Web Mapping: OpenLayers, Leaflet, MapBox, tile servers, WMS/WFS services',
                'Spatial Analysis: Clustering algorithms, boundary estimation, network analysis, geostatistics'
            ],
            'Software Development & Architecture': [
                'Python: Django/GeoDjango, Flask, Pandas, NumPy, SciKit-Learn, spatial libraries',
                'JVM: Scala (Spark), Java (GeoTools, enterprise), Groovy scripting',
                'Web Technologies: React, JavaScript, d3.js, RESTful APIs, microservices',
                'Databases: PostgreSQL/PostGIS, Oracle, MySQL, MongoDB, spatial optimization',
                'DevOps: Docker, Kubernetes, CI/CD (GitLab, GitHub), Airflow, Celery, nginx'
            ]
        },

        'experience': [
            {
                'title': 'PARTNER & SENIOR DATA ARCHITECT',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Geospatial Data Platform Architecture and Big Data Engineering',
                'responsibilities': [
                    'Architected and engineered production geospatial platforms including BALLISTA (redistricting) and DAMON (boundary estimation) serving thousands of analysts',
                    'Built enterprise-scale ETL pipelines using PySpark and Sedona processing billions of geospatial records with advanced spatial clustering algorithms',
                    'Developed multi-tenant data warehouse integrating Census, electoral, and demographic data using PostGIS and Spark SQL optimization',
                    'Implemented fraud detection systems processing multi-terabyte campaign finance datasets with real-time spatial analysis capabilities',
                    'Created parametric boundary estimation algorithms using PostGIS and GRASS without machine learning dependencies',
                    'Led integration of ESRI ArcGIS Server, OSGeo tools (QGIS, GRASS), and SAFE FME for enterprise geospatial workflows'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Enterprise Geospatial Data Engineering and Team Leadership',
                'responsibilities': [
                    'Led team of 11 engineers building multi-dimensional data warehouse using Spark/Sedona for longitudinal geospatial analysis',
                    'Designed scalable architecture integrating Census Bureau, Bureau of Labor Statistics data using advanced PostGIS and dbt transformations',
                    'Modernized legacy ETL systems implementing Scala/Spark and Sedona workflows, achieving 57% performance improvement',
                    'Built comprehensive data governance framework with PostGIS quality validation and GRASS-based spatial analysis pipelines',
                    'Developed Random Device Engagement (RDE) survey platform with real-time geospatial aggregation and visualization',
                    'Trained engineering staff on OSGeo technologies (QGIS, GRASS) and advanced PostGIS spatial analysis techniques'
                ]
            },
            {
                'title': 'ANALYTICS SUPERVISOR & BIG DATA ENGINEER',
                'company': 'GSD&M, Austin, TX',
                'dates': '2018 – 2019',
                'subtitle': 'Big Data Infrastructure Transformation and Geospatial Analytics',
                'responsibilities': [
                    'Transformed desktop GIS operations into distributed Hadoop/Spark clusters on AWS with ESRI ArcGIS Server integration',
                    'Developed customer segmentation platform using Spark/PySpark with advanced spatial analysis and machine learning',
                    'Built real-time geospatial dashboards using React, d3.js, and OpenLayers for Fortune 500 client analytics',
                    'Integrated ESRI and OSGeo technology stacks for scalable geospatial processing of advertising and customer data',
                    'Implemented spatial clustering algorithms and demographic analysis workflows improving targeting efficacy by 40%'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER & GEOSPATIAL DEVELOPER',
                'company': 'Mautinoa Technologies, Austin, TX',
                'dates': '2016 – 2018',
                'subtitle': 'GeoDjango Platform and Multi-Agent Geospatial Modeling',
                'responsibilities': [
                    'Architected SimCrisis: GeoDjango web application with NetLogo multi-agent modeling for econometric crisis simulations',
                    'Implemented advanced PostGIS spatial algorithms for population analysis and humanitarian intervention optimization',
                    'Built modular geospatial architecture accepting custom rule extensions for crisis modeling and supply chain analysis',
                    'Collaborated with UNICEF and IFRC technical teams on geospatial requirements and validation workflows',
                    'Developed RESTful APIs and React interfaces for complex geospatial simulation visualization and analysis'
                ]
            },
            {
                'title': 'SENIOR DATA ANALYST & GIS DEVELOPER',
                'company': 'Myers Research, Austin, TX',
                'dates': '2012 – 2014',
                'subtitle': 'Survey Platform Development with Integrated Geospatial Analysis',
                'responsibilities': [
                    'Co-developed RACSO: comprehensive GeoDjango platform for survey operations with advanced PostGIS spatial analysis',
                    'Implemented geospatial market segmentation using ESRI and OSGeo tools for location-based demographic insights',
                    'Built survey instrument design tools with integrated spatial sampling and geographic targeting capabilities',
                    'Optimized PostGIS database schemas for large-scale spatial survey data storage and complex geographic queries',
                    'Led technical evaluation of 1,200+ vendor proposals, selecting optimal geospatial technology stack'
                ]
            }
        ],

        'achievements': {
            'Geospatial Platform Engineering': [
                'Architected BALLISTA redistricting platform processing Census data for thousands of analysts with real-time PostGIS collaborative editing',
                'Built DAMON boundary estimation system using advanced PostGIS algorithms and incomplete data without machine learning requirements',
                'Developed SimCrisis geospatial simulation platform integrating NetLogo multi-agent modeling with GeoDjango web interface',
                'Created production-scale survey platform RACSO with integrated ESRI and OSGeo geospatial analysis capabilities'
            ],
            'Big Data & Performance Engineering': [
                'Implemented Spark/Sedona ETL pipelines achieving 57% performance improvement processing billions of geospatial records',
                'Built distributed geospatial systems using AWS Hadoop clusters with ESRI ArcGIS Server and PostGIS integration',
                'Developed fraud detection algorithms processing multi-terabyte datasets with real-time PostGIS spatial analysis',
                'Created spatial clustering algorithms using PySpark and Sedona achieving 88% improvement in targeting efficacy'
            ],
            'Technical Innovation & Leadership': [
                'Pioneered integration of ESRI, OSGeo (QGIS, GRASS), and SAFE FME technologies in production web applications',
                'Led engineering teams up to 11 developers specializing in geospatial data architecture and Spark/Sedona optimization',
                'Established technical standards for PostGIS database design, spatial indexing, and distributed geospatial processing',
                'Developed comprehensive spatial data governance frameworks ensuring quality across petabyte-scale geospatial warehouses'
            ]
        },

        '_metadata': {
            'version': 'technical_detailed',
            'created': datetime.now().isoformat(),
            'description': 'Technical version emphasizing engineering skills, data architecture, and platform development'
        }
    }

    return data

def create_comprehensive_full_data():
    """Create comprehensive version with complete work history"""

    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'Research, Data Analytics & Engineering Professional',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        },

        'summary': """Research & Data Professional with 20+ years of comprehensive experience spanning applied research, data engineering, and software development. Expert in translating complex analytical requirements into scalable technical solutions. Proven track record leading cross-functional teams, architecting data platforms, and delivering insights that drive strategic decision-making across political, nonprofit, and technology sectors. Deep expertise in survey methodology, geospatial analysis, and building production systems for sensitive data applications.""",

        'competencies': {
            'Research and Analytics': [
                'Survey Methodology: Design, sampling, weighting, longitudinal analysis',
                'Statistical Analysis: Regression modeling, clustering, segmentation, machine learning',
                'Geospatial Analysis: Spatial clustering, boundary estimation, demographic mapping',
                'Data Visualization: Tableau, PowerBI, d3.js, Matplotlib, Seaborn, choropleth mapping',
                'Research Management: Team leadership, methodology design, stakeholder communication'
            ],
            'Programming and Development': [
                'Python: Django/GeoDjango, Flask, Pandas, PySpark, SciKit-Learn, TensorFlow',
                'JVM Languages: Scala (Spark), Java, Groovy',
                'Web Technologies: JavaScript, React, d3.js, PHP, HTML/CSS',
                'Database Languages: SQL, T-SQL, PostgreSQL/PostGIS',
                'Statistical Computing: R, SPSS, SAS, Stata'
            ],
            'Data Infrastructure': [
                'Cloud Platforms: AWS (EC2, RDS, S3), Google Cloud Platform, Microsoft Azure',
                'Big Data: Apache Spark, PySpark, Hadoop, Snowflake, dbt',
                'Databases: PostgreSQL/PostGIS, MySQL, Oracle, MongoDB, Neo4j',
                'Geospatial: ESRI ArcGIS, Quantum GIS, GeoServer, OSGeo, GRASS',
                'DevOps: Docker, Git, CI/CD pipelines, automated testing, version control'
            ]
        },

        'experience': [
            {
                'title': 'PARTNER',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Data, Technology and Strategy Consulting',
                'responsibilities': [
                    'Conduct comprehensive quantitative and qualitative research studies for political candidates and organizations',
                    'Architect cloud-based data warehouse solutions processing billions of records for electoral analytics',
                    'Design scalable ETL pipelines using PySpark and dbt for large-scale geospatial and demographic datasets',
                    'Develop custom analytical tools and algorithms for fraud detection and spatial clustering',
                    'Manage complex client relationships across political, nonprofit, and technology sectors',
                    'Lead technical architecture decisions for data-intensive applications and platforms'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Enterprise Data Platform Development',
                'responsibilities': [
                    'Led design and implementation of enterprise-scale multi-tenant data warehouse',
                    'Managed engineering team of 11 professionals setting technical direction',
                    'Modernized legacy ETL processes implementing dbt and PySpark workflows',
                    'Overhauled survey methodology using Random Device Engagement and text messaging',
                    'Developed data governance framework and quality control measures',
                    'Built meta-analytical dataset for longitudinal analysis standardizing survey instruments'
                ]
            },
            {
                'title': 'ANALYTICS SUPERVISOR',
                'company': 'GSD&M, Austin, TX',
                'dates': '2018 – 2019',
                'subtitle': 'Big Data Transformation and Advanced Analytics',
                'responsibilities': [
                    'Transformed small data team into big data engineering operation scaling to Hadoop clusters',
                    'Managed accounts including US Air Force, Southwest Airlines/Chase, and Indeed',
                    'Implemented spatial analysis and consumer segmentation methodologies',
                    'Applied advanced statistical and ML techniques for behavioral clustering',
                    'Introduced version control and Agile methodologies improving delivery by 40%'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER',
                'company': 'Mautinoa Technologies, Austin, TX',
                'dates': '2016 – 2018',
                'subtitle': 'Financial Technology and Humanitarian Crisis Modeling',
                'responsibilities': [
                    'Conceived and engineered SimCrisis: GeoDjango application for econometric crisis simulations',
                    'Collaborated with International Federation of Red Cross, UNICEF, and humanitarian organizations',
                    'Implemented geospatial analysis for population impact assessment and resource optimization',
                    'Developed agent-based modeling and statistical analysis systems for crisis prediction'
                ]
            },
            {
                'title': 'SENIOR ANALYST',
                'company': 'Myers Research, Austin, TX',
                'dates': '2012 – 2014',
                'subtitle': 'Strategic Research and Survey Operations',
                'responsibilities': [
                    'Co-developed RACSO web application for comprehensive survey operations management',
                    'Designed survey instruments for specialized voting segments and niche markets',
                    'Introduced geospatial techniques enhancing market segmentation capabilities',
                    'Managed RFP process analyzing bids from 1,200+ vendors for platform development'
                ]
            },
            {
                'title': 'RESEARCH DIRECTOR',
                'company': 'Progressive Change Campaign Committee, Austin, TX',
                'dates': '2011 – 2012',
                'subtitle': 'Large-Scale Survey Systems and Method Development',
                'responsibilities': [
                    'Engineered FLEEM web application using Twilio API for thousands of simultaneous IVR surveys',
                    'Led all aspects of survey design, implementation, data analysis, and reporting',
                    'Developed new statistical methods for boundary estimation and geographic segmentation',
                    'Created comprehensive data visualization solutions for complex research findings'
                ]
            }
        ],

        'achievements': {
            'Software Development and Innovation': [
                'Conceived and deployed BALLISTA redistricting software used by thousands of analysts nationwide',
                'Developed DAMON boundary estimation system using incomplete data without ML requirements',
                'Created SimCrisis econometric simulation platform for humanitarian intervention modeling',
                'Built RACSO comprehensive survey operations platform from RFP through deployment'
            ],
            'Data Architecture and Engineering': [
                'Designed multi-dimensional data warehouse tracking decades of political and economic change',
                'Implemented scalable ETL pipelines achieving 57% performance improvement',
                'Developed fraud detection systems across multi-terabyte campaign finance datasets',
                'Created spatial clustering algorithms achieving 88% improved targeting efficacy'
            ],
            'Research Impact and Recognition': [
                'Research analysis used in court cases for redistricting, housing, and community development',
                'Regular expert testimony on methodology for journalists and elected officials',
                'Built foundational polling consortium infrastructure adopted by major research organizations',
                'Pioneered integration of geospatial techniques into political and market research'
            ]
        },

        '_metadata': {
            'version': 'comprehensive_full',
            'created': datetime.now().isoformat(),
            'description': 'Comprehensive version with complete work history and technical depth'
        }
    }

    return data

def create_consulting_minimal_data():
    """Create minimal consulting-focused version"""

    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'Data Analytics & Technology Consultant',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        },

        'summary': """Strategic data and technology consultant with 20+ years solving complex problems through analytics and software development. Specializes in transforming organizational data capabilities from concept to production. Expert in translating business requirements into technical solutions, with proven success across political, nonprofit, and technology sectors. Currently building scalable data platforms while modernizing legacy systems for improved performance and maintainability.""",

        'competencies': {
            'Consulting Expertise': [
                'Strategic Data Analysis (Exploratory, Predictive, Explanatory)',
                'Data Engineering and Infrastructure Development',
                'Systems Integration and Architecture Consulting',
                'Project Management and Product Management',
                'Team Leadership and Technical Mentoring',
                'Stakeholder Communication and Requirements Gathering'
            ],
            'Technical Solutions': [
                'Programming: Python (Django, Pandas, PySpark), Scala (Spark), JavaScript',
                'Data Platforms: PostgreSQL/PostGIS, Snowflake, MongoDB, AWS, GCP',
                'Analytics: Tableau, PowerBI, Statistical Modeling, Machine Learning',
                'Integration: APIs, ETL/ELT pipelines, Cloud migrations, Legacy modernization'
            ],
            'Industry Focus': [
                'Political and Electoral Data Analytics',
                'Nonprofit and Community Organization Solutions',
                'Technology Startup and Scale-up Consulting',
                'Geospatial Analysis and Demographic Intelligence',
                'Survey Research and Consumer Behavior Analysis'
            ]
        },

        'experience': [
            {
                'title': 'PRINCIPAL CONSULTANT',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Data, Technology and Strategy Consulting',
                'responsibilities': [
                    'Provide comprehensive data analysis, engineering, and strategic planning for diverse client portfolio',
                    'Develop custom software solutions and data pipeline architectures for complex integration requirements',
                    'Lead digital transformation initiatives including cloud migrations and legacy system modernization',
                    'Deliver management consulting including project planning, team building, and operational optimization',
                    'Maintain long-term strategic partnerships with clients across political, nonprofit, and technology sectors'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Enterprise Platform Development Leadership',
                'responsibilities': [
                    'Conceived and developed integrated data platform combining government, NGO, and proprietary datasets',
                    'Led engineering team building multi-tenant data warehouse from Census and economic statistics',
                    'Designed longitudinal analysis capabilities across demographic, economic, and geographic dimensions',
                    'Managed polling operations focusing on modern survey methodologies and text-based engagement',
                    'Trained technical staff on open source geospatial technologies and analytical best practices'
                ]
            },
            {
                'title': 'TECHNICAL CONSULTANT',
                'company': 'Various Clients, Austin, TX',
                'dates': '2016 – 2021',
                'subtitle': 'Specialized Project Consulting',
                'responsibilities': [
                    'Developed SimCrisis humanitarian modeling platform for international NGO collaboration',
                    'Created RACSO survey operations platform through vendor management and technical leadership',
                    'Built advanced analytics capabilities for advertising and customer intelligence applications',
                    'Implemented scalable telephony integration systems for large-scale data collection'
                ]
            }
        ],

        'achievements': {
            'Technology Innovation': [
                'Developed proprietary B2B SaaS solutions for data analytics and geospatial applications',
                'Created open source frameworks for political and social behavior prediction',
                'Pioneered integration of advanced mapping techniques into standard consulting deliverables'
            ],
            'Client Impact': [
                'Maintained 15+ year consulting relationships across political, nonprofit, and technology sectors',
                'Delivered complex systems integrations and data platform solutions for enterprise clients',
                'Provided strategic planning resulting in measurable operational improvements and cost savings'
            ],
            'Methodological Innovation': [
                'Developed statistical methods for boundary estimation and geographic segmentation',
                'Created frameworks for comprehensive technology audits and modernization planning',
                'Established best practices for multi-tenant data architecture and security compliance'
            ]
        },

        '_metadata': {
            'version': 'consulting_minimal',
            'created': datetime.now().isoformat(),
            'description': 'Minimal consulting-focused version emphasizing strategic advisory and technical expertise'
        }
    }

    return data

def create_software_engineer_data():
    """Create software engineer focused version"""

    data = {
        'personal_info': {
            'name': 'DHEERAJ CHAND',
            'title': 'Senior Software Engineer & Geospatial Platform Architect',
            'phone': '(202) 550-7110',
            'email': 'Dheeraj.Chand@gmail.com',
            'website': 'https://www.dheerajchand.com',
            'linkedin': 'https://www.linkedin.com/in/dheerajchand/'
        },

        'summary': """Senior Software Engineer with 20+ years building scalable geospatial data platforms, web applications, and distributed analytical systems. Expert in full-stack development with deep specialization in Apache Spark/Sedona for big data geospatial processing. Proven track record architecting multi-tenant SaaS platforms like BALLISTA and DAMON used by thousands of analysts, implementing ETL pipelines processing billions of geospatial records, and building production systems integrating ESRI, OSGeo, and SAFE FME technologies. Strong background in both enterprise consulting and startup environments, with experience leading engineering teams and delivering mission-critical geospatial applications.""",

        'competencies': {
            'Programming & Development': [
                'Python: Django/GeoDjango, Flask, Pandas, PySpark, NumPy, SciKit-Learn',
                'JVM: Scala (Spark/Sedona), Java (GeoTools, enterprise applications), Groovy',
                'Web Technologies: JavaScript, React, d3.js, OpenLayers, jQuery, HTML/CSS',
                'Database Languages: SQL, T-SQL, PostgreSQL/PostGIS, Oracle, MySQL',
                'Statistical/Analysis: R, SPSS, NetLogo (agent-based modeling)'
            ],
            'Big Data & Geospatial Platforms': [
                'Apache Spark: PySpark, Spark SQL, Sedona (geospatial), distributed processing',
                'Geospatial Stack: PostGIS, ESRI ArcGIS, Quantum GIS, GRASS, OSGeo, SAFE FME',
                'Cloud Platforms: AWS (EC2, RDS, S3), Snowflake, Google Cloud, Microsoft Azure',
                'Data Engineering: ETL/ELT pipelines, dbt, Hadoop, Informatica, CDAP',
                'Databases: PostgreSQL/PostGIS, Oracle, MongoDB, Neo4j, MySQL'
            ],
            'Software Architecture & DevOps': [
                'Distributed Systems: Multi-tenant SaaS, microservices, API design, scalability',
                'Geospatial Applications: Spatial algorithms, boundary estimation, clustering analysis',
                'Web Applications: Full-stack development, RESTful APIs, real-time collaboration',
                'DevOps: Docker, Vagrant, CI/CD (GitLab, GitHub), Celery, Airflow, nginx',
                'Integration: Twilio API, WMS tile servers, CRM/DMP integration, OAuth'
            ]
        },

        'experience': [
            {
                'title': 'PARTNER & SENIOR SOFTWARE ENGINEER',
                'company': 'Siege Analytics, Austin, TX',
                'dates': '2005 – Present',
                'subtitle': 'Geospatial Platform Architecture and Full-Stack Development',
                'responsibilities': [
                    'Architected and engineered BALLISTA: GeoDjango redistricting platform serving thousands of analysts with real-time collaborative editing, Census integration, and legal compliance analysis',
                    'Developed DAMON: Flask/PostGIS microservice using incomplete data for boundary estimation without machine learning, processing geographies at national scale',
                    'Built scalable ETL pipelines using PySpark and Sedona processing billions of geospatial records with sub-hour latency requirements',
                    'Implemented advanced spatial clustering algorithms achieving 88% improvement in analytical targeting efficacy for political applications',
                    'Created fraud detection systems processing multi-terabyte campaign finance datasets with real-time alerting capabilities',
                    'Led technical architecture decisions integrating ESRI, OSGeo, and SAFE FME technologies for Fortune 500 and political clients'
                ]
            },
            {
                'title': 'DATA PRODUCTS MANAGER',
                'company': 'Helm/Murmuration, Austin, TX',
                'dates': '2021 – 2023',
                'subtitle': 'Enterprise Geospatial Data Platform Development and Team Leadership',
                'responsibilities': [
                    'Led engineering team of 11 developers building enterprise-scale geospatial data platform for political organizing and issue advocacy',
                    'Designed multi-tenant data warehouse integrating Census, Bureau of Labor Statistics, and National Council of Educational Statistics using Spark/PySpark',
                    'Modernized legacy ETL systems using Scala/Spark and dbt, achieving 57% performance improvement in geospatial data processing',
                    'Built comprehensive data governance framework with automated PostGIS quality validation and GRASS-based analysis pipelines',
                    'Trained analytical and engineering staff on OSGeo technologies (QGIS, GRASS) for geospatial analysis and visualization',
                    'Implemented Spark/Sedona pipelines for longitudinal analysis across demographic, economic, and geographical dimensions'
                ]
            },
            {
                'title': 'ANALYTICS SUPERVISOR',
                'company': 'GSD&M, Austin, TX',
                'dates': '2018 – 2019',
                'subtitle': 'Big Data Infrastructure and Geospatial Analytics Platform',
                'responsibilities': [
                    'Transformed small data team into big data engineering operation, migrating from desktop GIS to Hadoop/Spark clusters on AWS',
                    'Developed customer segmentation platform using Spark/PySpark with advanced spatial analysis and machine learning integration',
                    'Built real-time data visualization dashboards using React, d3.js, and OpenLayers for executive reporting and client presentations',
                    'Implemented version control workflows and Agile development practices improving team delivery timelines by 40%',
                    'Integrated ESRI ArcGIS Server with custom web applications for high-volume advertising and customer analytics workloads'
                ]
            },
            {
                'title': 'SOFTWARE ENGINEER',
                'company': 'Mautinoa Technologies, Austin, TX',
                'dates': '2016 – 2018',
                'subtitle': 'GeoDjango Platform Development and Multi-Agent Modeling',
                'responsibilities': [
                    'Conceived and engineered SimCrisis: GeoDjango web application with NetLogo multi-agent modeling for econometric crisis simulations',
                    'Implemented modular architecture supporting extensible rule systems for crisis scenario modeling and humanitarian intervention analysis',
                    'Built geospatial analysis tools using PostGIS and GRASS for population impact assessment and resource optimization',
                    'Collaborated with UNICEF and International Federation of Red Cross technical teams for requirements validation and deployment',
                    'Created RESTful APIs and React interfaces for complex simulation parameter configuration and geospatial results visualization'
                ]
            },
            {
                'title': 'SENIOR ANALYST & PLATFORM DEVELOPER',
                'company': 'Myers Research, Austin, TX',
                'dates': '2012 – 2014',
                'subtitle': 'Survey Platform Development and Geospatial Market Analysis',
                'responsibilities': [
                    'Co-developed RACSO: comprehensive GeoDjango web application for survey lifecycle management from instrument design to analysis',
                    'Implemented survey design tools, data collection interfaces, and automated reporting with integrated geospatial analysis capabilities',
                    'Built PostGIS-based market segmentation features enhancing demographic analysis with location-based consumer insights',
                    'Designed database schemas and PostGIS optimization strategies for large-scale survey data storage and spatial queries',
                    'Led RFP process analyzing 1,200+ vendor proposals for platform development, selecting optimal technology stack'
                ]
            },
            {
                'title': 'RESEARCH DIRECTOR & PLATFORM ARCHITECT',
                'company': 'Progressive Change Campaign Committee, Austin, TX',
                'dates': '2011 – 2012',
                'subtitle': 'Telephony Integration and Real-Time Survey Systems',
                'responsibilities': [
                    'Engineered FLEEM: GeoDjango platform integrating Twilio API for thousands of simultaneous IVR phone surveys with real-time processing',
                    'Developed statistical boundary estimation methods using PostGIS and GRASS, enhancing geographic targeting for political research',
                    'Implemented real-time data collection and processing systems with live result visualization using d3.js and OpenLayers',
                    'Built foundational polling consortium database infrastructure later adopted by The Analyst Institute',
                    'Created comprehensive geospatial data visualization solutions improving stakeholder understanding of complex research findings'
                ]
            }
        ],

        'achievements': {
            'Geospatial Platform Development': [
                'Architected BALLISTA redistricting platform used by thousands of analysts nationwide with real-time collaborative editing and Census integration',
                'Built DAMON boundary estimation system achieving accurate geospatial results without machine learning using advanced PostGIS algorithms',
                'Developed SimCrisis econometric simulation platform with NetLogo multi-agent modeling and GeoDjango web interface',
                'Created RACSO comprehensive survey platform managing complete research lifecycle with integrated geospatial market segmentation'
            ],
            'Big Data & Performance Engineering': [
                'Implemented Spark/Sedona ETL optimizations achieving 57% performance improvement in geospatial data processing pipelines',
                'Built systems processing billions of spatial records with sub-hour latency using distributed Spark clusters on AWS',
                'Developed fraud detection algorithms processing multi-terabyte campaign finance datasets with real-time PostGIS spatial analysis',
                'Created spatial clustering algorithms achieving 88% improvement in analytical targeting efficacy using custom PySpark implementations'
            ],
            'Technical Leadership & Integration': [
                'Led engineering teams up to 11 developers specializing in scalable geospatial architecture and OSGeo/ESRI technology integration',
                'Pioneered integration of ESRI, OSGeo (QGIS, GRASS), and SAFE FME technologies into production web applications',
                'Established technical standards for GeoDjango, PostGIS, and Spark/Sedona development across distributed teams',
                'Mentored developers in advanced geospatial software engineering, spatial algorithms, and big data processing principles'
            ]
        },

        '_metadata': {
            'version': 'software_engineer',
            'created': datetime.now().isoformat(),
            'description': 'Software engineer focused version emphasizing technical skills and platform development'
        }
    }

    return data

def create_config_file(version_name, primary_color='#228B22', secondary_color='#B8860B', accent_blue='#1F4E79'):
    """Create a config file for a resume version with green, gold, and blue branding"""

    config = {
        'PRIMARY_GREEN': '#228B22',        # Forest Green for name and primary accents
        'SECONDARY_GOLD': '#B8860B',       # Dark Goldenrod for section headers
        'ACCENT_BLUE': '#1F4E79',          # Professional Blue for job titles and highlights
        'LIGHT_GOLD': '#DAA520',           # Goldenrod for lighter accents
        'LIGHT_BLUE': '#4682B4',           # Steel Blue for secondary highlights
        'DARK_GRAY': '#333333',            # Main text
        'MEDIUM_GRAY': '#666666',          # Secondary text
        'LIGHT_GRAY': '#999999',           # Tertiary text

        'FONT_MAIN': 'Helvetica',
        'FONT_BOLD': 'Helvetica-Bold',
        'FONT_ITALIC': 'Helvetica-Oblique',

        'NAME_SIZE': 24,
        'TITLE_SIZE': 14,
        'SECTION_HEADER_SIZE': 12,
        'JOB_TITLE_SIZE': 11,
        'BODY_SIZE': 9,
        'CONTACT_SIZE': 9,

        'PAGE_MARGIN': 0.6,
        'SECTION_SPACING': 0.12,
        'PARAGRAPH_SPACING': 0.06,
        'LINE_SPACING': 1.15,
        'JOB_SPACING': 6,
        'CATEGORY_SPACING': 4,

        'MAX_PAGES': 2,
        'BULLET_CHAR': '▸',

        '_metadata': {
            'version': version_name,
            'created': datetime.now().isoformat(),
            'description': f'Configuration for {version_name} resume version with green, gold, and blue branding'
        }
    }

    return config

def save_resume_data(version_name, data, config):
    """Save resume data and config to appropriate directories"""

    input_dir = Path("inputs") / version_name
    input_dir.mkdir(parents=True, exist_ok=True)

    # Save resume data
    data_file = input_dir / "resume_data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save config
    config_file = input_dir / "config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {version_name}: {data_file} and {config_file}")

def create_generation_script():
    """Create a shell script to generate all resume versions"""

    script_content = '''#!/bin/bash

# Resume Generation Script
# Generates all resume versions using the ReportLab script

echo "🚀 Generating all resume versions..."
echo

# Array of resume versions
versions=(
    "dheeraj_research_focused"
    "dheeraj_technical_detailed"
    "dheeraj_comprehensive_full"
    "dheeraj_consulting_minimal"
    "dheeraj_software_engineer"
)

# Generate each version in all formats
for version in "${versions[@]}"; do
    echo "📄 Generating: $version"

    # Generate PDF
    python reportlab_resume.py --format pdf --basename "$version"

    # Generate DOCX
    python reportlab_resume.py --format docx --basename "$version"

    # Generate RTF
    python reportlab_resume.py --format rtf --basename "$version"

    echo "✅ Completed: $version"
    echo
done

echo "🎉 All resume versions generated successfully!"
echo
echo "📁 Find your resumes in:"
echo "   outputs/dheeraj_research_focused/"
echo "   outputs/dheeraj_technical_detailed/"
echo "   outputs/dheeraj_comprehensive_full/"
echo "   outputs/dheeraj_consulting_minimal/"
echo "   outputs/dheeraj_software_engineer/"
echo
echo "💡 Each directory contains PDF, DOCX, and RTF versions"
'''

    script_file = Path("generate_all_resumes.sh")
    with open(script_file, 'w') as f:
        f.write(script_content)

    # Make script executable
    import stat
    script_file.chmod(script_file.stat().st_mode | stat.S_IEXEC)

    print(f"✅ Created generation script: {script_file}")

def main():
    """Main function to generate all resume data files"""

    print("🚀 Resume Data Generator")
    print("=" * 50)

    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()

    # Create all resume versions
    print("\n📝 Creating resume data files...")

    # All versions now use consistent green, gold, and blue branding

    # Research-focused version (Green, Gold, Blue)
    research_data = create_research_focused_data()
    research_config = create_config_file("research_focused")
    save_resume_data("dheeraj_research_focused", research_data, research_config)

    # Technical detailed version (Green, Gold, Blue)
    technical_data = create_technical_detailed_data()
    technical_config = create_config_file("technical_detailed")
    save_resume_data("dheeraj_technical_detailed", technical_data, technical_config)

    # Comprehensive full version (Green, Gold, Blue)
    comprehensive_data = create_comprehensive_full_data()
    comprehensive_config = create_config_file("comprehensive_full")
    save_resume_data("dheeraj_comprehensive_full", comprehensive_data, comprehensive_config)

    # Consulting minimal version (Green, Gold, Blue)
    consulting_data = create_consulting_minimal_data()
    consulting_config = create_config_file("consulting_minimal")
    save_resume_data("dheeraj_consulting_minimal", consulting_data, consulting_config)

    # Software engineer version (Green, Gold, Blue)
    engineer_data = create_software_engineer_data()
    engineer_config = create_config_file("software_engineer")
    save_resume_data("dheeraj_software_engineer", engineer_data, engineer_config)

    # Create generation script
    print("\n🔧 Creating generation script...")
    create_generation_script()

    print("\n✅ Resume data generation complete!")
    print("\n📋 Generated versions:")
    print("   • dheeraj_research_focused    - Emphasizes applied research leadership")
    print("   • dheeraj_technical_detailed  - Shows engineering depth and technical skills")
    print("   • dheeraj_comprehensive_full  - Complete work history with all details")
    print("   • dheeraj_consulting_minimal  - Consulting-focused strategic advisor")
    print("   • dheeraj_software_engineer   - Software engineering and platform development")
    print("\n🚀 Next steps:")
    print("   1. Review the generated JSON files in inputs/ directories")
    print("   2. Customize any content or styling as needed")
    print("   3. Run: ./generate_all_resumes.sh")
    print("   4. Or generate individual versions:")
    print("      python reportlab_resume.py --format all --basename dheeraj_research_focused")

if __name__ == "__main__":
    main()
