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
## ▶️ Run the Application


```bash
python app.py
```

Then open: 👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📂 Project Structure

```
FeedbackHub/
├── app.py                     # Main Flask application
├── models.py                  # SQLAlchemy User & Feedback models
├── requirements.txt            # Python dependencies
├── init_db.py                  # Database initialization script
│
├── static/                     # Frontend assets
│   ├── css/                    # Styling (style.css)
│   ├── js/                     # Scripts (auth.js, admin.js, feedback.js)
│   └── images/                 # Icons & logos
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Common layout
│   ├── index.html              # Feedback form
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── dashboard.html          # User dashboard
│   └── admin.html              # Admin dashboard
│
└── uploads/                    # User-uploaded image storage
```

---

## 🧪 Testing

The project includes automated unit tests for authentication and route handling.

```bash
# Run tests
pytest -q tests/
```

### Manual Testing Coverage:
✅ Registration / Login  
✅ Feedback Submission (text + rating + image)  
✅ Sentiment Analysis Integration  
✅ Admin Dashboard Visualization  
✅ Data Export (CSV, PDF)  
✅ Input and File Validation  

---

## 📈 Architecture & Workflow Overview

### **Workflow Steps**
1. **User Registration/Login** → Credentials verified & stored securely  
2. **Feedback Submission** → Data + optional image sent to backend  
3. **Sentiment Analysis** → Processed using VADER + TextBlob NLP  
4. **Database Storage** → Results stored in SQLite database  
5. **Admin Dashboard** → Data visualized using Chart.js  
6. **Report Generation** → Export as CSV or PDF  

---

## 🏗️ System Architecture

*(<img width="1648" height="567" alt="image" src="https://github.com/user-attachments/assets/e9a22223-f434-48db-a8e1-5af4f4f1301f" />
)*

---

## 💡 Next Steps & Future Ideas

- **Alembic Integration:** Replace manual migrations with database migration support  
- **Role-Based Access Control (RBAC):** Add granular permissions for staff/admin roles  
- **Rate Limiting:** Use Flask-Limiter to prevent spam submissions  
- **Pagination & Filtering:** Optimize admin table performance for large datasets  
- **AI-based NLP Models:** Upgrade with advanced models (BERT, DistilBERT)  
- **Cloud Deployment:** Host on AWS, Azure, or Render for scalability  

---

## 👨‍💻 Author

**Vanga Sai Charan**  
Bachelor of Technology, Computer Science & Engineering  
JNTUH University College of Engineering, Manthani  

📫 **Email:** [saicharanvanga906@gmail.com](mailto:saicharanvanga906@gmail.com)  
🔗 **GitHub:** [https://github.com/SaicharanVa](https://github.com/SaicharanVa)  
💼 **LinkedIn:** [https://www.linkedin.com/in/sai-charan-va/](https://www.linkedin.com/in/sai-charan-va/)  

---

## ⭐ Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com)  
- [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)  
- [TextBlob NLP](https://textblob.readthedocs.io)  
- [Chart.js](https://www.chartjs.org)  
- [ReportLab](https://www.reportlab.com)

---

> **Note:** This project was developed as part of an industry project with **Tata Consultancy Services (TCS)**, demonstrating real-world application of full-stack development and AI integration.

