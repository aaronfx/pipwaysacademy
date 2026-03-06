import cv2
import numpy as np
from PIL import Image
import os

def preprocess_chart_image(image_path):
    """Preprocess chart image for better AI analysis"""
    
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Enhance contrast
    lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
    
    # Save preprocessed version
    base, ext = os.path.splitext(image_path)
    preprocessed_path = f"{base}_enhanced{ext}"
    Image.fromarray(enhanced).save(preprocessed_path)
    
    return preprocessed_path

def detect_chart_patterns(image_path):
    """Basic pattern detection in chart screenshots"""
    
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return []
    
    patterns = []
    
    # Detect lines (trend lines, support/resistance)
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
    
    if lines is not None:
        horizontal_lines = 0
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi)
            if angle < 10 or angle > 170:  # Horizontal lines
                horizontal_lines += 1
        
        if horizontal_lines > 5:
            patterns.append("Multiple horizontal levels detected (possible support/resistance)")
    
    # Detect candlestick patterns (green/red detection)
    hsv = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2HSV)
    
    # Green candles
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(green_mask > 0) / (green_mask.shape[0] * green_mask.shape[1])
    
    # Red candles
    lower_red1 = np.array([0, 40, 40])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 40, 40])
    upper_red2 = np.array([180, 255, 255])
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)
    red_ratio = np.sum(red_mask > 0) / (red_mask.shape[0] * red_mask.shape[1])
    
    if green_ratio > red_ratio:
        patterns.append(f"Bullish sentiment detected ({green_ratio:.1%} green vs {red_ratio:.1%} red)")
    else:
        patterns.append(f"Bearish sentiment detected ({red_ratio:.1%} red vs {green_ratio:.1%} green)")
    
    return patterns

def extract_chart_metadata(image_path):
    """Extract metadata from chart image"""
    
    img = Image.open(image_path)
    
    metadata = {
        'size': img.size,
        'mode': img.mode,
        'format': img.format,
        'file_size_kb': os.path.getsize(image_path) / 1024
    }
    
    # Basic color analysis
    img_array = np.array(img)
    if len(img_array.shape) == 3:
        avg_color = np.mean(img_array, axis=(0,1))
        metadata['dominant_color'] = f"RGB({int(avg_color[0])}, {int(avg_color[1])}, {int(avg_color[2])})"
    
    return metadata
