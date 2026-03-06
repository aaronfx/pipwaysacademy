from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.course_model import Course, CourseEnrollment
from models.webinar_model import Webinar, WebinarRegistration
from models.trade_analysis_model import TradeAnalysis
from models.blog_model import BlogPost
from datetime import datetime

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@dashboard.route('/dashboard')
@login_required
def index():
    # Get user's active courses
    active_courses = CourseEnrollment.query.filter_by(
        user_id=current_user.id,
        status='active'
    ).all()
    
    # Get upcoming webinars
    registered_webinars = WebinarRegistration.query.filter_by(
        user_id=current_user.id
    ).join(Webinar).filter(Webinar.start_time > datetime.utcnow()).all()
    
    # Get recent analyses
    recent_analyses = TradeAnalysis.query.filter_by(
        user_id=current_user.id,
        status='completed'
    ).order_by(TradeAnalysis.completed_at.desc()).limit(5).all()
    
    # Get featured blog posts
    featured_posts = BlogPost.query.filter_by(
        status='published',
        is_featured=True
    ).order_by(BlogPost.published_at.desc()).limit(3).all()
    
    # Statistics
    stats = {
        'active_courses': len(active_courses),
        'upcoming_webinars': len(registered_webinars),
        'total_analyses': TradeAnalysis.query.filter_by(user_id=current_user.id).count(),
        'avg_trader_score': db.session.query(db.func.avg(TradeAnalysis.trader_score))
            .filter_by(user_id=current_user.id).scalar() or 0
    }
    
    return render_template('dashboard.html',
                         active_courses=active_courses,
                         registered_webinars=registered_webinars,
                         recent_analyses=recent_analyses,
                         featured_posts=featured_posts,
                         stats=stats)

@dashboard.route('/my-courses')
@login_required
def my_courses():
    enrollments = CourseEnrollment.query.filter_by(user_id=current_user.id).all()
    return render_template('my_courses.html', enrollments=enrollments)

@dashboard.route('/my-webinars')
@login_required
def my_webinars():
    registrations = WebinarRegistration.query.filter_by(user_id=current_user.id)\
        .join(Webinar).order_by(Webinar.start_time.desc()).all()
    return render_template('my_webinars.html', registrations=registrations)

@dashboard.route('/my-analyses')
@login_required
def my_analyses():
    analyses = TradeAnalysis.query.filter_by(user_id=current_user.id)\
        .order_by(TradeAnalysis.upload_date.desc()).all()
    return render_template('my_analyses.html', analyses=analyses)
