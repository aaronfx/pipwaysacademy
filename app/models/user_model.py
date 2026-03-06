from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    bio = db.Column(db.Text)
    avatar = db.Column(db.String(255))
    trading_experience = db.Column(db.String(50))  # beginner, intermediate, advanced
    preferred_market = db.Column(db.String(50))  # forex, stocks, crypto, etc.
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    analyses = db.relationship('TradeAnalysis', backref='user', lazy=True, cascade='all, delete-orphan')
    webinar_registrations = db.relationship('WebinarRegistration', backref='user', lazy=True, cascade='all, delete-orphan')
    course_progress = db.relationship('CourseProgress', backref='user', lazy=True, cascade='all, delete-orphan')
    enrollments = db.relationship('CourseEnrollment', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[:2].upper()
    
    def get_active_courses_count(self):
        return CourseEnrollment.query.filter_by(user_id=self.id, status='active').count()
    
    def get_completed_analyses_count(self):
        return TradeAnalysis.query.filter_by(user_id=self.id).count()
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
