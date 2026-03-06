from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models.course_model import Course, Module, Lesson, CourseEnrollment, CourseProgress
from app import db
from datetime import datetime

courses = Blueprint('courses', __name__)

@courses.route('/courses')
def index():
    page = request.args.get('page', 1, type=int)
    level = request.args.get('level')
    category = request.args.get('category')
    
    query = Course.query.filter_by(is_published=True)
    
    if level:
        query = query.filter_by(level=level)
    if category:
        query = query.filter_by(category=category)
    
    courses_list = query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    # Get filter options
    levels = db.session.query(Course.level).distinct().all()
    categories = db.session.query(Course.category).distinct().all()
    
    return render_template('courses.html',
                         courses=courses_list,
                         levels=[l[0] for l in levels if l[0]],
                         categories=[c[0] for c in categories if c[0]])

@courses.route('/courses/<string:slug>')
def view(slug):
    course = Course.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Check enrollment
    enrollment = None
    if current_user.is_authenticated:
        enrollment = CourseEnrollment.query.filter_by(
            user_id=current_user.id,
            course_id=course.id
        ).first()
    
    return render_template('course_view.html', course=course, enrollment=enrollment)

@courses.route('/courses/<string:slug>/enroll', methods=['POST'])
@login_required
def enroll(slug):
    course = Course.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Check if already enrolled
    existing = CourseEnrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id
    ).first()
    
    if existing:
        flash('You are already enrolled in this course.', 'info')
        return redirect(url_for('courses.view', slug=slug))
    
    enrollment = CourseEnrollment(
        user_id=current_user.id,
        course_id=course.id,
        status='active'
    )
    db.session.add(enrollment)
    db.session.commit()
    
    flash('Successfully enrolled in the course!', 'success')
    return redirect(url_for('courses.learn', slug=slug))

@courses.route('/courses/<string:slug>/learn')
@login_required
def learn(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    
    # Verify enrollment
    enrollment = CourseEnrollment.query.filter_by(
        user_id=current_user.id,
        course_id=course.id,
        status='active'
    ).first_or_404()
    
    # Get current lesson
    lesson_id = request.args.get('lesson', type=int)
    current_lesson = None
    
    if lesson_id:
        current_lesson = Lesson.query.get(lesson_id)
    else:
        # Get first incomplete lesson or last accessed
        progress = CourseProgress.query.filter_by(
            user_id=current_user.id
        ).join(Lesson).filter(
            Lesson.module.has(course_id=course.id)
        ).order_by(CourseProgress.last_accessed.desc()).first()
        
        if progress:
            current_lesson = progress.lesson
        else:
            # Get first lesson of first module
            first_module = Module.query.filter_by(course_id=course.id).order_by(Module.order).first()
            if first_module:
                current_lesson = Lesson.query.filter_by(module_id=first_module.id).order_by(Lesson.order).first()
    
    # Get progress for all lessons
    lesson_progress = {}
    for module in course.modules:
        for lesson in module.lessons:
            prog = CourseProgress.query.filter_by(
                user_id=current_user.id,
                lesson_id=lesson.id
            ).first()
            lesson_progress[lesson.id] = prog.completed if prog else False
    
    # Calculate overall progress
    total_lessons = sum(len(m.lessons) for m in course.modules)
    completed_lessons = sum(1 for v in lesson_progress.values() if v)
    progress_percentage = (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    
    enrollment.progress_percentage = progress_percentage
    db.session.commit()
    
    return render_template('course_learn.html',
                         course=course,
                         current_lesson=current_lesson,
                         lesson_progress=lesson_progress,
                         enrollment=enrollment)

@courses.route('/courses/lesson/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    progress = CourseProgress.query.filter_by(
        user_id=current_user.id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = CourseProgress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.session.add(progress)
    
    progress.completed = True
    progress.completed_at = datetime.utcnow()
    db.session.commit()
    
    # Check if course completed
    course = lesson.module.course
    total_lessons = sum(len(m.lessons) for m in course.modules)
    completed_count = CourseProgress.query.filter_by(
        user_id=current_user.id,
        completed=True
    ).join(Lesson).filter(
        Lesson.module.has(course_id=course.id)
    ).count()
    
    if completed_count >= total_lessons:
        enrollment = CourseEnrollment.query.filter_by(
            user_id=current_user.id,
            course_id=course.id
        ).first()
        if enrollment:
            enrollment.status = 'completed'
            enrollment.completed_at = datetime.utcnow()
            db.session.commit()
            flash('Congratulations! You have completed the course!', 'success')
    
    return redirect(url_for('courses.learn', slug=course.slug, lesson=lesson_id))
