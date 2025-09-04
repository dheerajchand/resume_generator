#!/usr/bin/env python3
"""
Resume Data Generator for ReportLab Script
Creates structured JSON input files for multiple resume versions with flexible color schemes
Now supports generic user configuration!
"""

import json
from pathlib import Path
from datetime import datetime
import argparse
import sys
from user_config import UserConfig


# Abstract Color System Classes
class ColorScheme:
    """Abstract color scheme with role-based colors"""

    def __init__(self, scheme_name="default"):
        self.scheme_name = scheme_name

        # Abstract color roles (these stay the same)
        self.roles = {
            "NAME_COLOR": "#228B22",  # Color for name header
            "TITLE_COLOR": "#B8860B",  # Color for professional title
            "SECTION_HEADER_COLOR": "#B8860B",  # Color for section headers
            "JOB_TITLE_COLOR": "#722F37",  # Color for job titles
            "ACCENT_COLOR": "#722F37",  # Color for highlights/accents
            "COMPETENCY_HEADER_COLOR": "#228B22",  # Color for competency categories
            "SUBTITLE_COLOR": "#228B22",  # Color for job subtitles
            "LINK_COLOR": "#B8860B",  # Color for links
            "LIGHT_ACCENT_COLOR": "#8B4444",  # Lighter version of accent
            "LIGHT_SECONDARY_COLOR": "#DAA520",  # Lighter version of secondary
            # Text colors (usually stay consistent)
            "DARK_TEXT_COLOR": "#333333",  # Main body text
            "MEDIUM_TEXT_COLOR": "#666666",  # Secondary text
            "LIGHT_TEXT_COLOR": "#999999",  # Tertiary text
        }

        # Typography and layout (role-based)
        self.typography = {
            "FONT_MAIN": "Helvetica",
            "FONT_BOLD": "Helvetica-Bold",
            "FONT_ITALIC": "Helvetica-Oblique",
            "NAME_SIZE": 24,
            "TITLE_SIZE": 14,
            "SECTION_HEADER_SIZE": 12,
            "JOB_TITLE_SIZE": 11,
            "BODY_SIZE": 9,
            "CONTACT_SIZE": 9,
        }

        self.layout = {
            "PAGE_MARGIN": 0.6,
            "SECTION_SPACING": 0.12,
            "PARAGRAPH_SPACING": 0.06,
            "LINE_SPACING": 1.15,
            "JOB_SPACING": 6,
            "CATEGORY_SPACING": 4,
            "MAX_PAGES": 2,
            "BULLET_CHAR": "▸",
        }

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        config = {}
        config.update(self.roles)
        config.update(self.typography)
        config.update(self.layout)
        config["_metadata"] = {
            "scheme_name": self.scheme_name,
            "created": datetime.now().isoformat(),
            "description": f"{self.scheme_name} color scheme for professional resume",
        }
        return config

    def save_to_file(self, filepath):
        """Save ColorScheme to JSON file"""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def from_dict(cls, data):
        """Create ColorScheme from dictionary"""
        scheme = cls(data.get("scheme_name", "custom"))
        scheme.roles.update(data.get("colors", {}))
        scheme.typography.update(data.get("typography", {}))
        scheme.layout.update(data.get("layout", {}))
        return scheme

    @classmethod
    def from_file(cls, filepath):
        """Load ColorScheme from JSON file"""
        with open(filepath, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)


class PredefinedSchemes:
    """Collection of predefined color schemes"""

    @staticmethod
    def default_professional():
        """Green, Gold, Burgundy - Professional and distinctive"""
        scheme = ColorScheme("default_professional")
        scheme.roles.update(
            {
                "NAME_COLOR": "#228B22",  # Forest Green
                "TITLE_COLOR": "#B8860B",  # Dark Goldenrod
                "SECTION_HEADER_COLOR": "#B8860B",  # Dark Goldenrod
                "JOB_TITLE_COLOR": "#722F37",  # Deep Burgundy
                "ACCENT_COLOR": "#722F37",  # Deep Burgundy
                "COMPETENCY_HEADER_COLOR": "#228B22",  # Forest Green
                "SUBTITLE_COLOR": "#228B22",  # Forest Green
                "LINK_COLOR": "#B8860B",  # Dark Goldenrod
                "LIGHT_ACCENT_COLOR": "#8B4444",  # Light Burgundy
                "LIGHT_SECONDARY_COLOR": "#DAA520",  # Goldenrod
            }
        )
        return scheme

    @staticmethod
    def corporate_blue():
        """Navy, Gray, Steel Blue - Corporate conservative"""
        scheme = ColorScheme("corporate_blue")
        scheme.roles.update(
            {
                "NAME_COLOR": "#1F4E79",  # Navy Blue
                "TITLE_COLOR": "#333333",  # Charcoal
                "SECTION_HEADER_COLOR": "#333333",  # Charcoal
                "JOB_TITLE_COLOR": "#4682B4",  # Steel Blue
                "ACCENT_COLOR": "#4682B4",  # Steel Blue
                "COMPETENCY_HEADER_COLOR": "#1F4E79",  # Navy Blue
                "SUBTITLE_COLOR": "#1F4E79",  # Navy Blue
                "LINK_COLOR": "#4682B4",  # Steel Blue
                "LIGHT_ACCENT_COLOR": "#6495ED",  # Cornflower Blue
                "LIGHT_SECONDARY_COLOR": "#666666",  # Medium Gray
            }
        )
        return scheme

    @staticmethod
    def modern_tech():
        """Teal, Orange, Gray - Modern tech company feel"""
        scheme = ColorScheme("modern_tech")
        scheme.roles.update(
            {
                "NAME_COLOR": "#2C5F5D",  # Deep Teal
                "TITLE_COLOR": "#FF6B35",  # Vibrant Orange
                "SECTION_HEADER_COLOR": "#FF6B35",  # Vibrant Orange
                "JOB_TITLE_COLOR": "#2C5F5D",  # Deep Teal
                "ACCENT_COLOR": "#FF6B35",  # Vibrant Orange
                "COMPETENCY_HEADER_COLOR": "#2C5F5D",  # Deep Teal
                "SUBTITLE_COLOR": "#2C5F5D",  # Deep Teal
                "LINK_COLOR": "#FF6B35",  # Vibrant Orange
                "LIGHT_ACCENT_COLOR": "#FF8C69",  # Light Orange
                "LIGHT_SECONDARY_COLOR": "#5F9EA0",  # Cadet Blue
            }
        )
        return scheme

    @classmethod
    def load_custom_scheme(cls, scheme_name):
        """Load a custom color scheme from JSON file"""
        scheme_file = Path("color_schemes") / f"{scheme_name}.json"

        if not scheme_file.exists():
            raise ValueError(f"Custom color scheme file not found: {scheme_file}")

        try:
            with open(scheme_file, "r") as f:
                data = json.load(f)

            scheme = ColorScheme(scheme_name)

            # Load colors from the JSON file
            if "_metadata" in data and "scheme_name" in data["_metadata"]:
                actual_name = data["_metadata"]["scheme_name"]
            else:
                actual_name = scheme_name

            # Update colors from JSON file (handle flattened structure from color_scheme_generator_tool.py)
            color_keys = [k for k in data.keys() if k.endswith("_COLOR")]
            for color_key in color_keys:
                if color_key in data:
                    scheme.roles[color_key] = data[color_key]

            # Update typography and layout if present
            typography_keys = [
                "FONT_MAIN",
                "FONT_BOLD",
                "FONT_ITALIC",
                "NAME_SIZE",
                "TITLE_SIZE",
                "SECTION_HEADER_SIZE",
                "JOB_TITLE_SIZE",
                "BODY_SIZE",
                "CONTACT_SIZE",
            ]
            for typo_key in typography_keys:
                if typo_key in data:
                    scheme.typography[typo_key] = data[typo_key]

            layout_keys = [
                "PAGE_MARGIN",
                "SECTION_SPACING",
                "PARAGRAPH_SPACING",
                "LINE_SPACING",
                "JOB_SPACING",
                "CATEGORY_SPACING",
                "MAX_PAGES",
                "BULLET_CHAR",
            ]
            for layout_key in layout_keys:
                if layout_key in data:
                    scheme.layout[layout_key] = data[layout_key]

            scheme.scheme_name = actual_name
            return scheme

        except Exception as e:
            raise ValueError(f"Error loading custom color scheme '{scheme_name}': {e}")


def create_directory_structure(user_config):
    """Create the directory structure for all resume versions"""

    resume_versions = [
        user_config.get_version_directory_name("research"),
        user_config.get_version_directory_name("technical"),
        user_config.get_version_directory_name("comprehensive"),
        user_config.get_version_directory_name("consulting"),
        user_config.get_version_directory_name("software"),
        user_config.get_version_directory_name("marketing"),
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


def create_config_file(user_config, version_name, color_scheme=None):
    """Create a config file for a resume version using color scheme"""
    if color_scheme is None:
        color_scheme = PredefinedSchemes.default_professional()

    config = {}

    # Check if this is a custom scheme name (string) that needs to be loaded
    if isinstance(color_scheme, str):
        try:
            # Try to load as custom scheme first
            color_scheme = PredefinedSchemes.load_custom_scheme(color_scheme)
        except ValueError:
            # Fall back to predefined schemes
            if color_scheme == "default_professional":
                color_scheme = PredefinedSchemes.default_professional()
            elif color_scheme == "corporate_blue":
                color_scheme = PredefinedSchemes.corporate_blue()
            elif color_scheme == "modern_tech":
                color_scheme = PredefinedSchemes.modern_tech()
            else:
                print(
                    f"⚠️  Unknown color scheme '{color_scheme}', using default_professional"
                )
                color_scheme = PredefinedSchemes.default_professional()

    # Map color scheme to config
    if hasattr(color_scheme, "roles"):
        config.update(color_scheme.roles)
    if hasattr(color_scheme, "typography"):
        config.update(color_scheme.typography)
    if hasattr(color_scheme, "layout"):
        config.update(color_scheme.layout)

    config["_metadata"] = {
        "version": version_name,
        "scheme_name": color_scheme.scheme_name,
        "user": user_config.name,
        "created": datetime.now().isoformat(),
        "description": f"Configuration for {version_name} using {color_scheme.scheme_name} color scheme",
    }

    return config


def create_color_scheme_files():
    """Create predefined color scheme files"""
    schemes_dir = Path("color_schemes")
    schemes_dir.mkdir(exist_ok=True)

    schemes = {
        "default_professional.json": PredefinedSchemes.default_professional(),
        "corporate_blue.json": PredefinedSchemes.corporate_blue(),
        "modern_tech.json": PredefinedSchemes.modern_tech(),
    }

    for filename, scheme in schemes.items():
        filepath = schemes_dir / filename
        scheme.save_to_file(filepath)
        print(f"✅ Created color scheme: {filepath}")

    return schemes_dir


# All the resume data creation functions - now they take user_config as parameter
def create_research_focused_data(user_config):
    """Create data for research-focused version"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Research and Data Analytics Leader with {user_config.config['resume_content']['years_experience']} years of experience directing applied research projects from conception to completion focused on economic mobility, community development, and social impact. Proven track record of leading cross-functional teams, translating complex research insights for diverse stakeholders including elected officials and community organizations, and implementing evidence-based solutions that drive meaningful outcomes. Expert in research methodology design, statistical analysis, and community partnership development with extensive experience serving vulnerable populations and addressing systemic poverty challenges.""",
        "competencies": {
            "Applied Research Leadership": [
                "Applied Research Project Management (Conception to Completion)",
                "Research Methodology Design and Implementation",
                "Cross-functional Team Leadership and Mentoring",
                "Stakeholder Communication and Translation of Complex Findings",
                "Evidence-Based Framework Development",
                "Survey Methodology and Consumer Insights",
                "Statistical Analysis and Data Validation",
            ],
            "Technical Proficiency": [
                "Programming: Python (Pandas, SciKit, TensorFlow, Django), R, SQL, Scala",
                "Data Platforms: PostgreSQL, MySQL, Snowflake, Spark, MongoDB, Oracle",
                "Analysis Tools: Excel (Advanced), Tableau, PowerBI, SPSS, SAS",
                "Research Tools: Survey Design, Sampling Methodology, Statistical Modeling",
                "Geospatial Analysis: ESRI ArcGIS, Quantum GIS, PostGIS, OSGeo",
            ],
            "Strategic Operations": [
                "Community Partnership Development",
                "Government Relations and Policy Analysis",
                "Multi-million Dollar Project Management",
                "Performance Measurement and Evaluation",
                "Data-Driven Decision Making for Social Impact",
                "Public Systems Integration",
                "Stakeholder Briefing and Expert Testimony",
            ],
        },
        "experience": [
            {
                "title": "PARTNER",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Leading Applied Research Projects with Community Development Focus",
                "responsibilities": [
                    "Direct comprehensive applied research projects from conception to completion for organizations focused on economic mobility and community development",
                    "Lead multi-million dollar research initiatives involving sensitive demographic and economic data addressing poverty and community health challenges",
                    "Translate complex research findings for diverse stakeholder groups including elected officials, NGO leadership, and community organizations",
                    "Collaborate with government agencies and research institutions to develop evidence-based solutions addressing systemic poverty",
                    "Manage client relationships across public sector and nonprofit organizations, consistently delivering research that drives strategic decision-making",
                    "Develop custom analytical tools processing billions of records to identify patterns in economic mobility and demographic trends",
                ],
            }
        ],
        "achievements": {
            "Research Leadership and Community Impact": [
                "Regular expert testimony and consultation on research methodology for journalists, elected officials, and community leaders",
                "Research analysis used in court cases addressing housing, redistricting, and community development with rigorous methodology",
                "Conceived and deployed cloud-based analytical software used by thousands of researchers nationwide for community-focused research",
            ]
        },
        "_metadata": {
            "version": "research_focused",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Research-focused version emphasizing applied research leadership and community impact",
        },
    }

    return data


def create_technical_detailed_data(user_config):
    """Create data for technical detailed version"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Senior Data Engineer with {user_config.config['resume_content']['years_experience']} years of expertise in geospatial data platforms, big data processing, and distributed systems architecture. Deep specialist in Apache Spark/Sedona for large-scale geospatial analytics, with fluency across ESRI, OSGeo, and SAFE FME technology stacks. Proven track record architecting production systems serving thousands of users, implementing PySpark pipelines processing billions of spatial records, and leading engineering teams. Expert in full-stack geospatial development from PostGIS database optimization to React-based mapping interfaces.""",
        "competencies": {
            "Big Data & Geospatial Processing": [
                "Apache Spark: PySpark, Spark SQL, Scala Spark, Sedona (geospatial), distributed processing",
                "Geospatial Databases: PostGIS (advanced), Oracle Spatial, spatial indexing, query optimization",
                "ETL/ELT: dbt, Informatica, CDAP, custom PySpark pipelines, data governance frameworks",
                "Cloud Platforms: AWS (EC2, RDS, S3), Snowflake, Hadoop clusters, distributed computing",
                "Streaming: Real-time data processing, Kafka integration, event-driven architectures",
            ],
            "GIS Technology Stack": [
                "ESRI: ArcGIS Server, ArcGIS Pro, enterprise geodatabases, ModelBuilder, ArcPy scripting",
                "OSGeo: QGIS, GRASS GIS, GDAL/OGR, GeoServer, spatial analysis workflows",
                "SAFE FME: Data transformation, format conversion, spatial ETL, enterprise integration",
                "Web Mapping: OpenLayers, Leaflet, MapBox, tile servers, WMS/WFS services",
                "Spatial Analysis: Clustering algorithms, boundary estimation, network analysis, geostatistics",
            ],
            "Software Development & Architecture": [
                "Python: Django/GeoDjango, Flask, Pandas, NumPy, SciKit-Learn, spatial libraries",
                "JVM: Scala (Spark), Java (GeoTools, enterprise), Groovy scripting",
                "Web Technologies: React, JavaScript, d3.js, RESTful APIs, microservices",
                "Databases: PostgreSQL/PostGIS, Oracle, MySQL, MongoDB, spatial optimization",
                "DevOps: Docker, Kubernetes, CI/CD (GitLab, GitHub), Airflow, Celery, nginx",
            ],
        },
        "experience": [
            {
                "title": "PARTNER & SENIOR DATA ARCHITECT",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Geospatial Data Platform Architecture and Big Data Engineering",
                "responsibilities": [
                    "Architected and engineered production geospatial platforms serving thousands of analysts",
                    "Built enterprise-scale ETL pipelines using PySpark and Sedona processing billions of geospatial records with advanced spatial clustering algorithms",
                    "Developed multi-tenant data warehouse integrating Census, electoral, and demographic data using PostGIS and Spark SQL optimization",
                    "Implemented fraud detection systems processing multi-terabyte datasets with real-time spatial analysis capabilities",
                    "Created parametric boundary estimation algorithms using PostGIS and GRASS without machine learning dependencies",
                    "Led integration of ESRI ArcGIS Server, OSGeo tools (QGIS, GRASS), and SAFE FME for enterprise geospatial workflows",
                ],
            }
        ],
        "achievements": {
            "Geospatial Platform Engineering": [
                "Architected redistricting platform processing Census data for thousands of analysts with real-time PostGIS collaborative editing",
                "Built boundary estimation system using advanced PostGIS algorithms and incomplete data without machine learning requirements",
                "Developed geospatial simulation platform integrating multi-agent modeling with web interface",
            ]
        },
        "_metadata": {
            "version": "technical_detailed",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Technical version emphasizing engineering skills, data architecture, and platform development",
        },
    }

    return data


def create_comprehensive_full_data(user_config):
    """Create comprehensive version with complete work history"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Research & Data Professional with {user_config.config['resume_content']['years_experience']} years of comprehensive experience spanning applied research, data engineering, and software development. Expert in translating complex analytical requirements into scalable technical solutions. Proven track record leading cross-functional teams, architecting data platforms, and delivering insights that drive strategic decision-making across political, nonprofit, and technology sectors. Deep expertise in survey methodology, geospatial analysis, and building production systems for sensitive data applications.""",
        "competencies": {
            "Research and Analytics": [
                "Survey Methodology: Design, sampling, weighting, longitudinal analysis",
                "Statistical Analysis: Regression modeling, clustering, segmentation, machine learning",
                "Geospatial Analysis: Spatial clustering, boundary estimation, demographic mapping",
                "Data Visualization: Tableau, PowerBI, d3.js, Matplotlib, Seaborn, choropleth mapping",
                "Research Management: Team leadership, methodology design, stakeholder communication",
            ],
            "Programming and Development": [
                "Python: Django/GeoDjango, Flask, Pandas, PySpark, SciKit-Learn, TensorFlow",
                "JVM Languages: Scala (Spark), Java, Groovy",
                "Web Technologies: JavaScript, React, d3.js, PHP, HTML/CSS",
                "Database Languages: SQL, T-SQL, PostgreSQL/PostGIS",
                "Statistical Computing: R, SPSS, SAS, Stata",
            ],
            "Data Infrastructure": [
                "Cloud Platforms: AWS (EC2, RDS, S3), Google Cloud Platform, Microsoft Azure",
                "Big Data: Apache Spark, PySpark, Hadoop, Snowflake, dbt",
                "Databases: PostgreSQL/PostGIS, MySQL, Oracle, MongoDB, Neo4j",
                "Geospatial: ESRI ArcGIS, Quantum GIS, GeoServer, OSGeo, GRASS",
                "DevOps: Docker, Git, CI/CD pipelines, automated testing, version control",
            ],
        },
        "experience": [
            {
                "title": "PARTNER",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Data, Technology and Strategy Consulting",
                "responsibilities": [
                    "Conduct comprehensive quantitative and qualitative research studies for political candidates and organizations",
                    "Architect cloud-based data warehouse solutions processing billions of records for electoral analytics",
                    "Design scalable ETL pipelines using PySpark and dbt for large-scale geospatial and demographic datasets",
                    "Develop custom analytical tools and algorithms for fraud detection and spatial clustering",
                    "Manage complex client relationships across political, nonprofit, and technology sectors",
                    "Lead technical architecture decisions for data-intensive applications and platforms",
                ],
            }
        ],
        "achievements": {
            "Software Development and Innovation": [
                "Conceived and deployed redistricting software used by thousands of analysts nationwide",
                "Developed boundary estimation system using incomplete data without ML requirements",
                "Created econometric simulation platform for humanitarian intervention modeling",
                "Built comprehensive survey operations platform from RFP through deployment",
            ]
        },
        "_metadata": {
            "version": "comprehensive_full",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Comprehensive version with complete work history and technical depth",
        },
    }

    return data


def create_consulting_minimal_data(user_config):
    """Create minimal consulting-focused version"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Strategic data and technology consultant with {user_config.config['resume_content']['years_experience']} years solving complex problems through analytics and software development. Specializes in transforming organizational data capabilities from concept to production. Expert in translating business requirements into technical solutions, with proven success across political, nonprofit, and technology sectors. Currently building scalable data platforms while modernizing legacy systems for improved performance and maintainability.""",
        "competencies": {
            "Consulting Expertise": [
                "Strategic Data Analysis (Exploratory, Predictive, Explanatory)",
                "Data Engineering and Infrastructure Development",
                "Systems Integration and Architecture Consulting",
                "Project Management and Product Management",
                "Team Leadership and Technical Mentoring",
                "Stakeholder Communication and Requirements Gathering",
            ],
            "Technical Solutions": [
                "Programming: Python (Django, Pandas, PySpark), Scala (Spark), JavaScript",
                "Data Platforms: PostgreSQL/PostGIS, Snowflake, MongoDB, AWS, GCP",
                "Analytics: Tableau, PowerBI, Statistical Modeling, Machine Learning",
                "Integration: APIs, ETL/ELT pipelines, Cloud migrations, Legacy modernization",
            ],
            "Industry Focus": [
                "Political and Electoral Data Analytics",
                "Nonprofit and Community Organization Solutions",
                "Technology Startup and Scale-up Consulting",
                "Geospatial Analysis and Demographic Intelligence",
                "Survey Research and Consumer Behavior Analysis",
            ],
        },
        "experience": [
            {
                "title": "PRINCIPAL CONSULTANT",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Data, Technology and Strategy Consulting",
                "responsibilities": [
                    "Provide comprehensive data analysis, engineering, and strategic planning for diverse client portfolio",
                    "Develop custom software solutions and data pipeline architectures for complex integration requirements",
                    "Lead digital transformation initiatives including cloud migrations and legacy system modernization",
                    "Deliver management consulting including project planning, team building, and operational optimization",
                    "Maintain long-term strategic partnerships with clients across political, nonprofit, and technology sectors",
                ],
            }
        ],
        "achievements": {
            "Technology Innovation": [
                "Developed proprietary B2B SaaS solutions for data analytics and geospatial applications",
                "Created open source frameworks for political and social behavior prediction",
                "Pioneered integration of advanced mapping techniques into standard consulting deliverables",
            ]
        },
        "_metadata": {
            "version": "consulting_minimal",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Minimal consulting-focused version emphasizing strategic advisory and technical expertise",
        },
    }

    return data


def create_software_engineer_data(user_config):
    """Create software engineer focused version"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Senior Software Engineer with {user_config.config['resume_content']['years_experience']} years building scalable geospatial data platforms, web applications, and distributed analytical systems. Expert in full-stack development with deep specialization in Apache Spark/Sedona for big data geospatial processing. Proven track record architecting multi-tenant SaaS platforms used by thousands of analysts, implementing ETL pipelines processing billions of geospatial records, and building production systems integrating ESRI, OSGeo, and SAFE FME technologies. Strong background in both enterprise consulting and startup environments, with experience leading engineering teams and delivering mission-critical geospatial applications.""",
        "competencies": {
            "Programming & Development": [
                "Python: Django/GeoDjango, Flask, Pandas, PySpark, NumPy, SciKit-Learn",
                "JVM: Scala (Spark/Sedona), Java (GeoTools, enterprise applications), Groovy",
                "Web Technologies: JavaScript, React, d3.js, OpenLayers, jQuery, HTML/CSS",
                "Database Languages: SQL, T-SQL, PostgreSQL/PostGIS, Oracle, MySQL",
                "Statistical/Analysis: R, SPSS, NetLogo (agent-based modeling)",
            ],
            "Big Data & Geospatial Platforms": [
                "Apache Spark: PySpark, Spark SQL, Sedona (geospatial), distributed processing",
                "Geospatial Stack: PostGIS, ESRI ArcGIS, Quantum GIS, GRASS, OSGeo, SAFE FME",
                "Cloud Platforms: AWS (EC2, RDS, S3), Snowflake, Google Cloud, Microsoft Azure",
                "Data Engineering: ETL/ELT pipelines, dbt, Hadoop, Informatica, CDAP",
                "Databases: PostgreSQL/PostGIS, Oracle, MongoDB, Neo4j, MySQL",
            ],
            "Software Architecture & DevOps": [
                "Distributed Systems: Multi-tenant SaaS, microservices, API design, scalability",
                "Geospatial Applications: Spatial algorithms, boundary estimation, clustering analysis",
                "Web Applications: Full-stack development, RESTful APIs, real-time collaboration",
                "DevOps: Docker, Vagrant, CI/CD (GitLab, GitHub), Celery, Airflow, nginx",
                "Integration: Twilio API, WMS tile servers, CRM/DMP integration, OAuth",
            ],
        },
        "experience": [
            {
                "title": "PARTNER & SENIOR SOFTWARE ENGINEER",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Geospatial Platform Architecture and Full-Stack Development",
                "responsibilities": [
                    "Architected and engineered redistricting platform serving thousands of analysts with real-time collaborative editing, Census integration, and legal compliance analysis",
                    "Developed boundary estimation microservice using incomplete data for boundary estimation without machine learning, processing geographies at national scale",
                    "Built scalable ETL pipelines using PySpark and Sedona processing billions of geospatial records with sub-hour latency requirements",
                    "Implemented advanced spatial clustering algorithms achieving 88% improvement in analytical targeting efficacy for political applications",
                    "Created fraud detection systems processing multi-terabyte campaign finance datasets with real-time alerting capabilities",
                    "Led technical architecture decisions integrating ESRI, OSGeo, and SAFE FME technologies for Fortune 500 and political clients",
                ],
            }
        ],
        "achievements": {
            "Geospatial Platform Development": [
                "Architected redistricting platform used by thousands of analysts nationwide with real-time collaborative editing and Census integration",
                "Built boundary estimation system achieving accurate geospatial results without machine learning using advanced PostGIS algorithms",
                "Developed econometric simulation platform with NetLogo multi-agent modeling and web interface",
                "Created comprehensive survey platform managing complete research lifecycle with integrated geospatial market segmentation",
            ]
        },
        "_metadata": {
            "version": "software_engineer",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Software engineer focused version emphasizing technical skills and platform development",
        },
    }

    return data


def create_product_marketing_data(user_config):
    """Create data for product marketing focused version"""

    data = {
        "personal_info": user_config.get_personal_info(),
        "summary": f"""Results-driven Product Marketing professional with {user_config.config['resume_content']['years_experience']} years of experience translating complex data insights into compelling market strategies and customer narratives. Expert in market intelligence, competitive analysis, and data-driven positioning with proven success leading cross-functional teams and launching B2B SaaS platforms used by thousands of users. Deep expertise in survey methodology, customer segmentation, and go-to-market strategy development. Skilled at turning complex technical concepts into clear, actionable messaging that drives customer adoption and business growth across political, technology, and consulting sectors.""",
        "competencies": {
            "Product Marketing Core": [
                "Market Intelligence & Competitive Analysis",
                "Product Positioning & Messaging Development",
                "Go-to-Market Strategy & Product Launch Management",
                "Customer Segmentation & Buyer Persona Development",
                "Cross-functional Team Leadership & Collaboration",
                "Sales Enablement & Training Material Development",
                "Data-Driven Decision Making & Analytics Interpretation",
            ],
            "Research & Analytics": [
                "Survey Methodology & Customer Insights",
                "Market Research Design & Implementation",
                "Competitive Intelligence & SWOT Analysis",
                "Customer Journey Mapping & Behavioral Analysis",
                "Statistical Modeling & Trend Analysis",
                "Performance Metrics & Dashboard Development",
                "A/B Testing & Conversion Optimization",
            ],
            "Communication & Technology": [
                "Strategic Messaging & Narrative Development",
                "Stakeholder Communication & Executive Briefings",
                "Content Creation: Case Studies, Battle Cards, Playbooks",
                "B2B SaaS Platform Experience & Technical Acumen",
                "CRM/Marketing Automation (Salesforce, HubSpot)",
                "Data Visualization (Tableau, PowerBI, D3.js)",
                "AI/ML Tools Integration & Marketing Technology Stack",
            ],
        },
        "experience": [
            {
                "title": "PARTNER & STRATEGIC CONSULTANT",
                "company": "Your Company Name, Your City, ST",
                "dates": "2005 – Present",
                "subtitle": "Market Research, Product Strategy & Go-to-Market Leadership",
                "responsibilities": [
                    "Led comprehensive market intelligence and competitive analysis projects for B2B technology platforms, delivering actionable insights that shaped product positioning and messaging strategies",
                    "Developed and executed go-to-market strategies for multiple SaaS platform launches, achieving thousands of active users and significant market penetration",
                    "Created compelling product narratives and value propositions that translated complex technical capabilities into clear customer benefits, resulting in improved adoption rates and customer engagement",
                    "Conducted extensive customer research and segmentation analysis using survey methodology and behavioral data to develop targeted buyer personas and messaging frameworks",
                    "Collaborated with cross-functional teams including engineering, sales, and customer success to align product strategy with market demands and customer feedback",
                    "Built comprehensive competitive intelligence frameworks analyzing market trends, pricing strategies, and feature differentiation across political technology and data analytics sectors",
                ],
            }
        ],
        "achievements": {
            "Product Marketing & Launch Success": [
                "Successfully launched multiple B2B SaaS platforms used by thousands of active users with proven market adoption and customer retention",
                "Developed comprehensive go-to-market strategies resulting in measurable increases in customer acquisition, engagement, and platform utilization across diverse market segments",
                "Created compelling product narratives and messaging frameworks that effectively translated complex technical capabilities into clear customer value propositions",
            ]
        },
        "_metadata": {
            "version": "product_marketing",
            "user": user_config.name,
            "created": datetime.now().isoformat(),
            "description": "Product marketing focused version emphasizing market research, go-to-market strategy, and customer insights",
        },
    }

    return data


def save_resume_data(user_config, version_name, data, config):
    """Save resume data and config to appropriate directories"""

    input_dir = Path("inputs") / user_config.get_version_directory_name(version_name)
    input_dir.mkdir(parents=True, exist_ok=True)

    # Save resume data
    data_file = input_dir / "resume_data.json"
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save config
    config_file = input_dir / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"✅ Saved {version_name}: {data_file} and {config_file}")


def main():
    """Main function to generate all resume data files"""
    parser = argparse.ArgumentParser(
        description="Generate resume data with flexible color schemes",
        epilog="""
Examples:
  python resume_data_generator.py --generate-data
  python resume_data_generator.py --generate-data --color-scheme corporate_blue
  python resume_data_generator.py --color-scheme modern_tech
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--generate-data",
        action="store_true",
        help="Generate resume data files (recommended for direct usage)",
    )
    parser.add_argument(
        "--color-scheme",
        default="default_professional",
        help="Color scheme to use (built-in: default_professional, corporate_blue, modern_tech, or custom scheme name)",
    )

    args = parser.parse_args()

    # If no arguments provided, show help
    if len(sys.argv) == 1:
        parser.print_help()
        return 0

    # The script runs if --generate-data is specified OR if --color-scheme is provided
    # This maintains compatibility with both direct usage and resume_manager.py calls

    print("🚀 Resume Data Generator")
    print("=" * 50)

    # Load user configuration
    try:
        user_config = UserConfig()
        print(f"👤 Loaded configuration for: {user_config.name}")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("\n🔧 Run 'python setup_user.py' to create your configuration first!")
        return 1
    except Exception as e:
        print(f"❌ Error loading user configuration: {e}")
        return 1

    # Validate configuration
    try:
        user_config.validate_config()
    except ValueError as e:
        print(f"❌ {e}")
        return 1

    # Create color scheme files first
    print("\n🎨 Creating color scheme files...")
    create_color_scheme_files()

    # Select color scheme - handle both built-in and custom schemes
    print(f"\n🎨 Using color scheme: {args.color_scheme}")

    # The create_config_file function will handle loading custom schemes
    color_scheme_name = args.color_scheme

    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure(user_config)

    # Create all resume versions with the specified color scheme
    print(f"\n📝 Creating resume data files with {color_scheme_name} color scheme...")

    # Research-focused version
    research_data = create_research_focused_data(user_config)
    research_config = create_config_file(
        user_config, "research_focused", color_scheme_name
    )
    save_resume_data(user_config, "research", research_data, research_config)

    # Technical detailed version
    technical_data = create_technical_detailed_data(user_config)
    technical_config = create_config_file(
        user_config, "technical_detailed", color_scheme_name
    )
    save_resume_data(user_config, "technical", technical_data, technical_config)

    # Comprehensive full version
    comprehensive_data = create_comprehensive_full_data(user_config)
    comprehensive_config = create_config_file(
        user_config, "comprehensive_full", color_scheme_name
    )
    save_resume_data(
        user_config, "comprehensive", comprehensive_data, comprehensive_config
    )

    # Consulting minimal version
    consulting_data = create_consulting_minimal_data(user_config)
    consulting_config = create_config_file(
        user_config, "consulting_minimal", color_scheme_name
    )
    save_resume_data(user_config, "consulting", consulting_data, consulting_config)

    # Software engineer version (DEFAULT)
    engineer_data = create_software_engineer_data(user_config)
    engineer_config = create_config_file(
        user_config, "software_engineer", color_scheme_name
    )
    save_resume_data(user_config, "software", engineer_data, engineer_config)

    # Product marketing version
    product_marketing_data = create_product_marketing_data(user_config)
    product_marketing_config = create_config_file(
        user_config, "product_marketing", color_scheme_name
    )
    save_resume_data(
        user_config, "marketing", product_marketing_data, product_marketing_config
    )

    print("\n✅ Resume data generation complete!")
    print(f"\n👤 User: {user_config.name}")
    print(f"🎨 Color scheme: {color_scheme_name}")
    print("\n📋 Generated versions:")
    print(
        f"   • {user_config.get_version_directory_name('research')} - Emphasizes applied research leadership"
    )
    print(
        f"   • {user_config.get_version_directory_name('technical')} - Shows engineering depth and technical skills"
    )
    print(
        f"   • {user_config.get_version_directory_name('comprehensive')} - Complete work history with all details"
    )
    print(
        f"   • {user_config.get_version_directory_name('consulting')} - Strategic advisor focused"
    )
    print(
        f"   • {user_config.get_version_directory_name('software')} - Software engineering and platform development (DEFAULT)"
    )
    print(
        f"   • {user_config.get_version_directory_name('marketing')} - Product marketing strategy and go-to-market leadership"
    )

    print("\n🚀 Next steps:")
    print("   1. Review the generated JSON files in inputs/ directories")
    print("   2. Customize any content or styling as needed")
    print(
        "   3. Generate resumes with: python resume_manager.py --version software --format pdf"
    )
    print(
        f"   4. Try different color schemes with: python resume_manager.py --generate-data --color-scheme [scheme_name]"
    )

    return 0


if __name__ == "__main__":
    exit(main())
