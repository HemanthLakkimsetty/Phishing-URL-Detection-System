# Phishing URL Detection System

A Python tool to check if URLs are safe, legal, and not spam. This tool performs multiple security checks to help you identify potentially malicious or suspicious URLs before accessing them.

It supports:
- Web interface (recommended)
- Command line interface
- Batch checking from a text file

## What This Project Checks

- URL format validation
- DNS/domain resolution
- Domain age lookup
- Suspicious URL patterns
- Local blacklist match
- SSL certificate check
- Redirect behavior
- Basic content spam indicators

## Project Files

- `web_interface.py` - Flask web app
- `main.py` - Command line runner
- `url_checker.py` - Core detection logic
- `templates/index.html` - Web UI page
- `blacklist.json` - Local blacklist entries
- `sample_urls.txt` - Example URLs for testing
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.7+
- Internet connection (for DNS, whois, and content checks)

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run web app (easiest)

```bash
python web_interface.py
```

Open: `http://localhost:5000`

Windows shortcut:

```bat
start_web.bat
```

### 3. Run command line mode

Single URL:

```bash
python main.py https://example.com
```

Interactive mode:

```bash
python main.py --interactive
```

Batch mode:

```bash
python main.py --file sample_urls.txt
```

Windows shortcut:

```bat
run_checker.bat
```

## Output

- Web mode saves results like: `url_check_YYYYMMDD_HHMMSS.json`
- Batch web mode saves results like: `batch_url_check_YYYYMMDD_HHMMSS.json`
- CLI mode also saves JSON report files

## Customize

- Edit `blacklist.json` to add/remove blocked domains
- Edit `spam_indicators` in `url_checker.py` to adjust content checks

## Troubleshooting

- `ModuleNotFoundError`: run `pip install -r requirements.txt`
- Port already in use: stop old process or run app on a different port
- Timeout/network errors: check your internet connection and retry

## Notes

- This tool gives heuristic checks, not a guarantee.
- Some safe sites may be flagged, and some risky sites may pass.
- Use results as guidance, not final proof.

