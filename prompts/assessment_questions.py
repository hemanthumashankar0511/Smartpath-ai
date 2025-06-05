import random

DOMAINS = {
    "python": [
        {"question": "What is the correct file extension for Python files?", "choices": [".py", ".pt", ".pyt", ".pyth"], "answer": ".py"},
        {"question": "Which keyword is used to define a function in Python?", "choices": ["func", "def", "function", "define"], "answer": "def"},
        {"question": "What is the output of print(2 ** 3)?", "choices": ["6", "8", "9", "5"], "answer": "8"},
        {"question": "Which of these is a mutable data type?", "choices": ["tuple", "str", "list", "int"], "answer": "list"},
        {"question": "How do you start a comment in Python?", "choices": ["//", "#", "<!--", "--"], "answer": "#"},
        {"question": "What does 'len([1,2,3])' return?", "choices": ["2", "3", "1", "0"], "answer": "3"},
        {"question": "Which of these is NOT a Python data structure?", "choices": ["set", "array", "list", "dict"], "answer": "array"},
        {"question": "What is the output of print('Hello' + 'World')?", "choices": ["Hello World", "HelloWorld", "Hello+World", "Error"], "answer": "HelloWorld"},
        {"question": "Which function is used to get input from the user?", "choices": ["scan()", "input()", "get()", "read()"], "answer": "input()"},
        {"question": "What is the correct way to create a dictionary?", "choices": ["{ 'a': 1, 'b': 2 }", "[ 'a', 1, 'b', 2 ]", "('a', 1, 'b', 2)", "< 'a': 1, 'b': 2 >"], "answer": "{ 'a': 1, 'b': 2 }"}
    ],
    "data_science": [
        {"question": "Which library is commonly used for data analysis in Python?", "choices": ["pandas", "matplotlib", "numpy", "scipy"], "answer": "pandas"},
        {"question": "What does CSV stand for?", "choices": ["Comma Separated Values", "Columnar Simple Values", "Common Separated Variables", "Comma Simple Values"], "answer": "Comma Separated Values"},
        {"question": "Which is a supervised learning algorithm?", "choices": ["K-Means", "Linear Regression", "PCA", "t-SNE"], "answer": "Linear Regression"},
        {"question": "What is the purpose of train/test split?", "choices": ["To evaluate model performance", "To clean data", "To visualize data", "To reduce overfitting"], "answer": "To evaluate model performance"},
        {"question": "Which metric is used for classification tasks?", "choices": ["Accuracy", "MSE", "R2 Score", "RMSE"], "answer": "Accuracy"},
        {"question": "What is overfitting?", "choices": ["Model fits noise", "Model fits trend", "Model underperforms", "Model is too simple"], "answer": "Model fits noise"},
        {"question": "Which library is used for plotting in Python?", "choices": ["matplotlib", "pandas", "scikit-learn", "seaborn"], "answer": "matplotlib"},
        {"question": "What is a confusion matrix used for?", "choices": ["Evaluating classification", "Data cleaning", "Feature selection", "Data normalization"], "answer": "Evaluating classification"},
        {"question": "Which is a dimensionality reduction technique?", "choices": ["PCA", "SVM", "Random Forest", "KNN"], "answer": "PCA"},
        {"question": "What is the output of a clustering algorithm?", "choices": ["Groups/Clusters", "Predictions", "Coefficients", "Residuals"], "answer": "Groups/Clusters"}
    ],
    "web_dev": [
        {"question": "What does HTML stand for?", "choices": ["HyperText Markup Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language", "Hyperlinking Text Markup Language"], "answer": "HyperText Markup Language"},
        {"question": "Which tag is used for the largest heading in HTML?", "choices": ["<h1>", "<head>", "<h6>", "<header>"], "answer": "<h1>"},
        {"question": "Which property is used to change text color in CSS?", "choices": ["color", "font-color", "text-color", "background-color"], "answer": "color"},
        {"question": "Which language runs in a web browser?", "choices": ["JavaScript", "Python", "C++", "Java"], "answer": "JavaScript"},
        {"question": "What does CSS stand for?", "choices": ["Cascading Style Sheets", "Creative Style System", "Computer Style Sheet", "Colorful Style Sheet"], "answer": "Cascading Style Sheets"},
        {"question": "Which HTTP method is used to update data?", "choices": ["PUT", "GET", "POST", "DELETE"], "answer": "PUT"},
        {"question": "What is the default port for HTTP?", "choices": ["80", "443", "21", "8080"], "answer": "80"},
        {"question": "Which tag is used to create a link in HTML?", "choices": ["<a>", "<link>", "<href>", "<url>"], "answer": "<a>"},
        {"question": "What is a CSS class selector?", "choices": [".classname", "#classname", "classname", "*classname"], "answer": ".classname"},
        {"question": "Which of these is a frontend framework?", "choices": ["React", "Django", "Flask", "Node.js"], "answer": "React"}
    ],
    "machine_learning": [
        {"question": "Which algorithm is used for classification?", "choices": ["Logistic Regression", "K-Means", "PCA", "Apriori"], "answer": "Logistic Regression"},
        {"question": "What is a decision tree?", "choices": ["A tree-like model", "A clustering method", "A neural network", "A regression method"], "answer": "A tree-like model"},
        {"question": "Which library is used for machine learning in Python?", "choices": ["scikit-learn", "matplotlib", "pandas", "numpy"], "answer": "scikit-learn"},
        {"question": "What is the purpose of cross-validation?", "choices": ["Model evaluation", "Data cleaning", "Feature scaling", "Data visualization"], "answer": "Model evaluation"},
        {"question": "What is a hyperparameter?", "choices": ["Parameter set before training", "Parameter learned during training", "A type of data", "A loss function"], "answer": "Parameter set before training"},
        {"question": "Which activation function is commonly used in neural networks?", "choices": ["ReLU", "Sigmoid", "Tanh", "All of the above"], "answer": "All of the above"},
        {"question": "What is overfitting?", "choices": ["Model fits noise", "Model fits trend", "Model underperforms", "Model is too simple"], "answer": "Model fits noise"},
        {"question": "What is the output of a regression algorithm?", "choices": ["Continuous value", "Class label", "Cluster", "Tree"], "answer": "Continuous value"},
        {"question": "Which is a loss function for classification?", "choices": ["Cross-entropy", "MSE", "MAE", "RMSE"], "answer": "Cross-entropy"},
        {"question": "What is feature scaling?", "choices": ["Normalizing data", "Cleaning data", "Visualizing data", "Splitting data"], "answer": "Normalizing data"}
    ],
    "cloud_computing": [
        {"question": "What is IaaS?", "choices": ["Infrastructure as a Service", "Internet as a Service", "Integration as a Service", "Interface as a Service"], "answer": "Infrastructure as a Service"},
        {"question": "Which is a cloud provider?", "choices": ["AWS", "Oracle", "Dell", "Lenovo"], "answer": "AWS"},
        {"question": "What is the main benefit of cloud computing?", "choices": ["Scalability", "Complexity", "Cost", "Latency"], "answer": "Scalability"},
        {"question": "What is SaaS?", "choices": ["Software as a Service", "Storage as a Service", "Security as a Service", "System as a Service"], "answer": "Software as a Service"},
        {"question": "Which is a deployment model?", "choices": ["Public Cloud", "Private Cloud", "Hybrid Cloud", "All of the above"], "answer": "All of the above"},
        {"question": "What is virtualization?", "choices": ["Creating virtual resources", "Physical hardware", "Cloud storage", "Networking"], "answer": "Creating virtual resources"},
        {"question": "Which protocol is used for secure file transfer?", "choices": ["SFTP", "FTP", "SMTP", "HTTP"], "answer": "SFTP"},
        {"question": "What is a container?", "choices": ["Lightweight VM", "Physical server", "Database", "Network device"], "answer": "Lightweight VM"},
        {"question": "Which is a cloud storage service?", "choices": ["S3", "EC2", "Lambda", "RDS"], "answer": "S3"},
        {"question": "What is the main advantage of serverless?", "choices": ["No server management", "More hardware", "Manual scaling", "Higher cost"], "answer": "No server management"}
    ],
    "devops": [
        {"question": "What does CI stand for?", "choices": ["Continuous Integration", "Continuous Improvement", "Code Integration", "Continuous Implementation"], "answer": "Continuous Integration"},
        {"question": "Which tool is used for containerization?", "choices": ["Docker", "Jenkins", "Kubernetes", "Git"], "answer": "Docker"},
        {"question": "What is the purpose of Jenkins?", "choices": ["Automation server", "Database", "Web server", "IDE"], "answer": "Automation server"},
        {"question": "What is Infrastructure as Code?", "choices": ["Managing infrastructure with code", "Manual server setup", "Physical hardware", "Cloud storage"], "answer": "Managing infrastructure with code"},
        {"question": "Which is a version control system?", "choices": ["Git", "Docker", "Jenkins", "AWS"], "answer": "Git"},
        {"question": "What is a pipeline?", "choices": ["Automated workflow", "Manual process", "Database", "Server"], "answer": "Automated workflow"},
        {"question": "Which tool is used for orchestration?", "choices": ["Kubernetes", "Docker", "Git", "Jenkins"], "answer": "Kubernetes"},
        {"question": "What is monitoring?", "choices": ["Tracking system health", "Writing code", "Testing", "Deployment"], "answer": "Tracking system health"},
        {"question": "What is a rollback?", "choices": ["Reverting to previous state", "Deploying new code", "Scaling up", "Testing"], "answer": "Reverting to previous state"},
        {"question": "Which is a configuration management tool?", "choices": ["Ansible", "Docker", "Git", "Jenkins"], "answer": "Ansible"}
    ],
    "cybersecurity": [
        {"question": "What does VPN stand for?", "choices": ["Virtual Private Network", "Virtual Public Network", "Verified Private Network", "Very Private Network"], "answer": "Virtual Private Network"},
        {"question": "Which is a type of malware?", "choices": ["Virus", "Firewall", "Patch", "Backup"], "answer": "Virus"},
        {"question": "What is phishing?", "choices": ["Fraudulent attempt to obtain sensitive info", "A type of firewall", "A backup method", "A network protocol"], "answer": "Fraudulent attempt to obtain sensitive info"},
        {"question": "Which protocol is used for secure web browsing?", "choices": ["HTTPS", "HTTP", "FTP", "SMTP"], "answer": "HTTPS"},
        {"question": "What is a firewall?", "choices": ["Network security device", "Malware", "Antivirus", "Backup"], "answer": "Network security device"},
        {"question": "What is encryption?", "choices": ["Converting data to code", "Deleting data", "Backing up data", "Compressing data"], "answer": "Converting data to code"},
        {"question": "Which is a strong password?", "choices": ["P@ssw0rd!23", "password", "123456", "qwerty"], "answer": "P@ssw0rd!23"},
        {"question": "What is two-factor authentication?", "choices": ["Extra security step", "A type of malware", "A backup method", "A network protocol"], "answer": "Extra security step"},
        {"question": "What is a DDoS attack?", "choices": ["Distributed Denial of Service", "Data Download Service", "Direct Data Output System", "Domain Data Service"], "answer": "Distributed Denial of Service"},
        {"question": "Which is a security best practice?", "choices": ["Regular updates", "Weak passwords", "Sharing credentials", "Ignoring alerts"], "answer": "Regular updates"}
    ],
    "databases": [
        {"question": "What does SQL stand for?", "choices": ["Structured Query Language", "Simple Query Language", "Sequential Query Language", "Standard Query Language"], "answer": "Structured Query Language"},
        {"question": "Which is a relational database?", "choices": ["MySQL", "MongoDB", "Redis", "Cassandra"], "answer": "MySQL"},
        {"question": "What is a primary key?", "choices": ["Unique identifier", "Foreign key", "Index", "Constraint"], "answer": "Unique identifier"},
        {"question": "Which command is used to retrieve data?", "choices": ["SELECT", "INSERT", "UPDATE", "DELETE"], "answer": "SELECT"},
        {"question": "What is normalization?", "choices": ["Organizing data", "Deleting data", "Backing up data", "Encrypting data"], "answer": "Organizing data"},
        {"question": "Which is a NoSQL database?", "choices": ["MongoDB", "PostgreSQL", "MySQL", "SQLite"], "answer": "MongoDB"},
        {"question": "What is an index?", "choices": ["Speeds up queries", "Deletes data", "Backs up data", "Encrypts data"], "answer": "Speeds up queries"},
        {"question": "Which SQL clause is used to filter results?", "choices": ["WHERE", "ORDER BY", "GROUP BY", "HAVING"], "answer": "WHERE"},
        {"question": "What is a foreign key?", "choices": ["Links tables", "Unique identifier", "Constraint", "Backup"], "answer": "Links tables"},
        {"question": "Which is a database management system?", "choices": ["Oracle", "Linux", "Windows", "Python"], "answer": "Oracle"}
    ],
    "ai_fundamentals": [
        {"question": "What does AI stand for?", "choices": ["Artificial Intelligence", "Automated Interface", "Advanced Internet", "Algorithmic Integration"], "answer": "Artificial Intelligence"},
        {"question": "Which is a branch of AI?", "choices": ["Machine Learning", "Web Development", "Database Design", "Networking"], "answer": "Machine Learning"},
        {"question": "What is the Turing Test?", "choices": ["Test for machine intelligence", "Test for speed", "Test for memory", "Test for accuracy"], "answer": "Test for machine intelligence"},
        {"question": "Which language is popular for AI?", "choices": ["Python", "HTML", "CSS", "PHP"], "answer": "Python"},
        {"question": "What is an expert system?", "choices": ["AI that mimics human expertise", "Database", "Web server", "Operating system"], "answer": "AI that mimics human expertise"},
        {"question": "Which is a type of neural network?", "choices": ["CNN", "SQL", "HTML", "CSS"], "answer": "CNN"},
        {"question": "What is natural language processing?", "choices": ["AI for understanding language", "AI for images", "AI for games", "AI for hardware"], "answer": "AI for understanding language"},
        {"question": "Which is a search algorithm?", "choices": ["A*", "HTML", "CSS", "SQL"], "answer": "A*"},
        {"question": "What is reinforcement learning?", "choices": ["Learning by reward/punishment", "Learning by example", "Learning by memory", "Learning by coding"], "answer": "Learning by reward/punishment"},
        {"question": "Which is an AI application?", "choices": ["Speech recognition", "Word processing", "Spreadsheet", "Web browsing"], "answer": "Speech recognition"}
    ]
}

def get_questions(domain: str, num_questions: int = 10, seed: int = None):
    """
    Return a randomized list of domain questions (with shuffled answer options).
    Optionally set a seed for reproducibility.
    """
    domain = domain.lower()
    questions = DOMAINS.get(domain, [])[:]
    if seed is not None:
        random.seed(seed)
    random.shuffle(questions)
    selected = questions[:num_questions]
    for q in selected:
        random.shuffle(q['choices'])
    return selected