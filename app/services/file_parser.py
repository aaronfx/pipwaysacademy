import csv
import io
import re
from PyPDF2 import PdfReader
import pandas as pd

def parse_trade_file(file_path, file_type):
    """Parse various trade file formats and extract trading data"""
    
    content = ""
    
    try:
        if file_type in ['txt', 'csv']:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
        elif file_type == 'pdf':
            reader = PdfReader(file_path)
            for page in reader.pages:
                content += page.extract_text() + "\n"
                
        elif file_type in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
            content = df.to_string()
            
        elif file_type in ['doc', 'docx']:
            try:
                from docx import Document
                doc = Document(file_path)
                for para in doc.paragraphs:
                    content += para.text + "\n"
            except:
                content = "Document parsing limited. Please convert to text or PDF for better analysis."
        
        # Extract trading metrics using regex patterns
        metrics = extract_trading_metrics(content)
        
        # Format for AI analysis
        formatted_data = format_trade_data(content, metrics)
        
        return formatted_data
        
    except Exception as e:
        return f"Error parsing file: {str(e)}\n\nRaw content preview:\n{content[:2000]}"

def extract_trading_metrics(text):
    """Extract key trading metrics from text"""
    metrics = {}
    
    # Win rate patterns
    win_rate_patterns = [
        r'win\s*rate[:\s]+(\d+\.?\d*)%',
        r'winning\s*percentage[:\s]+(\d+\.?\d*)%',
        r'(\d+\.?\d*)%\s*win',
        r'win\s*ratio[:\s]+(\d+\.?\d*)%'
    ]
    
    for pattern in win_rate_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics['win_rate'] = float(match.group(1))
            break
    
    # Profit/loss patterns
    profit_patterns = [
        r'profit[:\s]+\$?([\d,]+\.?\d*)',
        r'net\s*profit[:\s]+\$?([\d,]+\.?\d*)',
        r'total\s*profit[:\s]+\$?([\d,]+\.?\d*)',
        r'p&l[:\s]+\$?([\d,]+\.?\d*)'
    ]
    
    for pattern in profit_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics['profit'] = match.group(1).replace(',', '')
            break
    
    # Trade count patterns
    trade_patterns = [
        r'total\s*trades[:\s]+(\d+)',
        r'number\s*of\s*trades[:\s]+(\d+)',
        r'trades\s*taken[:\s]+(\d+)',
        r'(\d+)\s*trades'
    ]
    
    for pattern in trade_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            metrics['total_trades'] = int(match.group(1))
            break
    
    # Risk-Reward patterns
    rr_patterns = [
        r'risk[:\s]+reward[:\s]+(\d+[:\.]\d+)',
        r'r:r[:\s]+(\d+[:\.]\d+)',
        r'risk\s*reward\s*ratio[:\s]+(\d+[:\.]\d+)'
    ]
    
    for pattern in rr_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rr = match.group(1).replace(':', '.')
            metrics['risk_reward'] = float(rr)
            break
    
    return metrics

def format_trade_data(raw_content, metrics):
    """Format extracted data for AI analysis"""
    
    formatted = f"""TRADING PERFORMANCE REPORT

EXTRACTED METRICS:
"""
    
    for key, value in metrics.items():
        formatted += f"- {key.replace('_', ' ').title()}: {value}\n"
    
    formatted += f"""
RAW TRADING DATA:
{raw_content[:8000]}

INSTRUCTION FOR AI:
Please analyze this trading data comprehensively. If specific metrics appear inconsistent or unclear from the data, note this in your analysis. Focus on identifying patterns in the raw trade data that indicate trading behavior, strategy effectiveness, and areas for improvement.
"""
    
    return formatted

def parse_mt4_report(file_path):
    """Specialized parser for MT4 strategy tester reports"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # MT4 specific parsing logic
    sections = {
        'summary': '',
        'trades': '',
        'statistics': ''
    }
    
    # Extract key MT4 sections
    lines = content.split('\n')
    current_section = None
    
    for line in lines:
        if 'Strategy Tester Report' in line:
            current_section = 'summary'
        elif 'Orders' in line or 'Deals' in line:
            current_section = 'trades'
        elif 'Summary' in line or 'Statistics' in line:
            current_section = 'statistics'
        
        if current_section and line.strip():
            sections[current_section] += line + '\n'
    
    return format_trade_data(content, extract_trading_metrics(content))
