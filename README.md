** SmartHire – AI-Powered Job and Resume Assistant
About the Project:

SmartHire is a career helper for students. Upload your resume and it reads your details, finds jobs that fit you, suggests how to improve your resume for a job you want, and answers career questions in a chat. Answers come only from our own job data and career guides, with built-in safety checks. Built with Python and Streamlit.

Features:

Resume reading (PDF and DOCX).
Extracting skills and qualifications.
Finding suitable job opportunities.
Showing matching and missing skills.
Resume improvement suggestions.
Career guidance chatbot.
Answers based on uploaded career notes and job information.
Basic safety checks for user inputs.
Technologies Used

Python
Gemini
LangChain
Streamlit
FAISS
Sentence Transformers
Pydantic
Pandas
Git and GitHub
Installation

Clone this repository.

Create a virtual environment. python -m venv venv

Install the required packages: pip install -r requirements.txt

Create a ".env" file using ".env.example".

Add your API key to ".env".

How to run python test_parser.py

Dataset

Download the job dataset and place it inside:

"data/jobs/jobs.csv"

Project Status

Development in progress.

More features will be added during development.