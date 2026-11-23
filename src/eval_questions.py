"""30 mentor test questions, written before looking at any results.
'expect' = words that should appear in the title of at least one source used."""

IN_SCOPE = [
    {"q": "How do I become a Data Analyst?", "expect": ["data analyst"]},
    {"q": "What skills do I need to become a Machine Learning Engineer?", "expect": ["machine learning"]},
    {"q": "How can I become a full stack web developer?", "expect": ["full stack"]},
    {"q": "What should a software fresher learn first?", "expect": ["roadmap", "fresher"]},
    {"q": "How do I switch my career into tech?", "expect": ["switch"]},
    {"q": "How should I write my resume as a fresher?", "expect": ["resume"]},
    {"q": "What are common resume mistakes freshers make?", "expect": ["mistakes", "resume"]},
    {"q": "How do I prepare for a technical interview?", "expect": ["interview"]},
    {"q": "What is the difference between junior and senior level jobs?", "expect": ["junior"]},
    {"q": "What are the experience levels in tech jobs?", "expect": ["junior", "fresher"]},
    {"q": "Which jobs need React and Node.js?", "expect": ["react", "full stack", "frontend", "node"]},
    {"q": "Show me data analyst jobs that need Power BI.", "expect": ["data analyst", "power bi"]},
    {"q": "Which machine learning engineer jobs need TensorFlow?", "expect": ["machine learning"]},
    {"q": "What skills do QA engineer jobs ask for?", "expect": ["qa"]},
    {"q": "Which Android developer jobs are available?", "expect": ["android"]},
    {"q": "What do DevOps jobs require?", "expect": ["devops"]},
    {"q": "Is Python enough to get a job as a data analyst?", "expect": ["data analyst"]},
    {"q": "How should I show my projects on my resume?", "expect": ["resume"]},
    {"q": "What should I learn to become a backend developer?", "expect": ["backend", "roadmap"]},
    {"q": "Which companies are hiring Frontend Developers?", "expect": ["frontend"]},
]

# Nothing to do with careers
UNRELATED = [
    {"q": "What is the weather in Mumbai today?"},
    {"q": "Explain how photosynthesis works."},
    {"q": "Who is the prime minister of India?"},
    {"q": "Translate 'good morning' into French."},
    {"q": "What is 25 times 18?"},
]

# Sound like career questions, but our documents do not contain the answer
NOT_IN_DOCS = [
    {"q": "What is the salary of a Data Analyst at Google?"},
    {"q": "What is the visa process for working in Germany?"},
    {"q": "Which company in India has the best work culture?"},
    {"q": "What will happen to software jobs by 2035?"},
    {"q": "What is the notice period rule under Indian labour law?"},
]