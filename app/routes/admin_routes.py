from flask import Blueprint, render_template, request, flash, redirect, url_for, abort, jsonify
from flask_login import login_required, current_user
from functools import wraps
from app import db
from models.user_model import User
from models.course_model import Course, Module, Lesson
from models.blog_model import BlogPost, BlogCategory
from models.webinar_model import Webinar, WebinarRegistration
from models.trade_analysis_model import TradeAnalysis
from datetime import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    # Statistics
    stats = {
        'total_users': User.query.count(),
        'total_courses': Course.query.count(),
        'total_blog_posts': BlogPost.query.count(),
        'total_webinars': Webinar.query.count(),
        'total_analyses': TradeAnalysis.query.count(),
        'active_enrollments': db.session.query(db.func.count(CourseEnrollment.id)).scalar(),
        'webinar_registrations': WebinarRegistration.query.count(),
        'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all(),
        'recent_analyses': TradeAnalysis.query.order_by(TradeAnalysis.upload_date.desc()).limit(5).all()
    }
    
    return render_template('admin/dashboard.html', stats=stats)

# User Management
@admin.route('/users')
@login_required
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    users_list = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('admin/users.html', users=users_list)

@admin.route('/users/<int:id>/toggle-status', methods=['POST'])
@login_required
@admin_required
def toggle_user_status(id):
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('You cannot deactivate yourself.', 'error')
        return redirect(url_for('admin.users'))
    
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {status} successfully.', 'success')
    return redirect(url_for('admin.users'))

# Course Management
@admin.route('/courses')
@login_required
@admin_required
def courses():
    courses_list = Course.query.order_by(Course.created_at.desc()).all()
    return render_template('admin/courses.html', courses=courses_list)

@admin.route('/courses/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    if request.method == 'POST':
        course = Course(
            title=request.form.get('title'),
            slug=request.form.get('slug'),
            description=request.form.get('description'),
            short_description=request.form.get('short_description'),
            level=request.form.get('level'),
            category=request.form.get('category'),
            price=float(request.form.get('price', 0)),
            is_published=bool(request.form.get('is_published')),
            is_featured=bool(request.form.get('is_featured')),
            duration_hours=float(request.form.get('duration_hours', 0)),
            instructor_id=current_user.id
        )
        
        # Handle featured image
        if 'featured_image' in request.files:
            file = request.files['featured_image']
            if file.filename:
                filename = secure_filename(f"course_{course.slug}_{file.filename}")
                file.save(os.path.join('static', 'images', 'courses', filename))
                course.featured_image = f"images/courses/{filename}"
        
        db.session.add(course)
        db.session.commit()
        
        flash('Course created successfully!', 'success')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_form.html', course=None)

@admin.route('/courses/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    
    if request.method == 'POST':
        course.title = request.form.get('title')
        course.slug = request.form.get('slug')
        course.description = request.form.get('description')
        course.short_description = request.form.get('short_description')
        course.level = request.form.get('level')
        course.category = request.form.get('category')
        course.price = float(request.form.get('price', 0))
        course.is_published = bool(request.form.get('is_published'))
        course.is_featured = bool(request.form.get('is_featured'))
        course.duration_hours = float(request.form.get('duration_hours', 0))
        
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin.courses'))
    
    return render_template('admin/course_form.html', course=course)

@admin.route('/courses/<int:course_id>/modules/create', methods=['POST'])
@login_required
@admin_required
def create_module(course_id):
    course = Course.query.get_or_404(course_id)
    
    module = Module(
        course_id=course_id,
        title=request.form.get('title'),
        description=request.form.get('description'),
        order=len(course.modules) + 1
    )
    
    db.session.add(module)
    db.session.commit()
    
    flash('Module added successfully!', 'success')
    return redirect(url_for('admin.edit_course', id=course_id))

@admin.route('/modules/<int:module_id>/lessons/create', methods=['POST'])
@login_required
@admin_required
def create_lesson(module_id):
    module = Module.query.get_or_404(module_id)
    
    lesson = Lesson(
        module_id=module_id,
        title=request.form.get('title'),
        description=request.form.get('description'),
        content=request.form.get('content'),
        video_url=request.form.get('video_url'),
        duration_minutes=int(request.form.get('duration_minutes', 0)),
        is_free_preview=bool(request.form.get('is_free_preview')),
        order=len(module.lessons) + 1
    )
    
    # Handle video file upload
    if 'video_file' in request.files:
        file = request.files['video_file']
        if file.filename:
            filename = secure_filename(f"lesson_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'courses', filename))
            lesson.video_file = filename
    
    # Handle PDF upload
    if 'pdf_file' in request.files:
        file = request.files['pdf_file']
        if file.filename:
            filename = secure_filename(f"lesson_pdf_{file.filename}")
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], 'courses', filename))
            lesson.pdf_file = filename
    
    db.session.add(lesson)
    db.session.commit()
    
    flash('Lesson added successfully!', 'success')
    return redirect(url_for('admin.edit_course', id=module.course_id))

# Blog Management
@admin.route('/blog')
@login_required
@admin_required
def blog_posts():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog_posts.html', posts=posts)

# Webinar Management
@admin.route('/webinars')
@login_required
@admin_required
def webinars():
    webinars_list = Webinar.query.order_by(Webinar.start_time.desc()).all()
    return render_template('admin/webinars.html', webinars=webinars_list)

@admin.route('/webinars/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_webinar():
    if request.method == 'POST':
        webinar = Webinar(
            title=request.form.get('title'),
            description=request.form.get('description'),
            short_description=request.form.get('short_description'),
            start_time=datetime.fromisoformat(request.form.get('start_time')),
            end_time=datetime.fromisoformat(request.form.get('end_time')) if request.form.get('end_time') else None,
            timezone=request.form.get('timezone', 'UTC'),
            meeting_link=request.form.get('meeting_link'),
            max_participants=int(request.form.get('max_participants')) if request.form.get('max_participants') else None,
            presenter_name=request.form.get('presenter_name'),
            presenter_bio=request.form.get('presenter_bio'),
            is_featured=bool(request.form.get('is_featured'))
        )
        
        db.session.add(webinar)
        db.session.commit()
        
        flash('Webinar created successfully!', 'success')
        return redirect(url_for('admin.webinars'))
    
    return render_template('admin/webinar_form.html', webinar=None)

# Analysis Monitoring
@admin.route('/analyses')
@login_required
@admin_required
def analyses():
    analyses_list = TradeAnalysis.query.order_by(TradeAnalysis.upload_date.desc()).all()
    return render_template('admin/analyses.html', analyses=analyses_list)

from werkzeug.utils import secure_filename
import os
from flask import current_app
from models.course_model import CourseEnrollment
