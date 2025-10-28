# Feedback Management Application

## Overview
A comprehensive feedback management system built with Flask, featuring sentiment analysis, user authentication, and advanced admin analytics. The application allows users to submit feedback with images and ratings, while administrators can analyze feedback through interactive visualizations and manage submissions.

## Recent Changes (October 28, 2025)
- ✅ **Admin Feedback Restriction**: Prevented admin users from submitting feedback (admins can only view and manage)
- ✅ Added delete feedback functionality for admin users
- ✅ Implemented Category vs Sentiment donut chart visualization
- ✅ Added time-based filtering (Past 10 days, Past 1 month, All time) for admin analytics
- ✅ Enhanced admin dashboard with interactive Chart.js visualizations
- ✅ Improved UI/UX with responsive design and smooth animations

## Tech Stack
- **Backend**: Flask (Python 3.11)
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with role-based access control
- **Sentiment Analysis**: VADER (Valence Aware Dictionary and sEntiment Reasoner)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Visualizations**: Chart.js for interactive charts
- **Image Processing**: Pillow
- **PDF Export**: ReportLab

## Project Architecture

### Backend Structure
- `app.py` - Main Flask application with all routes and API endpoints
- `models.py` - Database models (User, Feedback)
- `instance/feedback.db` - SQLite database (auto-created on first run)

### Frontend Structure
```
static/
├── css/
│   └── style.css - Global styles and responsive design
└── js/
    ├── admin.js - Admin dashboard functionality
    ├── auth.js - Authentication forms handling
    └── feedback.js - Feedback submission and user dashboard

templates/
├── base.html - Base template with navigation
├── index.html - Landing page with feedback form
├── login.html - User login page
├── register.html - User registration page
├── dashboard.html - User dashboard to view submitted feedback
└── admin.html - Admin analytics dashboard
```

### Features
1. **User Authentication**
   - Registration with email validation
   - Secure login with password hashing (Werkzeug)
   - Role-based access (User/Admin)
   - Session management with Flask-Login

2. **Feedback Submission**
   - Multiple feedback types (Complaint, Suggestion, Praise, General)
   - Text feedback with sentiment analysis
   - Optional image upload (PNG, JPG, JPEG, GIF)
   - Star rating system (1-5 stars)
   - Automatic sentiment detection (Positive, Negative, Neutral)

3. **User Dashboard**
   - View all submitted feedback
   - Filter by sentiment and feedback type
   - Delete own feedback
   - Download feedback as PDF

4. **Admin Dashboard**
   - **Statistics Overview**: Total feedback, average rating, sentiment counts
   - **Time-Based Filtering**: Past 10 days, Past 1 month, All time
   - **Sentiment Analysis Chart**: Pie chart showing sentiment distribution
   - **Feedback Type Chart**: Bar chart showing feedback by category
   - **Category vs Sentiment Chart**: Donut chart showing combined category-sentiment distribution
   - **Feedback Table**: Sortable table with all feedback details
   - **Delete Functionality**: Admin can delete any feedback with confirmation
   - **Filters**: Filter table by sentiment and feedback type
   - **Image Preview**: Click to view uploaded images in modal

5. **API Endpoints**
   - `GET /api/summary?time_filter=<filter>` - Dashboard statistics
   - `GET /api/feedbacks?time_filter=<filter>` - All feedback data
   - `GET /api/category-sentiment?time_filter=<filter>` - Category-sentiment aggregation
   - `DELETE /api/feedback/<id>` - Delete specific feedback (admin only)
   - `GET /api/user-feedbacks` - User's own feedback
   - `DELETE /api/user-feedback/<id>` - Delete own feedback

## Default Admin Account
- **Email**: admin@example.com
- **Password**: admin123

## Dependencies
See `requirements.txt`:
- Flask==3.0.0
- Flask-Login==0.6.3
- Flask-SQLAlchemy==3.1.1
- vaderSentiment==3.3.2
- Werkzeug==3.0.1
- Pillow==10.1.0
- reportlab==4.0.7

## Running the Application
The application runs on port 5000 with the workflow configured to execute:
```bash
python app.py
```

Access the application at the provided Replit URL.

## Security Features
- Password hashing with Werkzeug
- Session management with Flask-Login
- Role-based access control (@login_required, @admin_required)
- Secure file upload with extension validation
- CSRF protection via session tokens
- SQL injection protection via SQLAlchemy ORM
- Admin-only DELETE endpoint with authentication check

## Future Enhancements (Optional)
- Add CSRF tokens for DELETE requests
- Implement email notifications for new feedback
- Add export functionality for admin analytics
- Implement feedback response system
- Add real-time updates with WebSockets

## Notes
- LSP may show import errors, but these are false positives - all packages are installed and working correctly
- The application uses SQLite for development; consider PostgreSQL for production
- Images are stored in `/uploads` directory (auto-created)
- Debug mode is enabled for development
