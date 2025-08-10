# 🔒 Safe URL Checker

A comprehensive Python tool to check if URLs are safe, legal, and not spam. This tool performs multiple security checks to help you identify potentially malicious or suspicious URLs before accessing them.

## ✨ Features

- **URL Format Validation** - Ensures proper URL structure
- **DNS Resolution Check** - Verifies domain resolves to valid IP addresses
- **Domain Age Verification** - Checks how long the domain has been registered
- **Suspicious Pattern Detection** - Identifies known malicious URL patterns
- **Blacklist Checking** - Compares against known malicious domains
- **SSL Certificate Validation** - Ensures secure HTTPS connections
- **Redirect Analysis** - Detects suspicious redirects to different domains
- **Content Spam Detection** - Analyzes website content for spam indicators
- **Results Export** - Saves detailed analysis to JSON files
- **Multiple Input Modes** - Single URL, file-based, or interactive mode

## 🚀 Installation

1. **Clone or download the project files**
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 📋 Requirements

- Python 3.7 or higher
- Internet connection for URL checking
- Required packages (see `requirements.txt`):
  - requests
  - validators
  - beautifulsoup4
  - python-whois
  - dnspython
  - colorama
  - tldextract

## 🎯 Usage

### 🌐 Web Interface (Recommended)
```bash
python web_interface.py
```
Then open your browser to `http://localhost:5000`

**Or use the Windows launcher:**
```bash
start_web.bat
```

### 📱 Demo Interface
Open `simple_interface.html` in your browser for a demo version.

### 💻 Command Line Interface

#### Single URL Check
```bash
python main.py https://example.com
```

#### Check Multiple URLs from File
```bash
python main.py --file urls.txt
```

#### Interactive Mode
```bash
python main.py --interactive
```

#### Show Help
```bash
python main.py --help
```

#### Create Sample Files
```bash
python main.py --create-samples
```

## 📁 File Structure

```
safe-url-checker/
├── main.py                 # Command line application
├── web_interface.py        # Web server (Flask)
├── url_checker.py          # Core URL checking logic
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── QUICK_START.md         # Quick start guide
├── run_checker.bat        # Windows CLI launcher
├── start_web.bat          # Windows web launcher
├── simple_interface.html  # Demo HTML interface
├── templates/
│   └── index.html         # Web interface template
├── blacklist.json         # Blacklisted domains
├── sample_urls.txt        # Sample URLs for testing
└── url_check_*.json       # Analysis results (auto-generated)
```

## 🔍 Security Checks Explained

### 1. URL Format Validation
- Validates proper URL structure
- Ensures protocol (http/https) is present
- Checks for valid characters and format

### 2. DNS Resolution
- Resolves domain to IP addresses
- Detects suspicious IP patterns (localhost, private IPs)
- Ensures domain is accessible

### 3. Domain Age
- Checks domain registration date
- Flags very new domains (< 30 days) as suspicious
- Established domains (> 90 days) are considered safer

### 4. Suspicious Patterns
- Detects URL shorteners (bit.ly, tinyurl, etc.)
- Identifies IP addresses in URLs
- Finds very long random strings

### 5. Blacklist Check
- Compares against known malicious domains
- Uses customizable blacklist file
- Can be updated with new threats

### 6. SSL Certificate
- Validates HTTPS certificates
- Ensures secure connections
- Flags HTTP-only sites as less secure

### 7. Redirect Analysis
- Checks for suspicious redirects
- Detects cross-domain redirects
- Identifies potential phishing attempts

### 8. Content Analysis
- Analyzes website content for spam indicators
- Detects excessive advertising language
- Identifies suspicious scripts and popups

## 📊 Output Example

```
🔍 Analyzing URL: https://example.com
------------------------------------------------------------
URL Format          ✅ SAFE - Valid URL format
DNS Resolution      ✅ SAFE - DNS resolves to: 93.184.216.34
Domain Age          ✅ SAFE - Domain is established (8000+ days old)
Suspicious Patterns ✅ SAFE - No suspicious patterns detected
Blacklist Check     ✅ SAFE - Domain not in blacklist
SSL Certificate     ✅ SAFE - Valid SSL certificate
Redirect Check      ✅ SAFE - No suspicious redirects
Content Analysis    ✅ SAFE - Low spam indicators
------------------------------------------------------------
✅ URL appears SAFE (8/8 checks passed)
```

## ⚙️ Configuration

### Customizing Blacklist
Edit `blacklist.json` to add or remove domains:
```json
[
    "malware.example.com",
    "phishing.example.com",
    "scam.example.com"
]
```

### Adjusting Spam Detection
Modify the `spam_indicators` list in `url_checker.py` to customize spam detection keywords.

## 🛡️ Safety Features

- **Timeout Protection** - Prevents hanging on slow responses
- **Error Handling** - Graceful handling of network issues
- **User-Agent Spoofing** - Mimics real browser requests
- **Rate Limiting** - Built-in delays to avoid overwhelming servers
- **Safe Content Parsing** - Uses BeautifulSoup for safe HTML parsing

## ⚠️ Limitations

- **False Positives** - Some legitimate sites may be flagged
- **Network Dependent** - Requires internet connection
- **Not Real-time** - Results are based on current analysis
- **Limited to Public APIs** - Uses publicly available information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## ⚡ Quick Start

### 🌐 Web Interface (Easiest)
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start web server:**
   ```bash
   python web_interface.py
   ```

3. **Open browser:**
   Go to `http://localhost:5000`

4. **Paste URL and check!**

### 💻 Command Line
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test with a sample URL:**
   ```bash
   python main.py https://www.google.com
   ```

3. **Try interactive mode:**
   ```bash
   python main.py --interactive
   ```

### 📱 Demo Version
Simply open `simple_interface.html` in your browser for a demo!

## 🔧 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Install missing dependencies with `pip install -r requirements.txt`
2. **SSL Certificate Errors**: Some sites may have invalid certificates
3. **Timeout Errors**: Network issues or slow servers
4. **Permission Errors**: Ensure write permissions for result files

### Getting Help

- Check the help menu: `python main.py --help`
- Review error messages for specific issues
- Ensure all dependencies are installed correctly

---

**⚠️ Disclaimer**: This tool is for educational and security assessment purposes. Always use responsibly and in accordance with applicable laws and terms of service.
