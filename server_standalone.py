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
from email.mime.base import MIMEBase
from email import encoders
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
        # Restaurant/Bar specific
        self.restaurant_schema = False
        self.menu_links = []
        self.location_info = False
        self.hours_info = False
        self.reservation_links = []
        self.review_mentions = False
        self.cuisine_mentions = False
        self.price_range_mentions = False
        self.phone_number = False
        self.address_info = False
        # Review analysis
        self.review_widgets = []
        self.review_platforms = []  # Google, TripAdvisor, Yelp, etc.
        self.review_links = []
        self.rating_mentions = False
        self.social_media_links = []
        # Additional Restaurant/Bar specific
        self.cuisine_type = []
        self.dietary_restrictions = []  # vegan, gluten-free, vegetarian, etc.
        self.special_features = []  # outdoor seating, live music, happy hour, etc.
        self.photo_galleries = []
        self.events_calendar = False
        self.gift_cards = False
        self.catering_info = False
        self.private_dining = False
        self.delivery_takeout = False
        self.parking_info = False
        self.wifi_info = False
        
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
                # Check for menu links
                href_lower = href.lower()
                if 'menu' in href_lower:
                    self.menu_links.append(href)
                # Check for reservation links
                if any(keyword in href_lower for keyword in ['reserv', 'book', 'table', 'booking']):
                    self.reservation_links.append(href)
                # Check for menu links
                link_text = attrs_dict.get('text', '').lower() if 'text' in attrs_dict else ''
                href_lower = href.lower()
                if 'menu' in href_lower or 'menu' in link_text:
                    self.menu_links.append(href)
                # Check for reservation links
                if 'reserv' in href_lower or 'book' in href_lower or 'table' in href_lower or 'reserv' in link_text or 'book' in link_text:
                    self.reservation_links.append(href)
                
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
        
        # Check for restaurant/bar specific content
        data_lower = data.lower()
        # Location/address detection
        if any(keyword in data_lower for keyword in ['address', 'location', 'street', 'avenue', 'road', 'zip', 'postal']):
            self.location_info = True
            self.address_info = True
        # Hours detection
        if any(keyword in data_lower for keyword in ['hours', 'open', 'closed', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'am', 'pm']):
            self.hours_info = True
        # Phone detection
        if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', data):
            self.phone_number = True
        # Review mentions
        if any(keyword in data_lower for keyword in ['review', 'rating', 'star', 'yelp', 'tripadvisor', 'google review']):
            self.review_mentions = True
        # Rating detection (stars, ratings)
        if re.search(r'\d+\.?\d*\s*(star|rating|out of)', data_lower) or re.search(r'[⭐★]', data):
            self.rating_mentions = True
        
        # Cuisine type detection
        cuisine_keywords = ['italian', 'mexican', 'chinese', 'japanese', 'thai', 'indian', 'french', 'mediterranean', 
                           'american', 'seafood', 'steakhouse', 'pizza', 'sushi', 'bbq', 'barbecue', 'asian', 
                           'fusion', 'tapas', 'bistro', 'cafe', 'brasserie', 'pub', 'bar', 'grill', 'diner']
        for cuisine in cuisine_keywords:
            if cuisine in data_lower and cuisine.title() not in self.cuisine_type:
                self.cuisine_type.append(cuisine.title())
        
        # Dietary restrictions
        dietary_keywords = ['vegan', 'vegetarian', 'gluten-free', 'gluten free', 'dairy-free', 'dairy free', 
                           'keto', 'paleo', 'halal', 'kosher', 'nut-free', 'nut free', 'allergy', 'allergen']
        for dietary in dietary_keywords:
            if dietary in data_lower and dietary.title() not in [d.lower() for d in self.dietary_restrictions]:
                self.dietary_restrictions.append(dietary.title())
        
        # Special features
        feature_keywords = ['outdoor seating', 'patio', 'terrace', 'live music', 'entertainment', 'happy hour', 
                           'brunch', 'breakfast', 'lunch', 'dinner', 'late night', 'late-night', 'wine bar', 
                           'cocktail', 'craft beer', 'draft beer', 'full bar', 'bar', 'rooftop', 'waterfront', 
                           'view', 'fireplace', 'private room', 'private dining', 'event space', 'catering', 
                           'takeout', 'take-out', 'delivery', 'curbside', 'drive-thru', 'drive through', 
                           'parking', 'valet', 'wifi', 'wi-fi', 'free wifi', 'pet friendly', 'dog friendly']
        for feature in feature_keywords:
            if feature in data_lower and feature.title() not in [f.lower() for f in self.special_features]:
                self.special_features.append(feature.title())
        
        # Events/Calendar
        if any(keyword in data_lower for keyword in ['event', 'calendar', 'upcoming', 'schedule', 'reservation', 'book']):
            self.events_calendar = True
        
        # Gift cards
        if any(keyword in data_lower for keyword in ['gift card', 'gift certificate', 'gift']):
            self.gift_cards = True
        
        # Catering
        if 'catering' in data_lower:
            self.catering_info = True
        
        # Private dining
        if any(keyword in data_lower for keyword in ['private dining', 'private room', 'private event', 'event space']):
            self.private_dining = True
        
        # Delivery/Takeout
        if any(keyword in data_lower for keyword in ['delivery', 'takeout', 'take-out', 'pickup', 'pick-up', 'order online']):
            self.delivery_takeout = True
        
        # Parking
        if any(keyword in data_lower for keyword in ['parking', 'valet', 'garage', 'lot']):
            self.parking_info = True
        
        # WiFi
        if any(keyword in data_lower for keyword in ['wifi', 'wi-fi', 'wireless', 'internet']):
            self.wifi_info = True
        # Cuisine mentions
        if any(keyword in data_lower for keyword in ['cuisine', 'italian', 'mexican', 'asian', 'american', 'french', 'japanese', 'chinese', 'indian', 'mediterranean', 'steakhouse', 'seafood', 'pizza', 'sushi', 'bar', 'pub', 'bistro', 'cafe', 'restaurant']):
            self.cuisine_mentions = True
        # Price range
        if any(keyword in data_lower for keyword in ['$', 'price', 'affordable', 'moderate', 'upscale', 'fine dining', 'budget']):
            self.price_range_mentions = True

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
        
        # Check for restaurant schema in JSON-LD before parsing
        import json
        restaurant_schema_found = False
        try:
            # Find all JSON-LD scripts
            json_ld_pattern = r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>'
            json_ld_matches = re.findall(json_ld_pattern, html, re.DOTALL | re.IGNORECASE)
            for json_str in json_ld_matches:
                try:
                    data = json.loads(json_str)
                    # Check if it's a restaurant schema
                    if isinstance(data, dict):
                        schema_type = data.get('@type', '').lower()
                        if 'restaurant' in schema_type or 'foodestablishment' in schema_type or 'bar' in schema_type:
                            restaurant_schema_found = True
                            break
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                schema_type = item.get('@type', '').lower()
                                if 'restaurant' in schema_type or 'foodestablishment' in schema_type or 'bar' in schema_type:
                                    restaurant_schema_found = True
                                    break
                except:
                    pass
        except:
            pass
        
        # Parse HTML
        parser = HTMLAuditParser()
        parser.feed(html)
        parser.restaurant_schema = restaurant_schema_found
        
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
        
        # Restaurant/Bar Specific Checks (21-25)
        
        # 21. Restaurant Schema (JSON-LD)
        restaurant_schema_score = 15 if parser.restaurant_schema else 0
        audit_results.append({
            'name': 'Restaurant/Bar Schema Markup',
            'points': restaurant_schema_score,
            'maxPoints': 15,
            'status': 'pass' if restaurant_schema_score == 15 else 'fail'
        })
        total_score += restaurant_schema_score
        max_score += 15
        
        # 22. Menu Availability
        menu_score = 10 if len(parser.menu_links) > 0 else 0
        audit_results.append({
            'name': 'Menu Information Available',
            'points': menu_score,
            'maxPoints': 10,
            'status': 'pass' if menu_score == 10 else 'fail'
        })
        total_score += menu_score
        max_score += 10
        
        # 23. Location & Contact Information
        location_score = 10 if parser.location_info and parser.phone_number else (5 if parser.location_info or parser.phone_number else 0)
        audit_results.append({
            'name': 'Location & Contact Information',
            'points': location_score,
            'maxPoints': 10,
            'status': 'pass' if location_score >= 8 else ('warning' if location_score > 0 else 'fail')
        })
        total_score += location_score
        max_score += 10
        
        # 24. Operating Hours
        hours_score = 10 if parser.hours_info else 0
        audit_results.append({
            'name': 'Operating Hours Information',
            'points': hours_score,
            'maxPoints': 10,
            'status': 'pass' if hours_score == 10 else 'fail'
        })
        total_score += hours_score
        max_score += 10
        
        # 25. Reservation/Booking System
        reservation_score = 10 if len(parser.reservation_links) > 0 else 0
        audit_results.append({
            'name': 'Reservation/Booking System',
            'points': reservation_score,
            'maxPoints': 10,
            'status': 'pass' if reservation_score == 10 else 'fail'
        })
        total_score += reservation_score
        max_score += 10
        
        # 26. Review Visibility & Integration
        review_visibility_score = 10 if len(parser.review_platforms) > 0 or len(parser.review_widgets) > 0 else (5 if parser.review_mentions or parser.rating_mentions else 0)
        audit_results.append({
            'name': 'Review Visibility & Integration',
            'points': review_visibility_score,
            'maxPoints': 10,
            'status': 'pass' if review_visibility_score >= 8 else ('warning' if review_visibility_score > 0 else 'fail')
        })
        total_score += review_visibility_score
        max_score += 10
        
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
        },
        'Restaurant/Bar Schema Markup': {
            'title': 'How AI identifies your restaurant or bar',
            'explanation': f'{"AI agents can clearly identify your establishment as a restaurant or bar, making you discoverable in food-related queries." if status == "pass" else "AI agents may not recognize your website as a restaurant or bar, making you invisible in food discovery searches."}'
        },
        'Menu Information Available': {
            'title': 'How AI understands what you serve',
            'explanation': f'{"AI agents can find your menu and understand your offerings, helping customers discover your cuisine." if status == "pass" else "AI agents cannot find your menu, making it impossible to recommend your dishes or cuisine type to customers."}'
        },
        'Location & Contact Information': {
            'title': 'How AI helps customers find you',
            'explanation': f'{"AI agents can provide your location and contact info to customers searching for nearby restaurants." if status == "pass" else "AI agents cannot help customers find your location or contact you, reducing local discovery."}'
        },
        'Operating Hours Information': {
            'title': 'How AI knows when you are open',
            'explanation': f'{"AI agents can tell customers when you are open, enabling real-time recommendations." if status == "pass" else "AI agents cannot determine your hours, so they may recommend you when you are closed or skip you during open hours."}'
        },
        'Reservation/Booking System': {
            'title': 'How AI helps customers book tables',
            'explanation': f'{"AI agents can direct customers to your booking system, enabling seamless reservations." if status == "pass" else "AI agents cannot help customers make reservations, reducing conversion opportunities."}'
        },
        'Review Visibility & Integration': {
            'title': 'How AI understands customer sentiment',
            'explanation': 'AI agents can access and analyze customer reviews to understand your restaurant reputation and customer satisfaction.' if status == 'pass' else 'AI agents cannot find or analyze customer reviews, missing critical signals about your restaurant quality and customer satisfaction.'
        },
        'Cuisine Type Identification': {
            'title': 'How AI categorizes your cuisine',
            'explanation': f'{"AI agents can identify your cuisine type, helping customers find restaurants that match their preferences." if status == "pass" else "AI agents cannot determine your cuisine type, making it harder for customers to discover you when searching for specific food types."}'
        },
        'Dietary Restrictions Information': {
            'title': 'How AI helps customers with dietary needs',
            'explanation': f'{"AI agents can identify dietary options (vegan, gluten-free, etc.), helping customers with specific dietary requirements find your restaurant." if status == "pass" else "AI agents cannot identify dietary options, making your restaurant invisible to customers searching for specific dietary accommodations."}'
        },
        'Special Features & Amenities': {
            'title': 'How AI understands your unique offerings',
            'explanation': f'{"AI agents can identify special features (outdoor seating, live music, etc.), helping match customers to restaurants with specific amenities." if status == "pass" else "AI agents cannot identify special features, missing opportunities to match customers looking for specific experiences."}'
        },
        'Visual Content & Photo Galleries': {
            'title': 'How AI visualizes your restaurant',
            'explanation': f'{"AI agents can access visual content to understand your restaurant atmosphere and food presentation." if status == "pass" else "AI agents have limited visual information, making it harder to understand your restaurant atmosphere and food quality."}'
        },
        'Events & Calendar Information': {
            'title': 'How AI knows about your events',
            'explanation': f'{"AI agents can identify upcoming events and special occasions, helping customers discover time-sensitive opportunities." if status == "pass" else "AI agents cannot identify events or special occasions, missing opportunities to recommend time-sensitive experiences."}'
        },
        'Additional Services Information': {
            'title': 'How AI understands your service offerings',
            'explanation': f'{"AI agents can identify additional services (gift cards, catering, private dining), expanding discovery opportunities." if status == "pass" else "AI agents cannot identify additional services, limiting discovery to basic dining experiences only."}'
        },
        'Delivery & Takeout Information': {
            'title': 'How AI knows your service options',
            'explanation': f'{"AI agents can identify delivery and takeout options, helping customers find convenient dining solutions." if status == "pass" else "AI agents cannot identify delivery or takeout options, missing customers looking for off-premise dining."}'
        },
        'Parking & Accessibility Information': {
            'title': 'How AI helps customers plan their visit',
            'explanation': f'{"AI agents can provide parking and accessibility information, helping customers make informed decisions about visiting." if status == "pass" else "AI agents cannot provide parking or accessibility information, creating uncertainty for potential customers."}'
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
        'Multimedia Content': 'Rich media is not properly recognized',
        'Restaurant/Bar Schema Markup': 'AI cannot identify your establishment type',
        'Menu Information Available': 'Your menu is invisible to AI agents',
        'Location & Contact Information': 'Customers cannot find your location',
        'Operating Hours Information': 'AI does not know when you are open',
        'Reservation/Booking System': 'AI cannot help customers book tables',
        'Review Visibility & Integration': 'Customer reviews are invisible to AI agents',
        'Cuisine Type Identification': 'AI cannot identify your cuisine type',
        'Dietary Restrictions Information': 'Dietary options are not visible to AI agents',
        'Special Features & Amenities': 'Special features are not recognized by AI',
        'Visual Content & Photo Galleries': 'Visual content is limited for AI understanding',
        'Events & Calendar Information': 'Events are not discoverable by AI agents',
        'Additional Services Information': 'Additional services are invisible to AI',
        'Delivery & Takeout Information': 'Service options are unclear to AI agents',
        'Parking & Accessibility Information': 'Accessibility information is missing'
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
    """Generate interpretive summary based on score for restaurants/bars"""
    if score >= 80:
        return "AI agents have a strong understanding of your restaurant or bar, making you highly discoverable in food-related searches and recommendations."
    elif score >= 60:
        return "AI agents partially understand your establishment, but several important signals remain unclear, limiting your visibility in discovery searches."
    elif score >= 40:
        return "AI agents form an incomplete understanding of your restaurant or bar, with significant gaps that reduce your discoverability."
    else:
        return "AI agents struggle to identify and understand your establishment, making you nearly invisible in food discovery searches and recommendations."

def generate_review_recommendations(parser, url, html):
    """Generate recommendations based on review analysis and common restaurant review patterns"""
    recommendations = []
    
    # Check what review platforms are present
    has_google = 'Google' in parser.review_platforms
    has_tripadvisor = 'TripAdvisor' in parser.review_platforms
    has_yelp = 'Yelp' in parser.review_platforms
    has_review_widgets = len(parser.review_widgets) > 0
    has_social_media = len(parser.social_media_links) > 0
    
    # Recommendation 1: Review Platform Presence
    if not has_google and not has_tripadvisor and not has_yelp:
        recommendations.append({
            'category': 'Review Visibility',
            'priority': 'High',
            'title': 'Add Review Platform Links',
            'description': 'Link to your Google Business Profile, TripAdvisor, and Yelp pages. AI agents use these platforms to understand customer sentiment and make recommendations.',
            'action': 'Add prominent links to your Google Maps listing, TripAdvisor page, and Yelp profile in your website footer or contact section.',
            'impact': 'Increases discoverability in local search and AI-powered restaurant recommendations'
        })
    elif not has_google:
        recommendations.append({
            'category': 'Review Visibility',
            'priority': 'High',
            'title': 'Add Google Business Profile Link',
            'description': 'Google Reviews are critical for AI agents. Most AI assistants prioritize Google Business listings when recommending restaurants.',
            'action': 'Add a link to your Google Business Profile and embed Google Reviews widget on your website.',
            'impact': 'Significantly improves visibility in Google-powered AI assistants and local search'
        })
    
    # Recommendation 2: Review Widget Integration
    if not has_review_widgets:
        recommendations.append({
            'category': 'Review Integration',
            'priority': 'Medium',
            'title': 'Embed Review Widgets',
            'description': 'Displaying reviews directly on your website helps AI agents understand customer sentiment and your restaurant\'s strengths.',
            'action': 'Embed Google Reviews widget or TripAdvisor review snippets on your homepage or dedicated reviews page.',
            'impact': 'AI agents can better understand customer feedback and your restaurant\'s reputation'
        })
    
    # Recommendation 3: Social Media Integration
    if not has_social_media:
        recommendations.append({
            'category': 'Social Proof',
            'priority': 'Medium',
            'title': 'Link Social Media Accounts',
            'description': 'Social media posts and reviews provide additional signals for AI agents about your restaurant\'s popularity and customer engagement.',
            'action': 'Add links to your Instagram, Facebook, and other social media accounts. AI agents analyze social content for restaurant recommendations.',
            'impact': 'Increases signals for AI agents about your restaurant\'s popularity and customer engagement'
        })
    
    # Recommendation 4: Common Review Themes (Based on typical restaurant feedback)
    html_lower = html.lower()
    
    # Check for common positive mentions
    if 'wait' in html_lower or 'slow' in html_lower or 'time' in html_lower:
        recommendations.append({
            'category': 'Service Optimization',
            'priority': 'Medium',
            'title': 'Address Wait Time Concerns',
            'description': 'Many restaurant reviews mention wait times. Proactively address this on your website.',
            'action': 'Add information about reservation options, peak hours, or average wait times. Consider implementing online waitlist or reservation system.',
            'impact': 'Reduces negative review mentions and improves customer expectations'
        })
    
    if not parser.hours_info:
        recommendations.append({
            'category': 'Information Clarity',
            'priority': 'High',
            'title': 'Display Clear Operating Hours',
            'description': 'One of the most common review complaints is confusion about hours or arriving when closed.',
            'action': 'Prominently display your operating hours on your homepage and ensure they\'re accurate. Update for holidays and special events.',
            'impact': 'Reduces customer frustration and negative reviews about hours'
        })
    
    if not parser.menu_links or len(parser.menu_links) == 0:
        recommendations.append({
            'category': 'Menu Transparency',
            'priority': 'High',
            'title': 'Make Menu Easily Accessible',
            'description': 'Reviews often mention menu clarity and availability. AI agents need menu information to make recommendations.',
            'action': 'Add a clear "Menu" link in navigation and ensure menu is easily accessible. Include prices and dietary information (vegan, gluten-free, etc.).',
            'impact': 'Improves customer decision-making and AI agent understanding of your offerings'
        })
    
    # Recommendation 5: Response to Reviews
    recommendations.append({
        'category': 'Review Management',
        'priority': 'High',
        'title': 'Respond to Reviews Regularly',
        'description': 'AI agents analyze review responses to understand how restaurants handle customer feedback. Active engagement signals quality.',
        'action': 'Respond to reviews on Google, TripAdvisor, and Yelp within 24-48 hours. Thank positive reviewers and address concerns professionally.',
        'impact': 'Shows active customer engagement and improves AI agent perception of your restaurant\'s quality'
    })
    
    # Recommendation 6: Photo Optimization
    if len(parser.images) < 10:
        recommendations.append({
            'category': 'Visual Content',
            'priority': 'Medium',
            'title': 'Add More High-Quality Photos',
            'description': 'Reviews with photos get more attention from AI agents. Visual content helps AI understand your restaurant\'s atmosphere and food quality.',
            'action': 'Add professional photos of your dishes, interior, and exterior. Encourage customers to share photos in reviews.',
            'impact': 'Increases visual signals for AI agents and improves customer trust'
        })
    
    # Recommendation 7: Price Range Clarity
    if not parser.price_range_mentions:
        recommendations.append({
            'category': 'Pricing Transparency',
            'priority': 'Medium',
            'title': 'Clarify Price Range',
            'description': 'Price range is a key factor in AI agent recommendations. Unclear pricing can lead to mismatched customer expectations.',
            'action': 'Add price range indicators ($$, $$$) or average meal cost information. This helps AI agents match customers to appropriate restaurants.',
            'impact': 'Improves AI agent matching and reduces customer surprise about pricing'
        })
    
    # Recommendation 8: Special Features
    recommendations.append({
        'category': 'Unique Selling Points',
        'priority': 'Medium',
        'title': 'Highlight What Makes You Unique',
        'description': 'AI agents look for unique features when making recommendations. Common differentiators include: outdoor seating, live music, happy hour, private dining, etc.',
        'action': 'Clearly highlight special features, events, or unique aspects of your restaurant that customers mention positively in reviews.',
        'impact': 'Helps AI agents differentiate your restaurant and match it to specific customer preferences'
    })
    
    return recommendations

def save_user_to_database(email, url, report_id, score):
    """Save user email to database for future purposes"""
    try:
        db_file = 'user_database.json'
        users = []
        
        # Load existing users
        if os.path.exists(db_file):
            try:
                with open(db_file, 'r') as f:
                    users = json.load(f)
            except:
                users = []
        
        # Add new user
        user_entry = {
            'email': email,
            'url': url,
            'report_id': report_id,
            'score': score,
            'timestamp': datetime.now().isoformat(),
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        users.append(user_entry)
        
        # Save back to file
        with open(db_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        print(f"✅ User saved to database: {email}", flush=True)
        return True
    except Exception as e:
        print(f"Database error: {e}", file=sys.stderr)
        return False

def send_email_report(email, url, report_data, report_id):
    """Send full report via email with PDF attachment"""
    try:
        # Save user to database
        save_user_to_database(email, url, report_id, report_data['score'])
        
        # Get SMTP settings from environment variables or use defaults
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER', '')
        smtp_password = os.environ.get('SMTP_PASSWORD', '')
        from_email = os.environ.get('FROM_EMAIL', smtp_user)
        
        # Generate PDF HTML content
        pdf_html = generate_email_pdf_html(report_id, url, report_data)
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = email
        msg['Subject'] = f'AI Website Audit Report for {url}'
        
        # Email body
        body_text = f"""
Hello!

Thank you for using our AI Website Audit service.

Your website ({url}) received an AI Readiness Score of {report_data['score']}/100.

Please find your complete audit report attached as an HTML file that you can save as PDF.

Best regards,
AI Website Audit Team
"""
        msg.attach(MIMEText(body_text, 'plain'))
        
        # Attach PDF HTML as file
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(pdf_html.encode('utf-8'))
        encoders.encode_base64(attachment)
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename= "AI_Audit_Report_{url.replace("https://", "").replace("http://", "").replace("/", "_")}.html"'
        )
        msg.attach(attachment)
        
        # Send email if SMTP credentials are configured
        if smtp_user and smtp_password:
            try:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
                server.quit()
                print(f"✅ Email sent successfully to {email}", flush=True)
                return True
            except Exception as e:
                print(f"⚠️ SMTP error (email saved to database): {e}", file=sys.stderr)
                # Still return True because user is saved to database
                return True
        else:
            # If no SMTP configured, save email to file for manual sending
            email_file = f"emails_to_send/email_{int(time.time())}_{email.replace('@', '_at_')}.eml"
            os.makedirs('emails_to_send', exist_ok=True)
            with open(email_file, 'w') as f:
                f.write(f"To: {email}\n")
                f.write(f"Subject: {msg['Subject']}\n")
                f.write(f"From: {from_email}\n\n")
                f.write(body_text)
                f.write(f"\n\n--- PDF Report HTML ---\n{pdf_html}")
            print(f"⚠️ SMTP not configured. Email saved to {email_file}", flush=True)
            print(f"💡 To enable email sending, set environment variables:", flush=True)
            print(f"   SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL", flush=True)
            return True  # Still return True because user is saved
        
    except Exception as e:
        print(f"Email error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def generate_email_pdf_html(report_id, url, report_data):
    """Generate HTML content for PDF attachment"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Website Audit Report - {url}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.6;
            color: #333;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 20px;
        }}
        .score {{
            font-size: 4rem;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }}
        .insight {{
            margin: 20px 0;
            padding: 15px;
            border-left: 4px solid #ddd;
            background: #f9f9f9;
        }}
        .insight.pass {{
            border-left-color: #10b981;
        }}
        .insight.warning {{
            border-left-color: #f59e0b;
        }}
        .insight.fail {{
            border-left-color: #ef4444;
        }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            text-align: center;
            color: #666;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Website Audit Report</h1>
        <p><strong>Website:</strong> {url}</p>
        <p><strong>Date:</strong> {timestamp}</p>
        <div class="score">{report_data['score']}/100</div>
    </div>
    
    <h2>Detailed Analysis</h2>
"""
    
    for item in report_data['details']:
        status_class = item.get('status', 'fail')
        html_content += f"""
    <div class="insight {status_class}">
        <h3>{item['name']}</h3>
        <p><strong>Score:</strong> {item['points']}/{item['maxPoints']} ({status_class.upper()})</p>
        <p>{item.get('explanation', item.get('description', ''))}</p>
    </div>
"""
    
    html_content += f"""
    <div class="footer">
        <p>Generated by AI Website Audit Tool</p>
        <p>Report ID: {report_id}</p>
    </div>
</body>
</html>
"""
    
    return html_content

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
        
        # Debug: print the path being requested
        print(f'GET request: {path}', flush=True)
        
        if path == '/' or path == '/index.html':
            self.serve_file('index.html', 'text/html')
        elif path == '/admin':
            self.serve_admin_page()
        elif path == '/privacy-policy.html':
            # Explicitly handle privacy policy
            self.serve_file('privacy-policy.html', 'text/html')
        elif path.startswith('/api/pdf/'):
            self.handle_pdf_download(path)
        elif path == '/api/admin/scans':
            self.handle_admin_scans()
        elif path.endswith('.html'):
            # Serve any other HTML file
            filename = path.lstrip('/')
            if os.path.exists(filename):
                self.serve_file(filename, 'text/html')
            else:
                self.send_error(404)
        elif path.endswith('.css'):
            filename = path.lstrip('/')
            if os.path.exists(filename):
                self.serve_file(filename, 'text/css')
            else:
                self.send_error(404)
        elif path.endswith('.js'):
            filename = path.lstrip('/')
            if os.path.exists(filename):
                self.serve_file(filename, 'application/javascript')
            else:
                self.send_error(404)
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
            
            # Generate review-based recommendations
            # Fetch HTML again to analyze for recommendations
            try:
                ssl_context = ssl._create_unverified_context()
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5'
                }
                req = urllib.request.Request(url, headers=headers)
                try:
                    response = urllib.request.urlopen(req, timeout=10, context=ssl_context)
                except urllib.error.HTTPError as e:
                    if e.code == 403:
                        simple_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
                        req = urllib.request.Request(url, headers=simple_headers)
                        response = urllib.request.urlopen(req, timeout=10, context=ssl_context)
                    else:
                        raise
                html = response.read().decode('utf-8', errors='ignore')
                
                # Parse again to get parser data for recommendations
                parser = HTMLAuditParser()
                parser.feed(html)
                
                # Check for review widgets
                review_widgets_found = []
                if 'google' in html.lower() and ('review' in html.lower() or 'rating' in html.lower()):
                    if 'maps/embed' in html.lower() or 'place_id' in html.lower():
                        review_widgets_found.append('Google Reviews Widget')
                if 'tripadvisor' in html.lower():
                    review_widgets_found.append('TripAdvisor Widget')
                if 'yelp' in html.lower() and 'review' in html.lower():
                    review_widgets_found.append('Yelp Widget')
                parser.review_widgets = review_widgets_found
                
                review_recommendations = generate_review_recommendations(parser, url, html)
            except Exception as e:
                # If we can't fetch again, generate basic recommendations
                print(f'Warning: Could not generate review recommendations: {e}', flush=True)
                parser = HTMLAuditParser()
                review_recommendations = generate_review_recommendations(parser, url, '')
            
            # Add recommendations to audit result
            audit_result['reviewRecommendations'] = review_recommendations
            
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
                'locked': True,
                'reviewRecommendations': audit_result.get('reviewRecommendations', [])
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
            email_sent = send_email_report(email, reports_store[report_id]['url'], full_report, report_id)
            
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
                    'locked': False,
                    'reviewRecommendations': full_report.get('reviewRecommendations', [])
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
    try:
        server_address = (host, port)
        httpd = HTTPServer(server_address, RequestHandler)
        
        # Get the actual port (in case port 0 was used for auto-assignment)
        actual_port = httpd.server_address[1]
        
        print(f'🚀 Server running on http://{host}:{actual_port}', flush=True)
        if host == '0.0.0.0':
            print(f'📝 Accessible from: http://localhost:{actual_port}', flush=True)
            print(f'🌐 Or from network: http://<your-ip>:{actual_port}', flush=True)
        else:
            print(f'📝 Open your browser and navigate to: http://{host}:{actual_port}', flush=True)
        print(f'🛑 Press Ctrl+C to stop the server', flush=True)
        print(f'✅ Server is ready and listening on port {actual_port}', flush=True)
        
        httpd.serve_forever()
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f'❌ Port {port} is already in use. Trying alternative port...', flush=True)
            # Try next port
            try:
                server_address = (host, 0)  # Let OS assign port
                httpd = HTTPServer(server_address, RequestHandler)
                actual_port = httpd.server_address[1]
                print(f'🚀 Server running on port {actual_port}', flush=True)
                httpd.serve_forever()
            except Exception as e2:
                print(f'❌ Failed to start server: {e2}', flush=True)
                sys.exit(1)
        else:
            print(f'❌ Failed to start server: {e}', flush=True)
            sys.exit(1)
    except KeyboardInterrupt:
        print('\n👋 Server stopped', flush=True)
        httpd.server_close()
    except Exception as e:
        print(f'❌ Server error: {e}', flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    # Get port from environment variable (for cloud platforms) or command line
    port = int(os.environ.get('PORT', sys.argv[1] if len(sys.argv) > 1 else 3000))
    # Use 0.0.0.0 to accept connections from any interface (for cloud deployment)
    host = os.environ.get('HOST', '0.0.0.0')
    run_server(port, host)

