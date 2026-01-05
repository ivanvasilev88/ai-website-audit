#!/usr/bin/env python3
"""
Python version of the AI Website Audit server
Uses Flask instead of Express
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import sys

app = Flask(__name__, static_folder='.')
CORS(app)

def perform_ai_audit(url):
    """Perform AI audit on a website"""
    try:
        # Fetch the website
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }, timeout=10, allow_redirects=True)
        response.raise_for_status()
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        audit_results = []
        total_score = 0
        max_score = 0
        
        # 1. Check for title tag
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''
        title_score = 10 if title else 0
        audit_results.append({
            'name': 'Has Title Tag',
            'points': title_score,
            'maxPoints': 10,
            'status': 'pass' if title_score == 10 else 'fail'
        })
        total_score += title_score
        max_score += 10
        
        # 2. Check for meta description
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_desc_tag.get('content', '') if meta_desc_tag else ''
        meta_desc_score = 10 if meta_description and len(meta_description) > 50 else (5 if meta_description else 0)
        audit_results.append({
            'name': 'Has Meta Description',
            'points': meta_desc_score,
            'maxPoints': 10,
            'status': 'pass' if meta_desc_score == 10 else ('warning' if meta_desc_score == 5 else 'fail')
        })
        total_score += meta_desc_score
        max_score += 10
        
        # 3. Check for structured data (JSON-LD, microdata)
        json_ld = len(soup.find_all('script', type='application/ld+json'))
        microdata = len(soup.find_all(attrs={'itemscope': True}))
        structured_data_score = 15 if json_ld > 0 else (10 if microdata > 0 else 0)
        audit_results.append({
            'name': 'Structured Data (Schema.org)',
            'points': structured_data_score,
            'maxPoints': 15,
            'status': 'pass' if structured_data_score >= 10 else 'fail'
        })
        total_score += structured_data_score
        max_score += 15
        
        # 4. Check for semantic HTML
        semantic_elements = soup.find_all(['header', 'nav', 'main', 'article', 'section', 'aside', 'footer'])
        semantic_count = len(semantic_elements)
        semantic_score = 15 if semantic_count >= 3 else (8 if semantic_count > 0 else 0)
        audit_results.append({
            'name': 'Semantic HTML Elements',
            'points': semantic_score,
            'maxPoints': 15,
            'status': 'pass' if semantic_score >= 10 else ('warning' if semantic_score > 0 else 'fail')
        })
        total_score += semantic_score
        max_score += 15
        
        # 5. Check for alt text on images
        images = soup.find_all('img')
        images_count = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        alt_text_score = 10 if images_count == 0 else round((images_with_alt / images_count) * 10)
        audit_results.append({
            'name': 'Image Alt Text',
            'points': alt_text_score,
            'maxPoints': 10,
            'status': 'pass' if alt_text_score >= 8 else ('warning' if alt_text_score >= 5 else 'fail')
        })
        total_score += alt_text_score
        max_score += 10
        
        # 6. Check for heading hierarchy
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h1_count = len(h1_tags)
        h2_count = len(h2_tags)
        heading_score = 10 if h1_count == 1 and h2_count > 0 else (7 if h1_count == 1 else (5 if h1_count > 0 else 0))
        audit_results.append({
            'name': 'Proper Heading Hierarchy',
            'points': heading_score,
            'maxPoints': 10,
            'status': 'pass' if heading_score >= 7 else ('warning' if heading_score > 0 else 'fail')
        })
        total_score += heading_score
        max_score += 10
        
        # 7. Check for Open Graph tags
        og_tags = soup.find_all('meta', attrs={'property': lambda x: x and x.startswith('og:')})
        og_count = len(og_tags)
        og_score = 10 if og_count >= 3 else (5 if og_count > 0 else 0)
        audit_results.append({
            'name': 'Open Graph Tags',
            'points': og_score,
            'maxPoints': 10,
            'status': 'pass' if og_score >= 7 else ('warning' if og_score > 0 else 'fail')
        })
        total_score += og_score
        max_score += 10
        
        # 8. Check for robots meta tag
        robots_meta = soup.find('meta', attrs={'name': 'robots'})
        robots_content = robots_meta.get('content', '') if robots_meta else ''
        robots_score = 10 if not robots_content or 'noindex' not in robots_content else 0
        audit_results.append({
            'name': 'Crawlable by AI (Robots)',
            'points': robots_score,
            'maxPoints': 10,
            'status': 'pass' if robots_score == 10 else 'fail'
        })
        total_score += robots_score
        max_score += 10
        
        # Calculate final score
        final_score = round((total_score / max_score) * 100) if max_score > 0 else 0
        
        return {
            'score': final_score,
            'details': audit_results
        }
    except Exception as error:
        raise Exception(f'Failed to fetch or analyze website: {str(error)}')

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', path)

@app.route('/api/scan', methods=['POST'])
def scan():
    """API endpoint to scan a website"""
    try:
        data = request.get_json()
        url = data.get('url') if data else None
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate URL format
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.scheme.startswith('http'):
                return jsonify({'error': 'URL must use http or https protocol'}), 400
        except Exception:
            return jsonify({'error': 'Invalid URL format'}), 400
        
        audit_result = perform_ai_audit(url)
        return jsonify(audit_result)
    except Exception as error:
        print(f'Error scanning website: {error}', file=sys.stderr)
        return jsonify({
            'error': str(error) if str(error) else 'An error occurred while scanning the website'
        }), 500

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    print(f'Server running on http://localhost:{port}')
    app.run(host='0.0.0.0', port=port, debug=True)


