import requests
import validators
import tldextract
import dns.resolver
import whois
import re
import time
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import json
import os
from datetime import datetime

# Initialize colorama for colored output
init(autoreset=True)

class SafeURLChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Known malicious patterns
        self.suspicious_patterns = [
            r'bit\.ly', r'tinyurl\.com', r'goo\.gl', r't\.co', r'is\.gd',
            r'v\.gd', r'cli\.gs', r'ow\.ly', r'u\.to', r'j\.mp',
            r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',  # IP addresses
            r'[a-zA-Z0-9]{20,}',  # Very long random strings
        ]
        
        # Spam/advertisement indicators
        self.spam_indicators = [
            'click', 'banner', 'ad', 'advertisement', 'sponsor', 'promo',
            'offer', 'discount', 'deal', 'limited', 'free', 'win',
            'lottery', 'prize', 'winner', 'claim', 'urgent', 'act now',
            'limited time', 'exclusive', 'secret', 'hidden', 'revealed'
        ]
        
        # Load blacklisted domains (you can expand this)
        self.blacklisted_domains = self.load_blacklist()
        
    def load_blacklist(self):
        """Load blacklisted domains from file or return default list"""
        blacklist_file = 'blacklist.json'
        if os.path.exists(blacklist_file):
            try:
                with open(blacklist_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default blacklist
        return [
            'malware.example.com',
            'phishing.example.com',
            'scam.example.com'
        ]
    
    def validate_url_format(self, url):
        """Check if URL format is valid"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            if not validators.url(url):
                return False, "Invalid URL format"
            
            return True, "Valid URL format"
        except Exception as e:
            return False, f"URL validation error: {str(e)}"
    
    def check_dns_resolution(self, url):
        """Check if domain resolves to valid IP"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Resolve domain to IP
            answers = dns.resolver.resolve(domain, 'A')
            ip_addresses = [str(answer) for answer in answers]
            
            # Check for suspicious IP patterns
            for ip in ip_addresses:
                if ip.startswith('0.') or ip.startswith('127.') or ip.startswith('10.'):
                    return False, f"Suspicious IP address: {ip}"
            
            return True, f"DNS resolves to: {', '.join(ip_addresses)}"
        except Exception as e:
            return False, f"DNS resolution failed: {str(e)}"
    
    def check_domain_age(self, url):
        """Check domain registration age"""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            w = whois.whois(domain)
            
            if w.creation_date:
                if isinstance(w.creation_date, list):
                    creation_date = w.creation_date[0]
                else:
                    creation_date = w.creation_date
                
                age_days = (datetime.now() - creation_date).days
                
                if age_days < 30:
                    return False, f"Domain is very new ({age_days} days old)"
                elif age_days < 90:
                    return True, f"Domain is relatively new ({age_days} days old)"
                else:
                    return True, f"Domain is established ({age_days} days old)"
            else:
                return False, "Could not determine domain age"
        except Exception as e:
            return True, f"Could not check domain age: {str(e)}"
    
    def check_suspicious_patterns(self, url):
        """Check for suspicious URL patterns"""
        for pattern in self.suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                return False, f"Contains suspicious pattern: {pattern}"
        return True, "No suspicious patterns detected"
    
    def check_blacklist(self, url):
        """Check if domain is blacklisted"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.lower()
        
        for blacklisted in self.blacklisted_domains:
            if blacklisted.lower() in domain:
                return False, f"Domain is blacklisted: {blacklisted}"
        
        return True, "Domain not in blacklist"
    
    def check_ssl_certificate(self, url):
        """Check SSL certificate validity"""
        try:
            if not url.startswith('https://'):
                return False, "No SSL certificate (HTTP only)"
            
            response = self.session.get(url, timeout=10, verify=True)
            return True, "Valid SSL certificate"
        except requests.exceptions.SSLError:
            return False, "Invalid SSL certificate"
        except Exception as e:
            return True, f"SSL check failed: {str(e)}"
    
    def check_website_content(self, url):
        """Analyze website content for spam indicators"""
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get text content
            text = soup.get_text().lower()
            title = soup.title.string.lower() if soup.title else ""
            
            spam_score = 0
            spam_indicators_found = []
            
            # Check for spam indicators in text
            for indicator in self.spam_indicators:
                if indicator in text or indicator in title:
                    spam_score += 1
                    spam_indicators_found.append(indicator)
            
            # Check for excessive links
            links = soup.find_all('a')
            if len(links) > 50:
                spam_score += 2
                spam_indicators_found.append("excessive_links")
            
            # Check for popup/redirect scripts
            scripts = soup.find_all('script')
            for script in scripts:
                script_text = str(script).lower()
                if 'window.open' in script_text or 'location.href' in script_text:
                    spam_score += 1
                    spam_indicators_found.append("suspicious_scripts")
            
            if spam_score >= 5:
                return False, f"High spam score ({spam_score}): {', '.join(spam_indicators_found)}"
            elif spam_score >= 3:
                return True, f"Moderate spam indicators ({spam_score}): {', '.join(spam_indicators_found)}"
            else:
                return True, "Low spam indicators"
                
        except Exception as e:
            return True, f"Content analysis failed: {str(e)}"
    
    def check_redirects(self, url):
        """Check for suspicious redirects"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=False)
            
            if response.status_code in [301, 302, 303, 307, 308]:
                redirect_url = response.headers.get('Location', '')
                if redirect_url:
                    # Check if redirect goes to different domain
                    original_domain = urlparse(url).netloc
                    redirect_domain = urlparse(redirect_url).netloc
                    
                    if original_domain != redirect_domain:
                        return False, f"Suspicious redirect to: {redirect_domain}"
            
            return True, "No suspicious redirects"
        except Exception as e:
            return True, f"Redirect check failed: {str(e)}"
    
    def check_url_safety(self, url):
        """Comprehensive URL safety check"""
        print(f"{Fore.CYAN}🔍 Analyzing URL: {url}{Style.RESET_ALL}")
        print("-" * 60)
        
        results = {}
        
        # 1. URL Format Validation
        is_valid, message = self.validate_url_format(url)
        results['format'] = {'safe': is_valid, 'message': message}
        self.print_result("URL Format", is_valid, message)
        
        if not is_valid:
            return results
        
        # 2. DNS Resolution
        is_safe, message = self.check_dns_resolution(url)
        results['dns'] = {'safe': is_safe, 'message': message}
        self.print_result("DNS Resolution", is_safe, message)
        
        # 3. Domain Age
        is_safe, message = self.check_domain_age(url)
        results['age'] = {'safe': is_safe, 'message': message}
        self.print_result("Domain Age", is_safe, message)
        
        # 4. Suspicious Patterns
        is_safe, message = self.check_suspicious_patterns(url)
        results['patterns'] = {'safe': is_safe, 'message': message}
        self.print_result("Suspicious Patterns", is_safe, message)
        
        # 5. Blacklist Check
        is_safe, message = self.check_blacklist(url)
        results['blacklist'] = {'safe': is_safe, 'message': message}
        self.print_result("Blacklist Check", is_safe, message)
        
        # 6. SSL Certificate
        is_safe, message = self.check_ssl_certificate(url)
        results['ssl'] = {'safe': is_safe, 'message': message}
        self.print_result("SSL Certificate", is_safe, message)
        
        # 7. Redirect Check
        is_safe, message = self.check_redirects(url)
        results['redirects'] = {'safe': is_safe, 'message': message}
        self.print_result("Redirect Check", is_safe, message)
        
        # 8. Content Analysis
        is_safe, message = self.check_website_content(url)
        results['content'] = {'safe': is_safe, 'message': message}
        self.print_result("Content Analysis", is_safe, message)
        
        # Overall assessment with percentage
        safe_checks = sum(1 for result in results.values() if result['safe'])
        total_checks = len(results)
        safety_percentage = round((safe_checks / total_checks) * 100, 1)
        
        print("-" * 60)
        print(f"{Fore.CYAN}📊 SAFETY SCORE: {safety_percentage}% ({safe_checks}/{total_checks} checks passed){Style.RESET_ALL}")
        
        if safety_percentage >= 80:
            print(f"{Fore.GREEN}✅ URL appears SAFE ({safety_percentage}% safety score){Style.RESET_ALL}")
        elif safety_percentage >= 60:
            print(f"{Fore.YELLOW}⚠️  URL has some concerns ({safety_percentage}% safety score){Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ URL appears UNSAFE ({safety_percentage}% safety score){Style.RESET_ALL}")
        
        return results
    
    def print_result(self, check_name, is_safe, message):
        """Print formatted check result"""
        status = f"{Fore.GREEN}✅ SAFE{Style.RESET_ALL}" if is_safe else f"{Fore.RED}❌ UNSAFE{Style.RESET_ALL}"
        print(f"{check_name:<20} {status} - {message}")
    
    def save_results(self, url, results, filename=None):
        """Save analysis results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"url_check_{timestamp}.json"
        
        # Calculate overall assessment if not already present
        if 'overall' not in results:
            safe_checks = sum(1 for result in results.values() if result['safe'])
            total_checks = len(results)
            safety_percentage = round((safe_checks / total_checks) * 100, 1)
            
            if safety_percentage >= 80:
                results['overall'] = {
                    'status': 'safe', 
                    'message': f'URL appears SAFE ({safe_checks}/{total_checks} checks passed)',
                    'percentage': safety_percentage,
                    'color': 'green'
                }
            elif safety_percentage >= 60:
                results['overall'] = {
                    'status': 'warning', 
                    'message': f'URL has some concerns ({safe_checks}/{total_checks} checks passed)',
                    'percentage': safety_percentage,
                    'color': 'orange'
                }
            else:
                results['overall'] = {
                    'status': 'unsafe', 
                    'message': f'URL appears UNSAFE ({safe_checks}/{total_checks} checks passed)',
                    'percentage': safety_percentage,
                    'color': 'red'
                }
        
        data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'results': results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n{Fore.CYAN}📄 Results saved to: {filename}{Style.RESET_ALL}")
        return filename
    
    def check_url_safety_web(self, url):
        """Web-compatible URL safety check (no console output)"""
        results = {}
        
        # 1. URL Format Validation
        is_valid, message = self.validate_url_format(url)
        results['format'] = {'safe': is_valid, 'message': message}
        
        if not is_valid:
            return results
        
        # 2. DNS Resolution
        is_safe, message = self.check_dns_resolution(url)
        results['dns'] = {'safe': is_safe, 'message': message}
        
        # 3. Domain Age
        is_safe, message = self.check_domain_age(url)
        results['age'] = {'safe': is_safe, 'message': message}
        
        # 4. Suspicious Patterns
        is_safe, message = self.check_suspicious_patterns(url)
        results['patterns'] = {'safe': is_safe, 'message': message}
        
        # 5. Blacklist Check
        is_safe, message = self.check_blacklist(url)
        results['blacklist'] = {'safe': is_safe, 'message': message}
        
        # 6. SSL Certificate
        is_safe, message = self.check_ssl_certificate(url)
        results['ssl'] = {'safe': is_safe, 'message': message}
        
        # 7. Redirect Check
        is_safe, message = self.check_redirects(url)
        results['redirects'] = {'safe': is_safe, 'message': message}
        
        # 8. Content Analysis
        is_safe, message = self.check_website_content(url)
        results['content'] = {'safe': is_safe, 'message': message}
        
        # Calculate overall assessment with percentage
        safe_checks = sum(1 for result in results.values() if result['safe'])
        total_checks = len(results)
        safety_percentage = round((safe_checks / total_checks) * 100, 1)
        
        if safety_percentage >= 80:
            results['overall'] = {
                'status': 'safe', 
                'message': f'URL appears SAFE ({safe_checks}/{total_checks} checks passed)',
                'percentage': safety_percentage,
                'color': 'green'
            }
        elif safety_percentage >= 60:
            results['overall'] = {
                'status': 'warning', 
                'message': f'URL has some concerns ({safe_checks}/{total_checks} checks passed)',
                'percentage': safety_percentage,
                'color': 'orange'
            }
        else:
            results['overall'] = {
                'status': 'unsafe', 
                'message': f'URL appears UNSAFE ({safe_checks}/{total_checks} checks passed)',
                'percentage': safety_percentage,
                'color': 'red'
            }
        
        return results
