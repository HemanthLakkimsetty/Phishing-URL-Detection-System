#!/usr/bin/env python3
"""
Web Interface for Safe URL Checker
"""

from flask import Flask, render_template, request, jsonify
from url_checker import SafeURLChecker
import json
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize the URL checker
checker = SafeURLChecker()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/check_url', methods=['POST'])
def check_url():
    """API endpoint to check URL safety"""
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({
                'success': False,
                'error': 'No URL provided'
            })
        
        # Perform URL safety check
        results = checker.check_url_safety_web(url)
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"url_check_{timestamp}.json"
        
        data_to_save = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        
        return jsonify({
            'success': True,
            'results': results,
            'filename': filename
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/check_multiple', methods=['POST'])
def check_multiple_urls():
    """API endpoint to check multiple URLs"""
    try:
        data = request.get_json()
        urls_text = data.get('urls', '').strip()
        
        if not urls_text:
            return jsonify({
                'success': False,
                'error': 'No URLs provided'
            })
        
        # Split URLs by newlines
        urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
        
        if not urls:
            return jsonify({
                'success': False,
                'error': 'No valid URLs found'
            })
        
        all_results = []
        
        for url in urls:
            try:
                results = checker.check_url_safety_web(url)
                all_results.append({
                    'url': url,
                    'results': results
                })
            except Exception as e:
                all_results.append({
                    'url': url,
                    'error': str(e)
                })
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"batch_url_check_{timestamp}.json"
        
        data_to_save = {
            'timestamp': datetime.now().isoformat(),
            'total_urls': len(urls),
            'results': all_results
        }
        
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        
        return jsonify({
            'success': True,
            'results': all_results,
            'filename': filename,
            'total_urls': len(urls)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌐 Starting Safe URL Checker Web Interface...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
