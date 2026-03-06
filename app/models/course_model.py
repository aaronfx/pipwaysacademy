from app import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    featured_image = db.Column(db.String(255))
    level = db.Column(db.String(50))  # beginner, intermediate, advanced, all-levels
    category = db.Column(db.String(100))
    price = db.Column(db.Float, default=0.0)
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    duration_hours = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    modules = db.relationship('Module', backref='course', lazy=True, cascade='all, delete-orphan', order_by='Module.order')
    enrollments = db.relationship('CourseEnrollment', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def get_modules_count(self):
        return len(self.modules)
    
    def get_lessons_count(self):
        return sum(len(module.lessons) for module in self.modules)
    
    def get_enrolled_students_count(self):
        return CourseEnrollment.query.filter_by(course_id=self.id).count()
    
    def get_total_duration(self):
        total = 0
        for module in self.modules:
            for lesson in module.lessons:
                if lesson.duration_minutes:
                    total += lesson.duration_minutes
        return total

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan', order_by='Lesson.order')

class Lesson(db.Model):
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)  # HTML content
    video_url = db.Column(db.String(500))
    video_file = db.Column(db.String(255))
    pdf_file = db.Column(db.String(255))
    duration_minutes = db.Column(db.Integer)
    order = db.Column(db.Integer, default=0)
    is_published = db.Column(db.Boolean, default=True)
    is_free_preview = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('CourseProgress', backref='lesson', lazy=True, cascade='all, delete-orphan')

class CourseEnrollment(db.Model):
    __tablename__ = 'course_enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active')  # active, completed, dropped
    progress_percentage = db.Column(db.Float, default=0.0)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'course_id', name='unique_enrollment'),)

class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='unique_progress'),)
