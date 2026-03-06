from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.trade_analysis_model import TradeAnalysis
from utils.ai_analysis import analyze_trade_results, analyze_chart_screenshot
from utils.file_parser import parse_trade_file
from app import db
import os
import threading

analysis = Blueprint('analysis', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@analysis.route('/analysis')
@login_required
def index():
    analyses = TradeAnalysis.query.filter_by(user_id=current_user.id)\
        .order_by(TradeAnalysis.upload_date.desc()).all()
    return render_template('analysis.html', analyses=analyses)

@analysis.route('/analysis/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_ext = filename.rsplit('.', 1)[1].lower()
            
            # Determine file type and analysis type
            if file_ext in ['png', 'jpg', 'jpeg']:
                analysis_type = 'chart_screenshot'
                subfolder = 'screenshots'
            else:
                analysis_type = 'trade_results'
                subfolder = 'documents'
            
            # Save file
            unique_filename = f"{current_user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder, unique_filename)
            file.save(file_path)
            
            # Create analysis record
            trade_analysis = TradeAnalysis(
                user_id=current_user.id,
                file_name=filename,
                file_path=file_path,
                file_type=file_ext,
                analysis_type=analysis_type,
                status='pending'
            )
            db.session.add(trade_analysis)
            db.session.commit()
            
            # Process analysis in background
            thread = threading.Thread(
                target=process_analysis,
                args=(trade_analysis.id, current_app._get_current_object())
            )
            thread.start()
            
            flash('File uploaded successfully! Analysis is processing.', 'success')
            return redirect(url_for('analysis.result', id=trade_analysis.id))
        
        flash('Invalid file type.', 'error')
        return redirect(request.url)
    
    return render_template('analysis_upload.html')

def process_analysis(analysis_id, app):
    with app.app_context():
        analysis = TradeAnalysis.query.get(analysis_id)
        if not analysis:
            return
        
        analysis.status = 'processing'
        analysis.processing_started_at = datetime.utcnow()
        db.session.commit()
        
        try:
            # Parse file content
            file_content = parse_trade_file(analysis.file_path, analysis.file_type)
            
            # Perform AI analysis
            if analysis.analysis_type == 'chart_screenshot':
                result = analyze_chart_screenshot(analysis.file_path)
            else:
                result = analyze_trade_results(file_content)
            
            # Update analysis with results
            analysis.trader_score = result.get('trader_score')
            analysis.trader_classification = result.get('classification')
            analysis.win_rate = result.get('win_rate')
            analysis.risk_reward_ratio = result.get('risk_reward_ratio')
            analysis.trade_frequency = result.get('trade_frequency')
            analysis.consistency_score = result.get('consistency_score')
            analysis.risk_management_score = result.get('risk_management_score')
            analysis.psychology_score = result.get('psychology_score')
            analysis.set_strengths(result.get('strengths', []))
            analysis.set_weaknesses(result.get('weaknesses', []))
            analysis.set_mistakes(result.get('mistakes', []))
            analysis.set_recommendations(result.get('recommendations', []))
            analysis.improvement_strategy = result.get('improvement_strategy')
            analysis.market_structure_analysis = result.get('market_structure')
            analysis.ai_full_response = result.get('full_response')
            analysis.status = 'completed'
            analysis.completed_at = datetime.utcnow()
            
        except Exception as e:
            analysis.status = 'failed'
            analysis.ai_full_response = str(e)
        
        db.session.commit()

@analysis.route('/analysis/<int:id>')
@login_required
def result(id):
    analysis = TradeAnalysis.query.get_or_404(id)
    
    if analysis.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    return render_template('analysis_result.html', analysis=analysis)

@analysis.route('/analysis/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    analysis = TradeAnalysis.query.get_or_404(id)
    
    if analysis.user_id != current_user.id and not current_user.is_admin:
        abort(403)
    
    # Delete file
    if os.path.exists(analysis.file_path):
        os.remove(analysis.file_path)
    
    db.session.delete(analysis)
    db.session.commit()
    
    flash('Analysis deleted successfully.', 'success')
    return redirect(url_for('analysis.index'))

from datetime import datetime
from flask import abort
