🚀 Smart Feedback Collection and Sentiment Analysis Platform

Feedback Analysis is a Flask-based full-stack web application that allows users to submit feedback, automatically analyzes sentiment using VADER and TextBlob NLP models, and provides administrators with a secure visual dashboard for insights and reporting.

This project demonstrates end-to-end development — combining Flask (Python), NLP (VADER + TextBlob), data visualization (Chart.js), and secure authentication — to deliver a real-world feedback management solution.

## 🌟 Key Features

### 👥 User Features
- **Authentication & Access Control**: Secure registration and login with Flask-Login and password hashing via Werkzeug
- **Intelligent Feedback Submission**: Users (authenticated or anonymous) can submit textual feedback, rating (1-5), and optionally upload images
- **Real-Time Sentiment Analysis**: On submission, VADER and TextBlob models process feedback text and store sentiment categories and scores
- **Feedback History**: Logged-in users can view their previously submitted feedback

### 🧠 Admin Features
- **Admin Dashboard**: Interactive charts using Chart.js for sentiment distribution, rating trends, and feedback volume
- **Advanced Analytics**: View aggregated statistics, search/filter feedback, and export reports
- **Reporting Tools**: CSV and PDF report exports with date-based and sentiment-based filtering
- **Secure File Handling**: Uploaded images validated with Pillow (PIL) and stored with sanitized filenames

## 💻 Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| Backend Framework | Python 3.x, Flask | Web framework and server logic |
| Database | SQLite (Flask-SQLAlchemy) | Lightweight persistence layer |
| Authentication | Flask-Login, Werkzeug | Session management and password hashing |
| NLP / Analysis | VADER, TextBlob Sentiment | Real-time sentiment classification |
| Visualization | Chart.js | Dynamic charts for data analytics |
| File Handling | Pillow (PIL) | Image validation and upload management |
| Reporting | ReportLab | PDF report generation |
| Testing | pytest | Automated unit testing |
| Version Control | Git & GitHub | Source code management |

## ⚙️ Setup and Installation

### 🧱 Prerequisites
Ensure you have:
- Python 3.x
- pip (Python package manager)
- Virtual environment (recommended)

### 🔧 Installation Steps

```bash
# Clone the Repository
git clone https://github.com/SaicharanVa/FeedbackHub.git
cd FeedbackHub

# Create and Activate Virtual Environment
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate

# Install Dependencies
pip install -r requirements.txt

## 🗄️ Initialize Database & Folders

```bash
# Create uploads directory
mkdir uploads

# The database (feedback.db) and tables are created automatically on first run
