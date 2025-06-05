CURRICULUM_TEMPLATES = {
    "python": {
        "title": "Python Developer Path",
        "milestones": [
            {"title": "Python Basics", "description": "Syntax, variables, data types", "resources": ["Python.org Docs", "Automate the Boring Stuff"]},
            {"title": "Control Flow", "description": "If, loops, functions", "resources": ["Real Python", "YouTube: Python Loops"]},
            {"title": "Data Structures", "description": "Lists, dicts, sets, tuples", "resources": ["GeeksforGeeks", "Python Docs"]},
            {"title": "OOP in Python", "description": "Classes, objects, inheritance", "resources": ["Corey Schafer OOP Playlist"]},
            {"title": "File I/O & Exceptions", "description": "Reading/writing files, error handling", "resources": ["Python Docs", "YouTube: Exceptions"]},
            {"title": "Virtual Environments & Packages", "description": "venv, pip, requirements.txt", "resources": ["Python Docs", "Real Python"]},
            {"title": "Testing & Debugging", "description": "unittest, pdb", "resources": ["Real Python", "YouTube: Debugging"]},
            {"title": "Project: Build a CLI App", "description": "Apply all concepts in a mini-project", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 8
    },
    "data_science": {
        "title": "Data Science Path",
        "milestones": [
            {"title": "Data Analysis with Pandas", "description": "DataFrames, cleaning, EDA", "resources": ["Kaggle", "Pandas Docs"]},
            {"title": "Data Visualization", "description": "Matplotlib, Seaborn", "resources": ["YouTube: Data Viz", "Seaborn Docs"]},
            {"title": "Statistics Basics", "description": "Mean, median, std, distributions", "resources": ["Khan Academy", "StatQuest"]},
            {"title": "Machine Learning Intro", "description": "Supervised/unsupervised, scikit-learn", "resources": ["scikit-learn Docs", "YouTube: ML Crash Course"]},
            {"title": "Model Evaluation", "description": "Metrics, cross-validation", "resources": ["Kaggle", "YouTube: Model Eval"]},
            {"title": "Project: Data Science Case Study", "description": "End-to-end project", "resources": ["Kaggle Datasets"]}
        ],
        "timeline_weeks": 10
    },
    "web_dev": {
        "title": "Web Development Path",
        "milestones": [
            {"title": "HTML & CSS", "description": "Structure and style web pages", "resources": ["MDN Web Docs", "freeCodeCamp"]},
            {"title": "JavaScript Basics", "description": "Syntax, DOM, events", "resources": ["JavaScript.info", "YouTube: JS Crash Course"]},
            {"title": "Responsive Design", "description": "Flexbox, media queries", "resources": ["CSS Tricks", "YouTube: Responsive Design"]},
            {"title": "Frontend Frameworks", "description": "React basics", "resources": ["React Docs", "freeCodeCamp"]},
            {"title": "Backend Basics", "description": "APIs, databases, Python/Node.js", "resources": ["YouTube: REST APIs", "MongoDB University"]},
            {"title": "Project: Build a Web App", "description": "Full-stack mini-project", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 10
    },
    "machine_learning": {
        "title": "Machine Learning Path",
        "milestones": [
            {"title": "ML Foundations", "description": "Types, workflow, tools", "resources": ["scikit-learn Docs", "YouTube: ML Basics"]},
            {"title": "Regression & Classification", "description": "Linear, logistic, metrics", "resources": ["Kaggle", "StatQuest"]},
            {"title": "Clustering & Dimensionality Reduction", "description": "KMeans, PCA", "resources": ["YouTube: Clustering", "Kaggle"]},
            {"title": "Neural Networks Intro", "description": "Perceptron, MLP", "resources": ["3Blue1Brown", "YouTube: Neural Nets"]},
            {"title": "Project: ML Model", "description": "Train and evaluate a model", "resources": ["Kaggle Datasets"]}
        ],
        "timeline_weeks": 8
    },
    "cloud_computing": {
        "title": "Cloud Computing Path",
        "milestones": [
            {"title": "Cloud Basics", "description": "IaaS, PaaS, SaaS", "resources": ["AWS Training", "Azure Docs"]},
            {"title": "Cloud Providers", "description": "AWS, Azure, GCP", "resources": ["YouTube: Cloud Overview"]},
            {"title": "Storage & Databases", "description": "S3, RDS, NoSQL", "resources": ["AWS Docs", "MongoDB University"]},
            {"title": "Serverless & Containers", "description": "Lambda, Docker", "resources": ["YouTube: Serverless", "Docker Docs"]},
            {"title": "Project: Deploy to Cloud", "description": "Deploy a sample app", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 6
    },
    "devops": {
        "title": "DevOps Path",
        "milestones": [
            {"title": "Version Control", "description": "Git basics", "resources": ["GitHub Docs", "Atlassian Git"]},
            {"title": "CI/CD", "description": "Jenkins, GitHub Actions", "resources": ["YouTube: CI/CD", "Jenkins Docs"]},
            {"title": "Containers & Orchestration", "description": "Docker, Kubernetes", "resources": ["Docker Docs", "Kubernetes Docs"]},
            {"title": "Monitoring & Logging", "description": "Prometheus, ELK", "resources": ["YouTube: Monitoring"]},
            {"title": "Project: DevOps Pipeline", "description": "Automate deployment", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 6
    },
    "cybersecurity": {
        "title": "Cybersecurity Path",
        "milestones": [
            {"title": "Security Basics", "description": "CIA triad, threats", "resources": ["Cybrary", "YouTube: Security Basics"]},
            {"title": "Network Security", "description": "Firewalls, VPNs", "resources": ["Cisco Networking Academy"]},
            {"title": "Application Security", "description": "OWASP Top 10", "resources": ["OWASP", "YouTube: AppSec"]},
            {"title": "Cryptography", "description": "Encryption, hashing", "resources": ["Khan Academy", "YouTube: Crypto"]},
            {"title": "Project: Secure an App", "description": "Apply security best practices", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 6
    },
    "databases": {
        "title": "Databases Path",
        "milestones": [
            {"title": "SQL Basics", "description": "SELECT, INSERT, UPDATE, DELETE", "resources": ["SQLZoo", "W3Schools"]},
            {"title": "Database Design", "description": "ERD, normalization", "resources": ["Khan Academy", "YouTube: DB Design"]},
            {"title": "NoSQL Databases", "description": "MongoDB, Redis", "resources": ["MongoDB University", "Redis Docs"]},
            {"title": "Indexing & Optimization", "description": "Indexes, query plans", "resources": ["YouTube: DB Indexing"]},
            {"title": "Project: Design a DB", "description": "Create a database schema", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 6
    },
    "ai_fundamentals": {
        "title": "AI Fundamentals Path",
        "milestones": [
            {"title": "AI Basics", "description": "History, types, applications", "resources": ["YouTube: AI Basics", "Wikipedia: AI"]},
            {"title": "Search & Reasoning", "description": "Search algorithms, logic", "resources": ["GeeksforGeeks", "YouTube: AI Search"]},
            {"title": "Knowledge Representation", "description": "Ontologies, graphs", "resources": ["Wikipedia: Knowledge Representation"]},
            {"title": "Machine Learning Intro", "description": "Supervised/unsupervised", "resources": ["Kaggle", "YouTube: ML Intro"]},
            {"title": "Project: AI Mini-Project", "description": "Build a simple AI app", "resources": ["GitHub Examples"]}
        ],
        "timeline_weeks": 6
    }
}

def get_curriculum(domain: str) -> dict:
    """Return the curriculum template for a given domain."""
    return CURRICULUM_TEMPLATES.get(domain.lower()) 