import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
# Import necessary modules for sentiment analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # VADER - Primary sentiment analyzer
from textblob import TextBlob  # TextBlob - Secondary analyzer
import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
from models import db, User, Feedback
from datetime import datetime, timedelta
from sqlalchemy import text as sql_text
import csv
from io import StringIO, BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from PIL import Image
from flask import request
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize VADER sentiment analyzer (Primary)
# VADER (Valence Aware Dictionary and sEntiment Reasoner) is our primary sentiment analyzer
# It is specifically attuned to social media and short texts, and handles:
# - Emojis and emoticons
# - Punctuation and capitalization
# - Common slang and abbreviations
analyzer = SentimentIntensityAnalyzer()

# Note: TextBlob (Secondary) is initialized on-demand when needed
# TextBlob provides:
# - Traditional sentiment analysis based on pattern matching
# - Additional NLP features like noun phrase extraction
# - More conservative sentiment scoring

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def auth_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not current_user.is_authenticated:
            session['next'] = request.url
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        session_user_id = session.get('user_id') or session.get('_user_id')
        if not session_user_id or str(session_user_id) != str(current_user.id):
            logout_user()
            session.clear()
            flash('Your session has expired. Please log in again.', 'error')
            return redirect(url_for('login'))
        return view_function(*args, **kwargs)
    return wrapped_view

def validate_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except:
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/x')
def debug_x():
    try:
        from flask import request
        app.logger.warning("Received request to /x — headers: %s; referrer: %s; ua: %s",
                           dict(request.headers), request.referrer, request.user_agent.string)
    except Exception:
        app.logger.exception('Error logging /x request')
    return ('', 204)

@app.route('/client_error', methods=['POST'])
def client_error():
    try:
        data = request.get_data(as_text=True)
        app.logger.warning('Client error report: %s', data)
    except Exception:
        app.logger.exception('Failed to log client error')
    return ('', 204)

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            session['user_id'] = user.id
            next_page = session.pop('next', None)
            if next_page:
                return redirect(next_page)
            if user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    resp = make_response(render_template('login.html'))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not password or not password_confirm:
            flash('Please provide and confirm your password.', 'error')
            return render_template('register.html')
        if password != password_confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        new_user = User(name=name, email=email, password_hash=hashed_password, role='user')

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@auth_required
def logout():
    logout_user()
    session.clear()

    resp = redirect(url_for('index'))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/dashboard')
@auth_required
def dashboard():
    user_feedbacks = Feedback.query.filter_by(user_id=current_user.id).order_by(Feedback.timestamp.desc()).all()
    resp = make_response(render_template('dashboard.html', feedbacks=user_feedbacks))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/admin')
@auth_required
def admin():
    if current_user.role != 'admin':
        flash('Access denied', 'error')
        return redirect(url_for('index'))

    resp = make_response(render_template('admin.html'))
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    try:
        if current_user.is_authenticated and current_user.role == 'admin':
            return jsonify({'success': False, 'message': 'Administrators cannot submit feedback'}), 403
        
        data = request.form
        if current_user.is_authenticated:
            name = current_user.name
            contact_email = current_user.email
        else:
            name = data.get('name', 'Anonymous')
            contact_email = data.get('email') or data.get('contact_email')
        feedback_type = data.get('feedback_type')
        text = data.get('text')
        rating = data.get('rating')
        
        if not feedback_type or not text:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Primary Sentiment Analysis using VADER
        try:
            # Get sentiment scores from VADER
            sentiment_scores = analyzer.polarity_scores(text)
            compound_score = sentiment_scores['compound']
            
            # Determine sentiment based on VADER compound score
            if compound_score >= 0.05:
                sentiment = 'Positive'
            elif compound_score <= -0.05:
                sentiment = 'Negative'
            else:
                sentiment = 'Neutral'
        
        except Exception as vader_error:
            # Fallback to TextBlob if VADER fails
            try:
                # Create TextBlob object for sentiment analysis
                blob = TextBlob(text)
                # Get polarity score from TextBlob (-1 to 1 range)
                polarity = blob.sentiment.polarity
                compound_score = polarity  # Use TextBlob polarity as compound score
                
                # Convert TextBlob polarity to sentiment categories
                if polarity > 0.1:
                    sentiment = 'Positive'
                elif polarity < -0.1:
                    sentiment = 'Negative'
                else:
                    sentiment = 'Neutral'
                    
            except Exception as textblob_error:
                # If both analyzers fail, default to Neutral
                sentiment = 'Neutral'
                compound_score = 0
                app.logger.error(f"Sentiment analysis failed - VADER: {vader_error}, TextBlob: {textblob_error}")
        
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                if validate_image(file_path):
                    image_path = filename
                else:
                    os.remove(file_path)
                    return jsonify({'success': False, 'message': 'Invalid image file'}), 400
        
        feedback = Feedback(
            user_id=current_user.id if current_user.is_authenticated else None,
            name=name,
            email=contact_email,
            feedback_type=feedback_type,
            text=text,
            rating=int(rating) if rating else None,
            sentiment=sentiment,
            score=compound_score,
            image_path=image_path
        )
        
        db.session.add(feedback)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Feedback submitted successfully!',
            'sentiment': sentiment,
            'score': compound_score
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/summary')
@auth_required
def get_summary():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    time_filter = request.args.get('time_filter', 'all')
    
    query = Feedback.query
    if time_filter == '10days':
        cutoff_date = datetime.utcnow() - timedelta(days=10)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    elif time_filter == '1month':
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    
    total_feedback = query.count()
    
    positive = query.filter_by(sentiment='Positive').count()
    negative = query.filter_by(sentiment='Negative').count()
    neutral = query.filter_by(sentiment='Neutral').count()
    
    feedbacks_with_rating = query.filter(Feedback.rating.isnot(None)).all()
    avg_rating = sum([f.rating for f in feedbacks_with_rating]) / len(feedbacks_with_rating) if feedbacks_with_rating else 0
    
    feedback_types_result = db.session.query(
        Feedback.feedback_type,
        db.func.count(Feedback.id)
    )
    
    if time_filter == '10days':
        cutoff_date = datetime.utcnow() - timedelta(days=10)
        feedback_types_result = feedback_types_result.filter(Feedback.timestamp >= cutoff_date)
    elif time_filter == '1month':
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        feedback_types_result = feedback_types_result.filter(Feedback.timestamp >= cutoff_date)
    
    feedback_types = feedback_types_result.group_by(Feedback.feedback_type).all()
    
    types_data = {ft: count for ft, count in feedback_types}
    
    return jsonify({
        'total': total_feedback,
        'sentiment': {
            'positive': positive,
            'negative': negative,
            'neutral': neutral
        },
        'average_rating': round(avg_rating, 2),
        'feedback_types': types_data
    })

@app.route('/api/feedbacks')
@auth_required
def get_feedbacks():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    time_filter = request.args.get('time_filter', 'all')
    
    query = Feedback.query
    if time_filter == '10days':
        cutoff_date = datetime.utcnow() - timedelta(days=10)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    elif time_filter == '1month':
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    
    feedbacks = query.order_by(Feedback.timestamp.desc()).all()
    return jsonify([feedback.to_dict() for feedback in feedbacks])

@app.route('/api/feedback/<int:feedback_id>', methods=['DELETE'])
@auth_required
def delete_feedback(feedback_id):
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    feedback = Feedback.query.get(feedback_id)
    if not feedback:
        return jsonify({'success': False, 'message': 'Feedback not found'}), 404
    
    if feedback.image_path:
        image_full_path = os.path.join(app.config['UPLOAD_FOLDER'], feedback.image_path)
        if os.path.exists(image_full_path):
            os.remove(image_full_path)
    
    db.session.delete(feedback)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Feedback deleted successfully'})

@app.route('/api/category-sentiment')
@auth_required
def get_category_sentiment():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    time_filter = request.args.get('time_filter', 'all')
    
    query = Feedback.query
    if time_filter == '10days':
        cutoff_date = datetime.utcnow() - timedelta(days=10)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    elif time_filter == '1month':
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Feedback.timestamp >= cutoff_date)
    
    category_sentiment_result = db.session.query(
        Feedback.feedback_type,
        Feedback.sentiment,
        db.func.count(Feedback.id)
    )
    
    if time_filter == '10days':
        cutoff_date = datetime.utcnow() - timedelta(days=10)
        category_sentiment_result = category_sentiment_result.filter(Feedback.timestamp >= cutoff_date)
    elif time_filter == '1month':
        cutoff_date = datetime.utcnow() - timedelta(days=30)
        category_sentiment_result = category_sentiment_result.filter(Feedback.timestamp >= cutoff_date)
    
    category_sentiment = category_sentiment_result.group_by(
        Feedback.feedback_type,
        Feedback.sentiment
    ).all()
    
    data = {}
    for category, sentiment, count in category_sentiment:
        key = f"{category} - {sentiment}"
        data[key] = count
    
    return jsonify(data)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/admin/export/csv')
@auth_required
def export_csv():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['ID', 'Name', 'Email', 'Type', 'Text', 'Rating', 'Sentiment', 'Score', 'Image','timestamp'])
    
    for feedback in feedbacks:
        writer.writerow([
            feedback.id,
            feedback.name,
            feedback.email or '',
            feedback.feedback_type,
            feedback.text,
            feedback.rating or 'N/A',
            feedback.sentiment,
            round(feedback.score, 3),
            'Yes' if feedback.image_path else 'No',
            feedback.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    from flask import Response
    response = Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=feedback_data.csv'}
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/admin/export/pdf')
@auth_required
def export_pdf():
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    feedbacks = Feedback.query.order_by(Feedback.timestamp.desc()).all()
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
    )
    
    elements.append(Paragraph("FeedbackHub Analysis Report", title_style))
    elements.append(Spacer(1, 12))
    
    total_feedback = len(feedbacks)
    positive = sum(1 for f in feedbacks if f.sentiment == 'Positive')
    negative = sum(1 for f in feedbacks if f.sentiment == 'Negative')
    neutral = sum(1 for f in feedbacks if f.sentiment == 'Neutral')
    
    feedbacks_with_rating = [f for f in feedbacks if f.rating is not None]
    avg_rating = sum([f.rating for f in feedbacks_with_rating]) / len(feedbacks_with_rating) if feedbacks_with_rating else 0
    
    feedbacks_with_images = sum(1 for f in feedbacks if f.image_path)
    
    summary_data = [
        ['Metric', 'Value'],
        ['Total Feedback', str(total_feedback)],
        ['Average Rating', f"{avg_rating:.2f}/5"],
        ['Positive Sentiment', f"{positive} ({positive/total_feedback*100:.1f}%)" if total_feedback > 0 else "0"],
        ['Negative Sentiment', f"{negative} ({negative/total_feedback*100:.1f}%)" if total_feedback > 0 else "0"],
        ['Neutral Sentiment', f"{neutral} ({neutral/total_feedback*100:.1f}%)" if total_feedback > 0 else "0"],
        ['Feedbacks with Images', str(feedbacks_with_images)]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    elements.append(Paragraph("Detailed Feedback", styles['Heading2']))
    elements.append(Spacer(1, 12))
    
    feedback_data = [['ID', 'Name', 'Email', 'Type', 'Rating', 'Sentiment', 'Image']]
    
    for feedback in feedbacks[:50]:
        feedback_data.append([
            str(feedback.id),
            feedback.name[:20],
            feedback.email or '',
            feedback.feedback_type[:15],
            str(feedback.rating) if feedback.rating else 'N/A',
            feedback.sentiment,
            'Yes' if feedback.image_path else 'No'
        ])

    feedback_table = Table(feedback_data, colWidths=[0.5*inch, 1.5*inch, 1.8*inch, 1.2*inch, 0.8*inch, 1*inch, 0.7*inch])
    feedback_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2ecc71')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(feedback_table)
    
    doc.build(elements)
    buffer.seek(0)
    
    from flask import Response
    response = Response(
        buffer.getvalue(),
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=feedback_report.pdf'}
    )
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def init_db():
    with app.app_context():
        db.create_all()

        try:
            conn = db.engine.connect()
            pragma = conn.execute(sql_text("PRAGMA table_info('feedback')")).fetchall()
            columns = [row[1] for row in pragma]
            if 'email' not in columns:
                print("Adding 'email' column to feedback table...")
                conn.execute(sql_text("ALTER TABLE feedback ADD COLUMN email VARCHAR(120)"))
                print("'email' column added.")
            conn.close()
        except Exception as e:
            print('Could not ensure email column exists:', e)
        
        if not User.query.filter_by(email='admin@example.com').first():
            admin = User(
                name='Admin',
                email='admin@example.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print('Admin user created')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)


@app.after_request
def add_no_cache_headers(response):
    try:
        if current_user.is_authenticated:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0, private'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
    except Exception:
        pass
    return response
