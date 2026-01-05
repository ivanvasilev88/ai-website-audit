#!/usr/bin/env python3
"""
Standalone Python server - NO external dependencies required!
Uses only Python standard library
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
from html.parser import HTMLParser
import json
import urllib.request
import urllib.error
import ssl
import sys
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import uuid
import time
from datetime import datetime
import base64
import os

class HTMLAuditParser(HTMLParser):
    """Custom HTML parser to extract audit information"""
    def __init__(self):
        super().__init__()
        self.title = ''
        self.meta_description = ''
        self.json_ld_count = 0
        self.microdata_count = 0
        self.semantic_elements = []
        self.images = []
        self.headings = {'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0}
        self.og_tags = []
        self.robots_meta = ''
        self.in_title = False
        self.current_tag = None
        self.links = []
        self.forms = []
        self.videos = []
        self.iframes = []
        self.scripts = []
        self.stylesheets = []
        self.lang_attribute = ''
        self.charset = ''
        self.viewport = ''
        self.keywords_meta = ''
        self.author_meta = ''
        self.twitter_card = False
        self.canonical_url = ''
        self.sitemap_reference = False
        self.analytics_tracking = False
        self.content_length = 0
        self.aria_labels = 0
        self.landmarks = 0
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        # Title tag
        if tag == 'title':
            self.in_title = True
            
        # Meta description
        if tag == 'meta' and attrs_dict.get('name') == 'description':
            self.meta_description = attrs_dict.get('content', '')
            
        # Robots meta
        if tag == 'meta' and attrs_dict.get('name') == 'robots':
            self.robots_meta = attrs_dict.get('content', '')
            
        # Open Graph tags
        if tag == 'meta' and attrs_dict.get('property', '').startswith('og:'):
            self.og_tags.append(attrs_dict.get('property', ''))
            
        # JSON-LD
        if tag == 'script' and attrs_dict.get('type') == 'application/ld+json':
            self.json_ld_count += 1
            
        # Microdata
        if 'itemscope' in attrs_dict:
            self.microdata_count += 1
            
        # Semantic elements
        if tag in ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer']:
            self.semantic_elements.append(tag)
            
        # Images
        if tag == 'img':
            self.images.append({
                'has_alt': 'alt' in attrs_dict
            })
            
        # Headings
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings[tag] += 1
            
        # Links
        if tag == 'a':
            href = attrs_dict.get('href', '')
            if href:
                self.links.append(href)
                
        # Forms
        if tag == 'form':
            self.forms.append(attrs_dict)
            
        # Videos
        if tag in ['video', 'iframe']:
            if tag == 'video':
                self.videos.append(attrs_dict)
            else:
                self.iframes.append(attrs_dict)
                
        # Scripts
        if tag == 'script':
            src = attrs_dict.get('src', '')
            if 'analytics' in src.lower() or 'gtag' in src.lower() or 'ga(' in src.lower():
                self.analytics_tracking = True
            self.scripts.append(src)
            
        # Stylesheets
        if tag == 'link' and attrs_dict.get('rel') == 'stylesheet':
            self.stylesheets.append(attrs_dict.get('href', ''))
            
        # Language
        if tag == 'html':
            self.lang_attribute = attrs_dict.get('lang', '')
            
        # Charset
        if tag == 'meta' and attrs_dict.get('charset'):
            self.charset = attrs_dict.get('charset', '')
            
        # Viewport
        if tag == 'meta' and attrs_dict.get('name') == 'viewport':
            self.viewport = attrs_dict.get('content', '')
            
        # Keywords
        if tag == 'meta' and attrs_dict.get('name') == 'keywords':
            self.keywords_meta = attrs_dict.get('content', '')
            
        # Author
        if tag == 'meta' and attrs_dict.get('name') == 'author':
            self.author_meta = attrs_dict.get('content', '')
            
        # Twitter Card
        if tag == 'meta' and attrs_dict.get('name', '').startswith('twitter:'):
            self.twitter_card = True
            
        # Canonical URL
        if tag == 'link' and attrs_dict.get('rel') == 'canonical':
            self.canonical_url = attrs_dict.get('href', '')
            
        # Sitemap reference
        if tag == 'link' and attrs_dict.get('rel') == 'sitemap':
            self.sitemap_reference = True
            
        # ARIA labels and landmarks
        if 'aria-label' in attrs_dict or 'aria-labelledby' in attrs_dict:
            self.aria_labels += 1
        if tag in ['header', 'nav', 'main', 'article', 'section', 'aside', 'footer'] or 'role' in attrs_dict:
            self.landmarks += 1
            
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
            
    def handle_data(self, data):
        if self.in_title:
            self.title += data
        self.content_length += len(data)

def perform_ai_audit(url):
    """Perform AI audit on a website using only standard library"""
    try:
        # Create SSL context that doesn't verify certificates (for testing)
        # This allows us to test HTTPS sites without certificate issues
        ssl_context = ssl._create_unverified_context()
        
        # Fetch the website with comprehensive browser headers to avoid 403 errors
        # Note: We don't include Accept-Encoding because urllib doesn't auto-decompress
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        req = urllib.request.Request(url, headers=headers)
        
        # Use the unverified SSL context for HTTPS connections
        # Handle 403 errors by retrying with simpler headers
        try:
            response = urllib.request.urlopen(req, timeout=10, context=ssl_context)
        except urllib.error.HTTPError as e:
            # Some sites return 403 even with good headers - try with minimal headers
            if e.code == 403:
                # Retry with just User-Agent
                simple_headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                }
                req = urllib.request.Request(url, headers=simple_headers)
                try:
                    response = urllib.request.urlopen(req, timeout=10, context=ssl_context)
                except urllib.error.HTTPError as e2:
                    if e2.code == 403:
                        raise Exception('Website blocked the request (403 Forbidden). Some websites block automated requests for security reasons. Try a different website or contact the website owner.')
                    raise
            else:
                raise
        
        html = response.read().decode('utf-8', errors='ignore')
        
        # Parse HTML
        parser = HTMLAuditParser()
        parser.feed(html)
        
        audit_results = []
        total_score = 0
        max_score = 0
        
        # 1. Check for title tag
        title = parser.title.strip()
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
        meta_description = parser.meta_description
        meta_desc_score = 10 if meta_description and len(meta_description) > 50 else (5 if meta_description else 0)
        audit_results.append({
            'name': 'Has Meta Description',
            'points': meta_desc_score,
            'maxPoints': 10,
            'status': 'pass' if meta_desc_score == 10 else ('warning' if meta_desc_score == 5 else 'fail')
        })
        total_score += meta_desc_score
        max_score += 10
        
        # 3. Check for structured data
        structured_data_score = 15 if parser.json_ld_count > 0 else (10 if parser.microdata_count > 0 else 0)
        audit_results.append({
            'name': 'Structured Data (Schema.org)',
            'points': structured_data_score,
            'maxPoints': 15,
            'status': 'pass' if structured_data_score >= 10 else 'fail'
        })
        total_score += structured_data_score
        max_score += 15
        
        # 4. Check for semantic HTML
        semantic_count = len(parser.semantic_elements)
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
        images_count = len(parser.images)
        images_with_alt = sum(1 for img in parser.images if img['has_alt'])
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
        h1_count = parser.headings['h1']
        h2_count = parser.headings['h2']
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
        og_count = len(parser.og_tags)
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
        robots_content = parser.robots_meta
        robots_score = 10 if not robots_content or 'noindex' not in robots_content else 0
        audit_results.append({
            'name': 'Crawlable by AI (Robots)',
            'points': robots_score,
            'maxPoints': 10,
            'status': 'pass' if robots_score == 10 else 'fail'
        })
        total_score += robots_score
        max_score += 10
        
        # 9. Check for language attribute
        lang_score = 10 if parser.lang_attribute else 0
        audit_results.append({
            'name': 'HTML Language Attribute',
            'points': lang_score,
            'maxPoints': 10,
            'status': 'pass' if lang_score == 10 else 'fail'
        })
        total_score += lang_score
        max_score += 10
        
        # 10. Check for viewport meta tag (mobile-friendly)
        viewport_score = 10 if parser.viewport else 0
        audit_results.append({
            'name': 'Mobile Viewport Meta Tag',
            'points': viewport_score,
            'maxPoints': 10,
            'status': 'pass' if viewport_score == 10 else 'fail'
        })
        total_score += viewport_score
        max_score += 10
        
        # 11. Check for charset declaration
        charset_score = 10 if parser.charset else 0
        audit_results.append({
            'name': 'Character Encoding Declaration',
            'points': charset_score,
            'maxPoints': 10,
            'status': 'pass' if charset_score == 10 else 'fail'
        })
        total_score += charset_score
        max_score += 10
        
        # 12. Check for canonical URL
        canonical_score = 10 if parser.canonical_url else 0
        audit_results.append({
            'name': 'Canonical URL',
            'points': canonical_score,
            'maxPoints': 10,
            'status': 'pass' if canonical_score == 10 else 'fail'
        })
        total_score += canonical_score
        max_score += 10
        
        # 13. Check for Twitter Card tags
        twitter_score = 10 if parser.twitter_card else 0
        audit_results.append({
            'name': 'Twitter Card Tags',
            'points': twitter_score,
            'maxPoints': 10,
            'status': 'pass' if twitter_score == 10 else 'fail'
        })
        total_score += twitter_score
        max_score += 10
        
        # 14. Check for accessibility (ARIA labels)
        aria_score = 10 if parser.aria_labels >= 3 else (5 if parser.aria_labels > 0 else 0)
        audit_results.append({
            'name': 'ARIA Labels & Accessibility',
            'points': aria_score,
            'maxPoints': 10,
            'status': 'pass' if aria_score >= 8 else ('warning' if aria_score > 0 else 'fail')
        })
        total_score += aria_score
        max_score += 10
        
        # 15. Check for content length (AI needs substantial content)
        content_score = 10 if parser.content_length > 1000 else (5 if parser.content_length > 500 else 0)
        audit_results.append({
            'name': 'Content Length (AI Readable)',
            'points': content_score,
            'maxPoints': 10,
            'status': 'pass' if content_score >= 8 else ('warning' if content_score > 0 else 'fail')
        })
        total_score += content_score
        max_score += 10
        
        # 16. Check for internal linking structure
        internal_links = sum(1 for link in parser.links if link.startswith('/') or link.startswith('#'))
        link_score = 10 if internal_links >= 5 else (5 if internal_links > 0 else 0)
        audit_results.append({
            'name': 'Internal Linking Structure',
            'points': link_score,
            'maxPoints': 10,
            'status': 'pass' if link_score >= 8 else ('warning' if link_score > 0 else 'fail')
        })
        total_score += link_score
        max_score += 10
        
        # 17. Check for forms (interactivity)
        form_score = 5 if len(parser.forms) > 0 else 0
        audit_results.append({
            'name': 'Interactive Forms',
            'points': form_score,
            'maxPoints': 5,
            'status': 'pass' if form_score == 5 else 'fail'
        })
        total_score += form_score
        max_score += 5
        
        # 18. Check for analytics tracking
        analytics_score = 5 if parser.analytics_tracking else 0
        audit_results.append({
            'name': 'Analytics Tracking',
            'points': analytics_score,
            'maxPoints': 5,
            'status': 'pass' if analytics_score == 5 else 'fail'
        })
        total_score += analytics_score
        max_score += 5
        
        # 19. Check for proper heading structure (h1-h6 hierarchy)
        heading_structure_score = 10 if parser.headings['h1'] == 1 and parser.headings['h2'] > 0 and parser.headings['h3'] >= 0 else (5 if parser.headings['h1'] == 1 else 0)
        audit_results.append({
            'name': 'Complete Heading Hierarchy',
            'points': heading_structure_score,
            'maxPoints': 10,
            'status': 'pass' if heading_structure_score >= 8 else ('warning' if heading_structure_score > 0 else 'fail')
        })
        total_score += heading_structure_score
        max_score += 10
        
        # 20. Check for video/media content
        media_score = 5 if len(parser.videos) > 0 or len(parser.iframes) > 0 else 0
        audit_results.append({
            'name': 'Multimedia Content',
            'points': media_score,
            'maxPoints': 5,
            'status': 'pass' if media_score == 5 else 'fail'
        })
        total_score += media_score
        max_score += 5
        
        # Calculate final score
        final_score = round((total_score / max_score) * 100) if max_score > 0 else 0
        
        return {
            'score': final_score,
            'details': audit_results,
            'totalChecks': len(audit_results)
        }
    except urllib.error.URLError as error:
        error_msg = str(error)
        if 'nodename nor servname provided' in error_msg or 'Name or service not known' in error_msg:
            raise Exception('Invalid URL or domain name not found. Please check the URL and try again.')
        elif 'timed out' in error_msg.lower() or 'timeout' in error_msg.lower():
            raise Exception('Request timed out. The website may be slow or unreachable. Please try again.')
        elif '403' in error_msg or 'Forbidden' in error_msg:
            raise Exception('Website blocked the request (403 Forbidden). Some websites block automated requests.')
        elif '404' in error_msg or 'Not Found' in error_msg:
            raise Exception('Website not found (404). Please check the URL and try again.')
        else:
            raise Exception(f'Failed to fetch website: {error_msg}. Please verify the URL is correct and accessible.')
    except Exception as error:
        error_msg = str(error)
        if 'Failed to fetch or analyze website' in error_msg:
            raise  # Re-raise our custom errors
        raise Exception(f'Failed to fetch or analyze website: {error_msg}')

# In-memory storage for reports and payments (in production, use a database)
reports_store = {}
payments_store = {}
admin_scans = []  # Store all scans for admin view

def transform_to_interpretation(insight, url):
    """Transform audit check into AI interpretation insight"""
    name = insight['name']
    status = insight['status']
    
    # Map audit checks to interpretation language
    interpretation_map = {
        'Has Title Tag': {
            'title': 'How AI identifies your website',
            'explanation': 'AI systems use your page title to understand what your site is about. ' + ('Your title clearly communicates your purpose.' if status == 'pass' else 'Your title is missing or unclear, making it harder for AI to identify your website\'s purpose.')
        },
        'Has Meta Description': {
            'title': 'How AI summarizes your content',
            'explanation': f'AI uses meta descriptions to create summaries of your website. {"Your description helps AI accurately summarize your content." if status == "pass" else "Without a clear description, AI may create incomplete or inaccurate summaries of what you offer."}'
        },
        'Structured Data (Schema.org)': {
            'title': 'How AI categorizes your business',
            'explanation': f'Structured data helps AI understand what type of business or content you represent. {"AI can clearly categorize your website." if status == "pass" else "AI may struggle to categorize your website without structured data signals."}'
        },
        'Semantic HTML Elements': {
            'title': 'How AI navigates your content structure',
            'explanation': f'Semantic HTML helps AI understand the organization of your content. {"AI can easily navigate and understand your content structure." if status == "pass" else "AI may misinterpret the importance and relationship of different sections on your site."}'
        },
        'Image Alt Text': {
            'title': 'How AI understands your visual content',
            'explanation': f'Images without descriptions create gaps in AI understanding. {"AI can interpret the meaning of your images." if status == "pass" else "AI cannot understand what your images represent, creating blind spots in interpretation."}'
        },
        'Proper Heading Hierarchy': {
            'title': 'How AI maps your content hierarchy',
            'explanation': f'Headings help AI understand what topics are most important on your page. {"AI can accurately map your content hierarchy and main topics." if status == "pass" else "AI may misunderstand which topics are most important on your website."}'
        },
        'Open Graph Tags': {
            'title': 'How AI represents your site in summaries',
            'explanation': f'Social media tags influence how AI describes your site when sharing. {"AI has clear signals for how to represent your website." if status == "pass" else "AI may use incomplete information when describing your website in summaries or recommendations."}'
        },
        'Crawlable by AI (Robots)': {
            'title': 'Whether AI can access your content',
            'explanation': f'{"AI systems can fully access and interpret your website." if status == "pass" else "Your website blocks AI access, preventing proper interpretation of your content."}'
        },
        'HTML Language Attribute': {
            'title': 'How AI identifies your content language',
            'explanation': 'AI can correctly identify the language of your content.' if status == 'pass' else 'AI may misinterpret the language of your content, affecting how it\'s processed and understood.'
        },
        'Mobile Viewport Meta Tag': {
            'title': 'How AI interprets your mobile experience',
            'explanation': f'{"AI understands your site is optimized for mobile devices." if status == "pass" else "AI may not recognize your mobile optimization, affecting how your site is interpreted across devices."}'
        },
        'Character Encoding Declaration': {
            'title': 'How AI reads your text content',
            'explanation': f'{"AI can correctly read and interpret all text characters on your site." if status == "pass" else "AI may misinterpret special characters, leading to incorrect text interpretation."}'
        },
        'Canonical URL': {
            'title': 'How AI identifies your primary content',
            'explanation': f'{"AI understands which version of your content is primary." if status == "pass" else "AI may be confused about which version of your content is the main one to interpret."}'
        },
        'Twitter Card Tags': {
            'title': 'How AI represents you on social platforms',
            'explanation': f'{"AI has clear signals for representing your site on social platforms." if status == "pass" else "AI may use incomplete information when representing your website on social platforms."}'
        },
        'ARIA Labels & Accessibility': {
            'title': 'How AI understands your interactive elements',
            'explanation': f'{"AI can understand the purpose of interactive elements on your site." if status == "pass" else "AI may misinterpret the function of buttons, forms, and other interactive elements."}'
        },
        'Content Length (AI Readable)': {
            'title': 'How much context AI has about your site',
            'explanation': f'{"AI has sufficient content to form a comprehensive understanding." if status == "pass" else "AI has limited content to work with, leading to incomplete interpretations."}'
        },
        'Internal Linking Structure': {
            'title': 'How AI maps relationships between your pages',
            'explanation': f'{"AI can understand how your pages relate to each other." if status == "pass" else "AI may not understand the relationships between different parts of your website."}'
        },
        'Interactive Forms': {
            'title': 'How AI interprets your user engagement',
            'explanation': f'{"AI recognizes interactive elements that indicate user engagement." if status == "pass" else "AI may not recognize ways users can interact with your site."}'
        },
        'Analytics Tracking': {
            'title': 'How AI understands your measurement approach',
            'explanation': f'{"AI recognizes that you track website performance." if status == "pass" else "AI has no signals about how you measure website effectiveness."}'
        },
        'Complete Heading Hierarchy': {
            'title': 'How AI organizes your content topics',
            'explanation': f'{"AI can organize and prioritize your content topics accurately." if status == "pass" else "AI may misorganize the importance of different topics on your site."}'
        },
        'Multimedia Content': {
            'title': 'How AI processes your rich media',
            'explanation': f'{"AI recognizes rich media content on your site." if status == "pass" else "AI may not recognize multimedia elements that are part of your content."}'
        }
    }
    
    interpretation = interpretation_map.get(name, {
        'title': f'How AI interprets {name.lower()}',
        'explanation': f'AI {"can" if status == "pass" else "cannot"} properly interpret this aspect of your website.'
    })
    
    return {
        'title': interpretation['title'],
        'explanation': interpretation['explanation'],
        'status': status
    }

def transform_to_locked_insight(insight, url):
    """Transform audit check into locked insight with visible but blurred content"""
    name = insight['name']
    status = insight['status']
    
    # Create personalized locked titles
    locked_titles_map = {
        'Has Title Tag': 'AI misidentifies your primary purpose',
        'Has Meta Description': 'Your value proposition is fragmented across pages',
        'Structured Data (Schema.org)': 'Authority signals are weaker than expected',
        'Semantic HTML Elements': 'AI cannot confidently summarize what you do',
        'Image Alt Text': 'Visual content creates interpretation gaps',
        'Proper Heading Hierarchy': 'Topic importance is unclear to AI',
        'Open Graph Tags': 'Social representation lacks clarity',
        'Crawlable by AI (Robots)': 'Access restrictions limit AI understanding',
        'HTML Language Attribute': 'Language interpretation may be incorrect',
        'Mobile Viewport Meta Tag': 'Mobile experience signals are missing',
        'Character Encoding Declaration': 'Text interpretation may have errors',
        'Canonical URL': 'Primary content version is ambiguous',
        'Twitter Card Tags': 'Social platform representation is incomplete',
        'ARIA Labels & Accessibility': 'Interactive element purposes are unclear',
        'Content Length (AI Readable)': 'Insufficient context for complete interpretation',
        'Internal Linking Structure': 'Page relationships are not well understood',
        'Interactive Forms': 'User engagement signals are missing',
        'Analytics Tracking': 'Measurement approach is not recognized',
        'Complete Heading Hierarchy': 'Content organization is unclear',
        'Multimedia Content': 'Rich media is not properly recognized'
    }
    
    # Get the interpretation explanation for blurred preview
    interpretation = transform_to_interpretation(insight, url)
    
    return {
        'title': locked_titles_map.get(name, f'AI interpretation gap: {name}'),
        'explanation': interpretation['explanation'],  # Include for blurred preview
        'status': status,
        'locked': True
    }

def generate_interpretive_summary(score):
    """Generate interpretive summary based on score"""
    if score >= 80:
        return "AI systems have a strong understanding of your website's purpose and content."
    elif score >= 60:
        return "AI partially understands your website, but several important signals remain unclear or misinterpreted."
    elif score >= 40:
        return "AI systems form an incomplete understanding of your website, with significant interpretation gaps."
    else:
        return "AI struggles to form a coherent understanding of your website, with many signals missing or unclear."

def send_email_report(email, url, report_data):
    """Send full report via email"""
    try:
        # For demo purposes, we'll just log the email
        # In production, configure SMTP settings
        report_text = f"""
AI Website Audit Report for {url}

Overall Score: {report_data['score']}/100

Detailed Results:
"""
        for item in report_data['details']:
            report_text += f"\n{item['name']}: {item['points']}/{item['maxPoints']} ({item['status']})\n"
        
        # In production, uncomment and configure SMTP:
        # msg = MIMEMultipart()
        # msg['From'] = 'audit@yourdomain.com'
        # msg['To'] = email
        # msg['Subject'] = f'AI Website Audit Report for {url}'
        # msg.attach(MIMEText(report_text, 'plain'))
        # 
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login('your_email@gmail.com', 'your_password')
        # server.send_message(msg)
        # server.quit()
        
        # For now, save to file for demo
        filename = f"report_{int(time.time())}.txt"
        with open(filename, 'w') as f:
            f.write(f"Email: {email}\n")
            f.write(f"URL: {url}\n\n")
            f.write(report_text)
        
        return True
    except Exception as e:
        print(f"Email error: {e}", file=sys.stderr)
        return False

class RequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler"""
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Serve static files and API endpoints"""
        path = self.path.split('?')[0]
        
        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif path == '/admin':
            self.serve_admin_page()
        elif path.startswith('/api/pdf/'):
            self.handle_pdf_download(path)
        elif path == '/api/admin/scans':
            self.handle_admin_scans()
        elif path.endswith('.css'):
            self.serve_file(path.lstrip('/'), 'text/css')
        elif path.endswith('.js'):
            self.serve_file(path.lstrip('/'), 'application/javascript')
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle API requests"""
        if self.path == '/api/scan':
            self.handle_scan()
        elif self.path == '/api/payment':
            self.handle_payment()
        elif self.path == '/api/unlock':
            self.handle_unlock()
        elif self.path == '/api/pdf':
            self.handle_pdf_generate()
        else:
            self.send_error(404)
    
    def serve_file(self, filename, content_type):
        """Serve a static file"""
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404)
    
    def handle_scan(self):
        """Handle the /api/scan endpoint"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            url = data.get('url')
            
            if not url:
                self.send_json_response({'error': 'URL is required'}, 400)
                return
            
            # Validate URL
            try:
                parsed = urlparse(url)
                if not parsed.scheme or not parsed.scheme.startswith('http'):
                    self.send_json_response({'error': 'URL must use http or https protocol'}, 400)
                    return
            except Exception:
                self.send_json_response({'error': 'Invalid URL format'}, 400)
                return
            
            audit_result = perform_ai_audit(url)
            
            # Store full report
            report_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            reports_store[report_id] = {
                'url': url,
                'full_report': audit_result,
                'timestamp': time.time(),
                'timestamp_iso': timestamp
            }
            
            # Store for admin view
            admin_scans.append({
                'report_id': report_id,
                'url': url,
                'score': audit_result['score'],
                'timestamp': timestamp,
                'payment_status': 'free'
            })
            
            # Transform audit checks into AI interpretation insights
            total_checks = len(audit_result['details'])
            score = audit_result['score']
            
            # Dynamic logic: Lower score = fewer free insights, Higher score = more free insights
            # Score 0-30: Show 1-2 free insights (most locked)
            # Score 30-50: Show 2-3 free insights
            # Score 50-70: Show 3-4 free insights
            # Score 70-85: Show 4-5 free insights
            # Score 85-100: Show 5-6 free insights (least locked)
            
            if score <= 30:
                free_count = 2  # Low score = fewer free insights
            elif score <= 50:
                free_count = 3
            elif score <= 70:
                free_count = 4
            elif score <= 85:
                free_count = 5
            else:  # score > 85
                free_count = 6  # High score = more free insights
            
            # Filter to get only passing insights (green) for "What AI Currently Understands"
            passing_insights = [insight for insight in audit_result['details'] if insight.get('status') == 'pass']
            other_insights = [insight for insight in audit_result['details'] if insight.get('status') != 'pass']
            
            # Ensure we don't exceed available passing insights
            actual_free_count = min(free_count, len(passing_insights))
            
            # Return dynamic number of free insights (only passing ones)
            free_insights = passing_insights[:actual_free_count]
            
            # Combine remaining passing insights with all non-passing insights for locked section
            remaining_passing = passing_insights[actual_free_count:] if len(passing_insights) > actual_free_count else []
            locked_insights = remaining_passing + other_insights
            
            # Transform insights to interpretation-focused language
            free_insights_transformed = [transform_to_interpretation(insight, url) for insight in free_insights]
            locked_insights_transformed = [transform_to_locked_insight(insight, url) for insight in locked_insights]
            
            # Generate interpretive summary based on score
            summary = generate_interpretive_summary(audit_result['score'])
            
            partial_report = {
                'score': audit_result['score'],
                'summary': summary,
                'freeInsights': free_insights_transformed,
                'lockedInsights': locked_insights_transformed,
                'totalInsights': total_checks,
                'reportId': report_id,
                'locked': True
            }
            
            self.send_json_response(partial_report)
        except Exception as error:
            import traceback
            print(f'Error in handle_scan: {error}', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            self.send_json_response({
                'error': str(error) if str(error) else 'An error occurred while scanning the website'
            }, 500)
    
    def handle_payment(self):
        """Handle payment processing"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            report_id = data.get('reportId')
            email = data.get('email', '').strip()
            payment_method = data.get('paymentMethod', 'demo')  # 'demo', 'stripe', 'paypal'
            
            if not report_id or report_id not in reports_store:
                self.send_json_response({'error': 'Invalid report ID'}, 400)
                return
            
            if not email or '@' not in email:
                self.send_json_response({'error': 'Valid email address is required'}, 400)
                return
            
            # Simulate payment processing (in production, integrate with Stripe/PayPal)
            payment_id = str(uuid.uuid4())
            payments_store[payment_id] = {
                'report_id': report_id,
                'email': email,
                'status': 'completed',
                'timestamp': time.time()
            }
            
            # Update admin scan payment status
            for scan in admin_scans:
                if scan['report_id'] == report_id:
                    scan['payment_status'] = 'paid'
                    break
            
            # Send full report via email
            full_report = reports_store[report_id]['full_report']
            email_sent = send_email_report(email, reports_store[report_id]['url'], full_report)
            
            self.send_json_response({
                'success': True,
                'paymentId': payment_id,
                'emailSent': email_sent,
                'message': 'Payment processed successfully. Full report sent to your email.' if email_sent else 'Payment processed successfully. Full report available below.'
            })
        except Exception as error:
            print(f'Payment error: {error}', file=sys.stderr)
            self.send_json_response({
                'error': str(error) if str(error) else 'Payment processing failed'
            }, 500)
    
    def handle_unlock(self):
        """Handle report unlock after payment"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            report_id = data.get('reportId')
            
            if not report_id or report_id not in reports_store:
                self.send_json_response({'error': 'Invalid report ID'}, 400)
                return
            
            # Check if any payment exists for this report
            payment_found = False
            for payment_id, payment in payments_store.items():
                if payment['report_id'] == report_id and payment['status'] == 'completed':
                    payment_found = True
                    break
            
            if payment_found:
                # Return full report with transformed insights
                report_data = reports_store[report_id]
                full_report = report_data['full_report']
                url = report_data['url']
                
                # Transform all insights
                all_insights_transformed = [transform_to_interpretation(insight, url) for insight in full_report['details']]
                summary = generate_interpretive_summary(full_report['score'])
                
                unlocked_report = {
                    'score': full_report['score'],
                    'summary': summary,
                    'freeInsights': all_insights_transformed,
                    'lockedInsights': [],
                    'totalInsights': len(all_insights_transformed),
                    'reportId': report_id,
                    'unlocked': True,
                    'locked': False
                }
                
                self.send_json_response(unlocked_report)
            else:
                self.send_json_response({'error': 'Payment verification failed. Please complete payment first.'}, 400)
        except Exception as error:
            print(f'Unlock error: {error}', file=sys.stderr)
            self.send_json_response({
                'error': str(error) if str(error) else 'Failed to unlock report'
            }, 500)
    
    def generate_pdf_html(self, report_id):
        """Generate HTML for PDF export"""
        if report_id not in reports_store:
            return None
        
        report_data = reports_store[report_id]
        url = report_data['url']
        report = report_data['full_report']
        timestamp = report_data.get('timestamp_iso', datetime.now().isoformat())
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Website Audit Report - {url}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
        .header {{ border-bottom: 3px solid #667eea; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #667eea; margin: 0; }}
        .header p {{ color: #666; margin: 5px 0; }}
        .score-section {{ text-align: center; margin: 30px 0; padding: 20px; background: #f7fafc; border-radius: 10px; }}
        .score {{ font-size: 48px; font-weight: bold; color: #667eea; }}
        .details {{ margin-top: 30px; }}
        .detail-item {{ padding: 15px; margin: 10px 0; border-left: 4px solid #e2e8f0; background: #f9fafb; }}
        .detail-item.pass {{ border-left-color: #48bb78; }}
        .detail-item.warning {{ border-left-color: #ed8936; }}
        .detail-item.fail {{ border-left-color: #f56565; }}
        .detail-name {{ font-weight: bold; font-size: 16px; }}
        .detail-score {{ float: right; color: #667eea; font-weight: bold; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #666; font-size: 12px; text-align: center; }}
        @media print {{ .no-print {{ display: none; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Website Audit Report</h1>
        <p><strong>Website URL:</strong> {url}</p>
        <p><strong>Generated:</strong> {timestamp}</p>
    </div>
    
    <div class="score-section">
        <div class="score">{report['score']}/100</div>
        <p style="font-size: 18px; color: #666;">AI Readiness Score</p>
    </div>
    
    <div class="details">
        <h2>Detailed Audit Results</h2>
"""
        
        for item in report['details']:
            html += f"""
        <div class="detail-item {item['status']}">
            <span class="detail-name">{item['name']}</span>
            <span class="detail-score">{item['points']}/{item['maxPoints']} points</span>
            <div style="clear: both;"></div>
        </div>
"""
        
        html += """
    </div>
    
    <div class="footer">
        <p>Generated by AI Website Audit Tool</p>
        <p>This report contains """ + str(len(report['details'])) + """ comprehensive AI-readiness checks</p>
    </div>
</body>
</html>
"""
        return html
    
    def handle_pdf_generate(self):
        """Generate PDF report"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            report_id = data.get('reportId')
            
            if not report_id or report_id not in reports_store:
                self.send_json_response({'error': 'Invalid report ID'}, 400)
                return
            
            # Check if payment was made
            payment_found = False
            for payment_id, payment in payments_store.items():
                if payment['report_id'] == report_id and payment['status'] == 'completed':
                    payment_found = True
                    break
            
            if not payment_found:
                self.send_json_response({'error': 'PDF download available after payment only'}, 403)
                return
            
            # Generate HTML for PDF
            html_content = self.generate_pdf_html(report_id)
            if not html_content:
                self.send_json_response({'error': 'Report not found'}, 404)
                return
            
            # Return HTML that can be printed to PDF
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
            
        except Exception as error:
            print(f'PDF error: {error}', file=sys.stderr)
            self.send_json_response({
                'error': str(error) if str(error) else 'Failed to generate PDF'
            }, 500)
    
    def handle_pdf_download(self, path):
        """Handle PDF download via GET"""
        try:
            report_id = path.split('/')[-1]
            
            if not report_id or report_id not in reports_store:
                self.send_error(404)
                return
            
            # Check payment
            payment_found = False
            for payment_id, payment in payments_store.items():
                if payment['report_id'] == report_id and payment['status'] == 'completed':
                    payment_found = True
                    break
            
            if not payment_found:
                self.send_error(403)
                return
            
            html_content = self.generate_pdf_html(report_id)
            if html_content:
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Length', str(len(html_content.encode('utf-8'))))
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            else:
                self.send_error(404)
        except Exception as error:
            print(f'PDF download error: {error}', file=sys.stderr)
            self.send_error(500)
    
    def handle_admin_scans(self):
        """Return admin scan data"""
        try:
            # Return recent scans (last 100)
            recent_scans = sorted(admin_scans, key=lambda x: x.get('timestamp', ''), reverse=True)[:100]
            self.send_json_response({
                'scans': recent_scans,
                'total': len(admin_scans)
            })
        except Exception as error:
            print(f'Admin error: {error}', file=sys.stderr)
            self.send_json_response({'error': str(error)}, 500)
    
    def serve_admin_page(self):
        """Serve admin page"""
        admin_html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Admin - AI Website Audit</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f7fafc; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #667eea; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { background: #f7fafc; font-weight: 600; color: #2d3748; }
        tr:hover { background: #f9fafb; }
        .status-paid { color: #48bb78; font-weight: bold; }
        .status-free { color: #ed8936; }
        .score { font-weight: bold; color: #667eea; }
    </style>
</head>
<body>
    <div class="container">
        <h1>AI Website Audit - Admin Dashboard</h1>
        <p>Total Scans: <span id="totalScans">0</span></p>
        <table id="scansTable">
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>URL</th>
                    <th>Score</th>
                    <th>Payment Status</th>
                </tr>
            </thead>
            <tbody id="scansBody">
            </tbody>
        </table>
    </div>
    <script>
        async function loadScans() {
            try {
                const response = await fetch('/api/admin/scans');
                const data = await response.json();
                document.getElementById('totalScans').textContent = data.total;
                const tbody = document.getElementById('scansBody');
                tbody.innerHTML = '';
                data.scans.forEach(scan => {
                    const row = tbody.insertRow();
                    row.insertCell(0).textContent = scan.timestamp;
                    row.insertCell(1).textContent = scan.url;
                    const scoreCell = row.insertCell(2);
                    scoreCell.textContent = scan.score;
                    scoreCell.className = 'score';
                    const statusCell = row.insertCell(3);
                    statusCell.textContent = scan.payment_status === 'paid' ? 'Paid' : 'Free';
                    statusCell.className = scan.payment_status === 'paid' ? 'status-paid' : 'status-free';
                });
            } catch (error) {
                console.error('Error loading scans:', error);
            }
        }
        loadScans();
        setInterval(loadScans, 5000); // Refresh every 5 seconds
    </script>
</body>
</html>
"""
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', str(len(admin_html.encode('utf-8'))))
        self.end_headers()
        self.wfile.write(admin_html.encode('utf-8'))
    
    def send_json_response(self, data, status=200):
        """Send JSON response"""
        json_data = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', str(len(json_data)))
        self.end_headers()
        self.wfile.write(json_data)
    
    def log_message(self, format, *args):
        """Suppress default logging"""
        pass

def run_server(port=3000, host='0.0.0.0'):
    """Start the HTTP server"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, RequestHandler)
    
    # Get the actual port (in case port 0 was used for auto-assignment)
    actual_port = httpd.server_address[1]
    
    print(f'🚀 Server running on http://{host}:{actual_port}')
    if host == '0.0.0.0':
        print(f'📝 Accessible from: http://localhost:{actual_port}')
        print(f'🌐 Or from network: http://<your-ip>:{actual_port}')
    else:
        print(f'📝 Open your browser and navigate to: http://{host}:{actual_port}')
    print(f'🛑 Press Ctrl+C to stop the server')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n👋 Server stopped')
        httpd.server_close()

if __name__ == '__main__':
    # Get port from environment variable (for cloud platforms) or command line
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 3000))
    # Use 0.0.0.0 to accept connections from any interface (for cloud deployment)
    host = os.environ.get('HOST', '0.0.0.0')
    run_server(port, host)

