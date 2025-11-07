🌟 Smart Feedback Collection and Sentiment Analysis Platform

Feedback Analysis is a Flask-based full-stack web application that allows users to submit feedback, automatically analyzes sentiment using the VADER,TextBlob NLP model, and provides administrators with a secure visual dashboard for insights and reporting.

This project demonstrates end-to-end development — combining Flask (Python), NLP (VADER),NLP (TextBlob) data visualization (Chart.js), and secure authentication — to deliver a real-world feedback management solution.

🚀 Key Features
👥 User Features

Authentication & Access Control: Secure registration and login with Flask-Login and password hashing via Werkzeug.

Intelligent Feedback Submission: Users (authenticated or anonymous) can submit textual feedback, a rating (1–5), and optionally upload an image.

Real-Time Sentiment Analysis: On submission, the VADER and TextBlob model processes feedback text and stores:

Sentiment Category → Positive / Neutral / Negative

Sentiment Score → Compound score between -1.0 and 1.0.

Feedback History: Logged-in users can view their previously submitted feedback.

🧠 Admin Features

Admin Dashboard: Displays interactive charts using Chart.js and D3.js for sentiment distribution, rating trends, and feedback volume.

Advanced Analytics: View aggregated statistics, search/filter feedback, and export reports.

Reporting Tools:

CSV and PDF report exports (via ReportLab)

Date-based and sentiment-based filtering

Secure File Handling: Uploaded images validated with Pillow (PIL) and stored with sanitized filenames.

💻 Tech Stack
Category	Technology	Purpose
Backend Framework	Python 3.x, Flask	Web framework and server logic
Database	SQLite (Flask-SQLAlchemy)	Lightweight persistence layer (feedback.db)
Authentication	Flask-Login, Werkzeug	Session management and password hashing
NLP / Analysis	VADER,TextBlob Sentiment	Real-time sentiment classification
Visualization	Chart.js, D3.js	Dynamic charts for data analytics
File Handling	Pillow (PIL)	Image validation and upload management
Reporting	ReportLab	PDF report generation
Testing	pytest	Automated unit testing
Version Control	Git & GitHub	Source code management
⚙️ Setup and Installation
🧱 Prerequisites

Ensure you have:

Python 3.x

pip (Python package manager)

Virtual environment (recommended)

🔧 Installation Steps
# Clone the Repository
git clone https://github.com/SaicharanVa/
cd FeedbackHub

# Create and Activate Virtual Environment
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

🗄️ Initialize Database & Folders
# Create uploads directory
mkdir uploads

# The database (feedback.db) and tables are created automatically on first run
# If updating schema, run migration script:
# python scripts/add_email_column.py

▶️ Run the Application
python app.py


Then open:
👉 http://127.0.0.1:5000

📂 Project Structure
FeedbackHub/
├── app.py                     # Main Flask application
├── models.py                  # SQLAlchemy User & Feedback models
├── feedback.db                # SQLite database file
├── requirements.txt           
│
├── static/                    # Frontend assets
│   ├── css/                   # Styling (style.css)
│   ├── js/                    # Scripts (auth.js, admin.js, feedback.js)
│   └── images/                # Icons & logos
│
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Common layout
│   ├── index.html             # Feedback form
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── dashboard.html         # User dashboard
│   └── admin.html             # Admin dashboard
│
└── uploads/                   # User-uploaded image storage

🧪 Testing

The project includes automated unit tests for authentication and route handling.

# Run tests
pytest -q tests/


Manual Testing Coverage:

✅ Registration / Login

✅ Feedback Submission (text + rating + image)

✅ Sentiment Analysis Integration

✅ Admin Dashboard Visualization

✅ Data Export (CSV, PDF)

✅ Input and File Validation

📈 Architecture & Workflow Overview

Workflow Steps

User Registration/Login → Credentials verified & stored securely.

Feedback Submission → Data + optional image sent to backend.

Sentiment Analysis → Processed using VADER NLP.

Database Storage → Results stored in SQLite (feedback.db).

Admin Dashboard → Data visualized using Chart.js / D3.js.

Report Generation → Export as CSV or PDF.

📊 (Refer to your architecture diagram and workflow image here — name it architecture.png and link below)

![System Architecture](static/images/architecture.png)

💡 Next Steps & Future Ideas

Alembic Integration: Replace manual migrations with database migration support.

Role-Based Access Control (RBAC): Add granular permissions for staff/admin roles.

Rate Limiting: Use Flask-Limiter to prevent spam submissions from anonymous users.

Pagination & Filtering: Optimize admin table performance for large datasets.

AI-based NLP Models: Upgrade VADER with advanced models (BERT, DistilBERT).

Cloud Deployment: Host on AWS, Azure, or Render for scalability.


👨‍💻 Author

Vanga Sai Charan
Bachelor of Technology, Computer Science & Engineering
JNTUH University College of Engineering, Manthani

📫 Email: saicharanvanga906@gmail.com
]
🔗 GitHub: https://github.com/SaicharanVa

💼 LinkedIn:https://www.linkedin.com/in/sai-charan-va/

⭐ Acknowledgements

Flask Documentation

VADER Sentiment

Chart.js

ReportLab