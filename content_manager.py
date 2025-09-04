#!/usr/bin/env python3
"""
Content Management System for Resume Generator
Manages base content with role-specific overrides
"""

from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import json
from datetime import datetime


@dataclass(frozen=True)
class ContentTemplate:
    """Immutable content template structure"""

    role: str
    version: str  # 'long' or 'short'
    personal_info: Dict[str, str]
    summary: str
    competencies: Dict[str, List[str]]
    experience: List[Dict[str, Any]]
    achievements: Dict[str, List[str]]
    projects: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Dict[str, Any]]
    metadata: Dict[str, Any]


class ContentManager:
    """Manages base content and role-specific overrides"""

    def __init__(self, base_content_path: str = "content/base_content.json"):
        self.base_content_path = Path(base_content_path)
        self.base_content = self._load_base_content()
        self.role_overrides = self._load_role_overrides()

    def _load_base_content(self) -> Dict[str, Any]:
        """Load base content template"""
        if self.base_content_path.exists():
            with open(self.base_content_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            return self._create_default_base_content()

    def _load_role_overrides(self) -> Dict[str, Dict[str, Any]]:
        """Load role-specific overrides"""
        overrides_dir = Path("content/role_overrides")
        overrides = {}

        if overrides_dir.exists():
            for override_file in overrides_dir.glob("*.json"):
                role = override_file.stem
                with open(override_file, "r", encoding="utf-8") as f:
                    overrides[role] = json.load(f)

        return overrides

    def _create_default_base_content(self) -> Dict[str, Any]:
        """Create default base content structure"""
        return {
            "personal_info": {
                "name": "Dheeraj Chand",
                "email": "dheeraj.chand@gmail.com",
                "phone": "202.550.7110",
                "website": "https://www.dheerajchand.com",
                "linkedin": "https://www.linkedin.com/in/dheerajchand/",
                "github": "https://github.com/dheerajchand",
                "location": "Washington, DC",
            },
            "base_summary": "Experienced data professional with expertise in software engineering, data science, and research. Proven track record of leading cross-functional teams and delivering scalable solutions.",
            "base_competencies": {
                "Programming Languages": [
                    "Python",
                    "R",
                    "SQL",
                    "JavaScript",
                    "Scala",
                    "Java",
                ],
                "Data & Analytics": [
                    "Machine Learning",
                    "Statistical Analysis",
                    "Data Visualization",
                    "ETL/ELT",
                ],
                "Cloud & Infrastructure": [
                    "AWS",
                    "Google Cloud",
                    "Docker",
                    "Kubernetes",
                    "Apache Spark",
                ],
                "Tools & Frameworks": [
                    "Django",
                    "React",
                    "PostgreSQL",
                    "MongoDB",
                    "Tableau",
                    "PowerBI",
                ],
            },
            "base_experience": [
                {
                    "title": "Principal Data Scientist & Software Engineer",
                    "company": "Independent Consulting",
                    "location": "Washington, DC",
                    "dates": "2015 – Present",
                    "type": "consulting",
                    "base_responsibilities": [
                        "Led data science and software engineering projects for government and private sector clients",
                        "Developed scalable data platforms processing millions of records",
                        "Built machine learning models for predictive analytics",
                        "Mentored junior developers and data scientists",
                    ],
                },
                {
                    "title": "Senior Research Analyst",
                    "company": "Political Research Organization",
                    "location": "Washington, DC",
                    "dates": "2010 – 2015",
                    "type": "research",
                    "base_responsibilities": [
                        "Conducted statistical analysis of political and demographic data",
                        "Developed survey methodologies and sampling frameworks",
                        "Created data visualization dashboards for stakeholders",
                        "Published research findings in academic journals",
                    ],
                },
            ],
            "base_achievements": {
                "Technical Leadership": [
                    "Architected and deployed cloud-based data platforms serving 10,000+ users",
                    "Led development of open-source tools used by research community",
                    "Mentored 15+ junior developers and data scientists",
                ],
                "Research & Innovation": [
                    "Published 5+ peer-reviewed research papers",
                    "Presented at 10+ international conferences",
                    "Developed novel statistical methodologies for survey research",
                ],
            },
            "base_projects": [
                {
                    "name": "Redistricting Analysis Platform",
                    "description": "Built comprehensive platform for electoral district analysis",
                    "technologies": [
                        "Python",
                        "Django",
                        "PostgreSQL",
                        "React",
                        "D3.js",
                    ],
                    "impact": "Used by 1,000+ researchers and analysts nationwide",
                },
                {
                    "name": "Survey Research Framework",
                    "description": "Developed statistical framework for survey methodology",
                    "technologies": ["R", "Python", "SQL", "Statistical Modeling"],
                    "impact": "Adopted by 3 major research organizations",
                },
            ],
            "base_education": [
                {
                    "degree": "Master of Science in Statistics",
                    "institution": "Georgetown University",
                    "location": "Washington, DC",
                    "year": "2010",
                    "gpa": "3.8/4.0",
                },
                {
                    "degree": "Bachelor of Science in Mathematics",
                    "institution": "University of Maryland",
                    "location": "College Park, MD",
                    "year": "2008",
                    "gpa": "3.6/4.0",
                },
            ],
            "base_certifications": [
                {
                    "name": "AWS Certified Solutions Architect",
                    "issuer": "Amazon Web Services",
                    "year": "2022",
                },
                {
                    "name": "Certified Analytics Professional",
                    "issuer": "INFORMS",
                    "year": "2021",
                },
            ],
        }

    def get_content_template(self, role: str, version: str = "long") -> ContentTemplate:
        """
        Get content template with role-specific overrides

        Args:
            role: Target role (e.g., 'software_engineer', 'data_scientist', 'research_analyst')
            version: 'long' or 'short'

        Returns:
            ContentTemplate with merged content
        """
        # Start with base content
        content = self.base_content.copy()

        # Apply role-specific overrides
        if role in self.role_overrides:
            content = self._merge_content(content, self.role_overrides[role])

        # Apply version-specific modifications
        content = self._apply_version_modifications(content, version)

        # Create immutable template
        return ContentTemplate(
            role=role,
            version=version,
            personal_info=content["personal_info"],
            summary=content["summary"],
            competencies=content["competencies"],
            experience=content["experience"],
            achievements=content["achievements"],
            projects=content["projects"],
            education=content["education"],
            certifications=content["certifications"],
            metadata=content.get("metadata", {}),
        )

    def _merge_content(
        self, base: Dict[str, Any], overrides: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge role-specific overrides with base content"""
        merged = base.copy()

        for key, value in overrides.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                merged[key] = self._merge_content(merged[key], value)
            else:
                merged[key] = value

        return merged

    def _apply_version_modifications(
        self, content: Dict[str, Any], version: str
    ) -> Dict[str, Any]:
        """Apply modifications based on version (long vs short)"""
        if version == "short":
            # Shorten summary
            if "summary" in content:
                content["summary"] = (
                    content["summary"][:200] + "..."
                    if len(content["summary"]) > 200
                    else content["summary"]
                )

            # Limit experience entries
            if "experience" in content and len(content["experience"]) > 3:
                content["experience"] = content["experience"][:3]

            # Limit projects
            if "projects" in content and len(content["projects"]) > 2:
                content["projects"] = content["projects"][:2]

            # Limit achievements
            if "achievements" in content:
                for category, items in content["achievements"].items():
                    if len(items) > 3:
                        content["achievements"][category] = items[:3]

        return content

    def create_role_override(self, role: str, overrides: Dict[str, Any]) -> None:
        """Create role-specific override file"""
        overrides_dir = Path("content/role_overrides")
        overrides_dir.mkdir(parents=True, exist_ok=True)

        override_file = overrides_dir / f"{role}.json"
        with open(override_file, "w", encoding="utf-8") as f:
            json.dump(overrides, f, indent=2, ensure_ascii=False)

    def save_base_content(self) -> None:
        """Save base content to file"""
        self.base_content_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.base_content_path, "w", encoding="utf-8") as f:
            json.dump(self.base_content, f, indent=2, ensure_ascii=False)


def create_software_engineer_overrides() -> Dict[str, Any]:
    """Create software engineer specific overrides"""
    return {
        "summary": "Senior Software Engineer with 15+ years of experience building scalable data platforms, web applications, and distributed systems. Expert in full-stack development with deep specialization in Python, JavaScript, and cloud technologies. Proven track record of leading engineering teams and delivering mission-critical applications.",
        "competencies": {
            "Programming Languages": [
                "Python",
                "JavaScript",
                "TypeScript",
                "Scala",
                "Java",
                "Go",
            ],
            "Frameworks & Libraries": [
                "Django",
                "Flask",
                "React",
                "Node.js",
                "Express",
                "FastAPI",
            ],
            "Cloud & Infrastructure": [
                "AWS",
                "Google Cloud",
                "Docker",
                "Kubernetes",
                "Terraform",
                "CI/CD",
            ],
            "Databases & Data": [
                "PostgreSQL",
                "MongoDB",
                "Redis",
                "Apache Spark",
                "Apache Kafka",
            ],
            "DevOps & Tools": [
                "Git",
                "Jenkins",
                "GitLab CI",
                "Prometheus",
                "Grafana",
                "ELK Stack",
            ],
        },
        "experience": [
            {
                "title": "Senior Software Engineer & Technical Lead",
                "company": "Independent Consulting",
                "location": "Washington, DC",
                "dates": "2015 – Present",
                "type": "engineering",
                "responsibilities": [
                    "Architected and developed scalable web applications serving 100,000+ users",
                    "Led full-stack development using Python, Django, React, and PostgreSQL",
                    "Implemented CI/CD pipelines reducing deployment time by 70%",
                    "Mentored 8+ junior developers and conducted technical interviews",
                    "Built microservices architecture handling 1M+ API requests daily",
                ],
            },
            {
                "title": "Full-Stack Developer",
                "company": "Political Research Organization",
                "location": "Washington, DC",
                "dates": "2010 – 2015",
                "type": "engineering",
                "responsibilities": [
                    "Developed data visualization platforms using D3.js and React",
                    "Built ETL pipelines processing 10TB+ of political data",
                    "Created RESTful APIs and database schemas for research applications",
                    "Optimized database queries improving performance by 60%",
                ],
            },
        ],
        "achievements": {
            "Technical Leadership": [
                "Led development of open-source redistricting platform used by 1,000+ researchers",
                "Architected cloud migration reducing infrastructure costs by 40%",
                "Implemented automated testing increasing code coverage to 95%",
                "Mentored 15+ developers, with 80% advancing to senior roles",
            ],
            "Software Development": [
                "Built real-time collaborative editing system supporting 50+ concurrent users",
                "Developed machine learning pipeline processing 100M+ records daily",
                "Created comprehensive API documentation and developer onboarding process",
                "Established coding standards and code review processes adopted company-wide",
            ],
        },
        "projects": [
            {
                "name": "Redistricting Analysis Platform",
                "description": "Full-stack web application for electoral district analysis with real-time collaboration",
                "technologies": [
                    "Python",
                    "Django",
                    "PostgreSQL",
                    "React",
                    "WebSockets",
                    "D3.js",
                ],
                "impact": "1,000+ active users, 50+ concurrent sessions, 99.9% uptime",
                "github": "https://github.com/dheerajchand/redistricting-platform",
            },
            {
                "name": "Data Pipeline Framework",
                "description": "Scalable ETL framework for processing large-scale political and demographic data",
                "technologies": [
                    "Python",
                    "Apache Spark",
                    "Apache Kafka",
                    "Docker",
                    "Kubernetes",
                ],
                "impact": "Processes 1TB+ daily, 99.5% data accuracy, 50% faster than previous system",
                "github": "https://github.com/dheerajchand/data-pipeline-framework",
            },
            {
                "name": "Survey Research API",
                "description": "RESTful API for survey data collection and statistical analysis",
                "technologies": ["Python", "FastAPI", "PostgreSQL", "Redis", "Celery"],
                "impact": "Serves 10+ research organizations, 1M+ API calls monthly",
                "github": "https://github.com/dheerajchand/survey-api",
            },
        ],
    }


def create_data_scientist_overrides() -> Dict[str, Any]:
    """Create data scientist specific overrides"""
    return {
        "summary": "Senior Data Scientist with 15+ years of experience in statistical analysis, machine learning, and data engineering. Expert in translating complex analytical requirements into scalable technical solutions. Proven track record of leading data science teams and delivering insights that drive strategic decision-making.",
        "competencies": {
            "Programming Languages": ["Python", "R", "SQL", "Scala", "Julia"],
            "Machine Learning": [
                "Scikit-learn",
                "TensorFlow",
                "PyTorch",
                "XGBoost",
                "Pandas",
                "NumPy",
            ],
            "Statistics & Analytics": [
                "Statistical Modeling",
                "A/B Testing",
                "Time Series",
                "Bayesian Methods",
            ],
            "Data Engineering": [
                "Apache Spark",
                "Apache Kafka",
                "Airflow",
                "dbt",
                "ETL/ELT",
            ],
            "Visualization & Tools": [
                "Tableau",
                "PowerBI",
                "D3.js",
                "Matplotlib",
                "Seaborn",
                "Plotly",
            ],
        },
        "achievements": {
            "Data Science Leadership": [
                "Led data science team of 8 analysts delivering 20+ ML models annually",
                "Developed predictive models with 95%+ accuracy for political forecasting",
                "Created automated reporting system reducing analysis time by 80%",
                "Mentored 12+ junior data scientists and analysts",
            ],
            "Research & Innovation": [
                "Published 8+ peer-reviewed papers in statistical methodology",
                "Developed novel sampling techniques adopted by 5+ research organizations",
                "Created open-source statistical analysis framework with 500+ GitHub stars",
                "Presented at 15+ international conferences on data science and statistics",
            ],
        },
    }


def create_research_analyst_overrides() -> Dict[str, Any]:
    """Create research analyst specific overrides"""
    return {
        "summary": "Senior Research Analyst with 15+ years of experience in survey methodology, statistical analysis, and policy research. Expert in designing and implementing large-scale research studies for government and nonprofit organizations. Proven track record of translating complex research findings into actionable policy recommendations.",
        "competencies": {
            "Research Methods": [
                "Survey Design",
                "Sampling Methodology",
                "Experimental Design",
                "Qualitative Research",
            ],
            "Statistical Analysis": [
                "R",
                "SPSS",
                "SAS",
                "Stata",
                "Regression Analysis",
                "Multivariate Statistics",
            ],
            "Data Management": [
                "SQL",
                "Python",
                "Data Cleaning",
                "Data Validation",
                "Quality Assurance",
            ],
            "Policy Analysis": [
                "Program Evaluation",
                "Impact Assessment",
                "Cost-Benefit Analysis",
                "Policy Research",
            ],
            "Communication": [
                "Report Writing",
                "Data Visualization",
                "Presentation Skills",
                "Stakeholder Engagement",
            ],
        },
        "achievements": {
            "Research Leadership": [
                "Led 25+ major research studies with budgets totaling $5M+",
                "Developed survey methodologies used by 10+ government agencies",
                "Created data visualization dashboards for congressional briefings",
                "Mentored 20+ junior researchers and analysts",
            ],
            "Policy Impact": [
                "Research findings cited in 3+ congressional hearings",
                "Developed evaluation framework adopted by Department of Education",
                "Created statistical models for redistricting analysis used in court cases",
                "Published 12+ policy briefs with 100,000+ total downloads",
            ],
        },
    }


def main():
    """Create content management system and role overrides"""
    print("🚀 Setting up Content Management System")
    print("=" * 50)

    # Create content manager
    manager = ContentManager()

    # Create role-specific overrides
    roles = {
        "software_engineer": create_software_engineer_overrides(),
        "data_scientist": create_data_scientist_overrides(),
        "research_analyst": create_research_analyst_overrides(),
    }

    for role, overrides in roles.items():
        manager.create_role_override(role, overrides)
        print(f"✅ Created overrides for: {role}")

    # Save base content
    manager.save_base_content()
    print("✅ Saved base content")

    # Test content generation
    print("\n🧪 Testing content generation:")

    for role in ["software_engineer", "data_scientist", "research_analyst"]:
        for version in ["long", "short"]:
            template = manager.get_content_template(role, version)
            print(
                f"  {role} ({version}): {len(template.experience)} experience entries, {len(template.projects)} projects"
            )

    print("\n🎉 Content management system ready!")


if __name__ == "__main__":
    main()
