#!/usr/bin/env python3
"""
Safe URL Checker - A comprehensive tool to check if URLs are safe, legal, and not spam
"""

import sys
import os
from url_checker import SafeURLChecker
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print application banner"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                    🔒 SAFE URL CHECKER 🔒                    ║
║                                                              ║
║  A comprehensive tool to verify URL safety, legality,       ║
║  and detect spam/advertisement content                      ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_help():
    """Print help information"""
    help_text = f"""
{Fore.YELLOW}Usage:{Style.RESET_ALL}
  python main.py <URL>                    # Check a single URL
  python main.py --file <filename>        # Check URLs from file
  python main.py --interactive            # Interactive mode
  python main.py --help                   # Show this help

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  python main.py https://example.com
  python main.py --file urls.txt
  python main.py --interactive

{Fore.YELLOW}Features:{Style.RESET_ALL}
  ✅ URL format validation
  ✅ DNS resolution check
  ✅ Domain age verification
  ✅ Suspicious pattern detection
  ✅ Blacklist checking
  ✅ SSL certificate validation
  ✅ Redirect analysis
  ✅ Content spam detection
  ✅ Results export to JSON
"""
    print(help_text)

def check_single_url(url, checker):
    """Check a single URL"""
    try:
        results = checker.check_url_safety(url)
        checker.save_results(url, results)
        return results
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Analysis interrupted by user{Style.RESET_ALL}")
        return None
    except Exception as e:
        print(f"\n{Fore.RED}❌ Error analyzing URL: {str(e)}{Style.RESET_ALL}")
        return None

def check_urls_from_file(filename, checker):
    """Check multiple URLs from a file"""
    try:
        if not os.path.exists(filename):
            print(f"{Fore.RED}❌ File not found: {filename}{Style.RESET_ALL}")
            return
        
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
        
        if not urls:
            print(f"{Fore.YELLOW}⚠️  No URLs found in file: {filename}{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}📁 Found {len(urls)} URLs to check{Style.RESET_ALL}\n")
        
        for i, url in enumerate(urls, 1):
            print(f"{Fore.CYAN}[{i}/{len(urls)}] Checking: {url}{Style.RESET_ALL}")
            results = check_single_url(url, checker)
            print("\n" + "="*80 + "\n")
            
    except Exception as e:
        print(f"{Fore.RED}❌ Error reading file: {str(e)}{Style.RESET_ALL}")

def interactive_mode(checker):
    """Run in interactive mode"""
    print(f"{Fore.CYAN}🎯 Interactive Mode - Enter URLs to check (type 'quit' to exit){Style.RESET_ALL}\n")
    
    while True:
        try:
            url = input(f"{Fore.GREEN}Enter URL: {Style.RESET_ALL}").strip()
            
            if url.lower() in ['quit', 'exit', 'q']:
                print(f"{Fore.CYAN}👋 Goodbye!{Style.RESET_ALL}")
                break
            
            if not url:
                continue
            
            print()
            results = check_single_url(url, checker)
            print()
            
            # Ask if user wants to save results
            save = input(f"{Fore.YELLOW}Save results to file? (y/n): {Style.RESET_ALL}").lower()
            if save in ['y', 'yes']:
                filename = input(f"{Fore.YELLOW}Enter filename (or press Enter for auto): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = None
                checker.save_results(url, results, filename)
            
            print("\n" + "="*80 + "\n")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⚠️  Exiting interactive mode{Style.RESET_ALL}")
            break
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {str(e)}{Style.RESET_ALL}")

def create_sample_files():
    """Create sample files for testing"""
    # Create sample URLs file
    sample_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.example.com",
        "https://www.wikipedia.org"
    ]
    
    with open('sample_urls.txt', 'w') as f:
        for url in sample_urls:
            f.write(url + '\n')
    
    # Create sample blacklist
    sample_blacklist = [
        "malware.example.com",
        "phishing.example.com",
        "scam.example.com",
        "fake-bank.example.com"
    ]
    
    with open('blacklist.json', 'w') as f:
        import json
        json.dump(sample_blacklist, f, indent=2)
    
    print(f"{Fore.GREEN}✅ Created sample files:{Style.RESET_ALL}")
    print(f"  - sample_urls.txt (sample URLs to test)")
    print(f"  - blacklist.json (sample blacklist)")

def main():
    """Main application entry point"""
    print_banner()
    
    # Parse command line arguments
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        print_help()
        return
    
    # Initialize URL checker
    try:
        checker = SafeURLChecker()
        print(f"{Fore.GREEN}✅ URL Checker initialized successfully{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"{Fore.RED}❌ Failed to initialize URL checker: {str(e)}{Style.RESET_ALL}")
        return
    
    # Handle different modes
    if '--file' in args:
        try:
            file_index = args.index('--file')
            if file_index + 1 < len(args):
                filename = args[file_index + 1]
                check_urls_from_file(filename, checker)
            else:
                print(f"{Fore.RED}❌ No filename provided for --file option{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Invalid --file usage{Style.RESET_ALL}")
    
    elif '--interactive' in args or '-i' in args:
        interactive_mode(checker)
    
    elif '--create-samples' in args:
        create_sample_files()
    
    else:
        # Single URL mode
        url = args[0]
        check_single_url(url, checker)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Application interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)
