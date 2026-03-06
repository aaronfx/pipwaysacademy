from app import db
from datetime import datetime
import json

class TradeAnalysis(db.Model):
    __tablename__ = 'trade_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Upload Info
    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(500))
    file_type = db.Column(db.String(50))  # pdf, csv, doc, screenshot, etc.
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Analysis Type
    analysis_type = db.Column(db.String(50))  # trade_results, chart_screenshot, journal
    
    # AI Analysis Results (stored as JSON)
    trader_score = db.Column(db.Integer)  # 0-100
    trader_classification = db.Column(db.String(100))  # Beginner, Scalper, etc.
    win_rate = db.Column(db.Float)
    risk_reward_ratio = db.Column(db.Float)
    trade_frequency = db.Column(db.String(50))
    consistency_score = db.Column(db.Float)
    risk_management_score = db.Column(db.Float)
    psychology_score = db.Column(db.Float)
    
    # Detailed Analysis
    strengths = db.Column(db.Text)  # JSON array
    weaknesses = db.Column(db.Text)  # JSON array
    mistakes_detected = db.Column(db.Text)  # JSON array
    recommendations = db.Column(db.Text)  # JSON array
    improvement_strategy = db.Column(db.Text)
    market_structure_analysis = db.Column(db.Text)  # For chart screenshots
    ai_full_response = db.Column(db.Text)  # Complete AI response
    
    # Status
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    processing_started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    def get_strengths_list(self):
        if self.strengths:
            return json.loads(self.strengths)
        return []
    
    def get_weaknesses_list(self):
        if self.weaknesses:
            return json.loads(self.weaknesses)
        return []
    
    def get_mistakes_list(self):
        if self.mistakes_detected:
            return json.loads(self.mistakes_detected)
        return []
    
    def get_recommendations_list(self):
        if self.recommendations:
            return json.loads(self.recommendations)
        return []
    
    def set_strengths(self, strengths_list):
        self.strengths = json.dumps(strengths_list)
    
    def set_weaknesses(self, weaknesses_list):
        self.weaknesses = json.dumps(weaknesses_list)
    
    def set_mistakes(self, mistakes_list):
        self.mistakes_detected = json.dumps(mistakes_list)
    
    def set_recommendations(self, recommendations_list):
        self.recommendations = json.dumps(recommendations_list)
