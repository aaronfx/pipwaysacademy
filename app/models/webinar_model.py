from app import db
from datetime import datetime

class Webinar(db.Model):
    __tablename__ = 'webinars'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_description = db.Column(db.String(500))
    featured_image = db.Column(db.String(255))
    
    # Schedule
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    timezone = db.Column(db.String(50), default='UTC')
    
    # Links
    meeting_link = db.Column(db.String(500))  # Zoom, Google Meet, etc.
    recording_link = db.Column(db.String(500))
    youtube_link = db.Column(db.String(500))
    
    # Settings
    max_participants = db.Column(db.Integer)
    is_featured = db.Column(db.Boolean, default=False)
    is_recorded = db.Column(db.Boolean, default=False)
    recording_available = db.Column(db.Boolean, default=False)
    
    # Status
    status = db.Column(db.String(50), default='upcoming')  # upcoming, live, ended, cancelled
    
    # Presenter
    presenter_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    presenter_name = db.Column(db.String(100))
    presenter_bio = db.Column(db.Text)
    presenter_image = db.Column(db.String(255))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('WebinarRegistration', backref='webinar', lazy=True, cascade='all, delete-orphan')
    
    def get_registered_count(self):
        return WebinarRegistration.query.filter_by(webinar_id=self.id).count()
    
    def get_available_spots(self):
        if self.max_participants:
            return max(0, self.max_participants - self.get_registered_count())
        return None
    
    def is_full(self):
        if self.max_participants:
            return self.get_registered_count() >= self.max_participants
        return False
    
    def update_status(self):
        now = datetime.utcnow()
        if self.status == 'cancelled':
            return
        if now < self.start_time:
            self.status = 'upcoming'
        elif self.start_time <= now <= self.end_time if self.end_time else True:
            self.status = 'live'
        else:
            self.status = 'ended'
        db.session.commit()

class WebinarRegistration(db.Model):
    __tablename__ = 'webinar_registrations'
    
    id = db.Column(db.Integer, primary_key=True)
    webinar_id = db.Column(db.Integer, db.ForeignKey('webinars.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    attended = db.Column(db.Boolean, default=False)
    attendance_time = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    
    __table_args__ = (db.UniqueConstraint('webinar_id', 'user_id', name='unique_webinar_registration'),)
