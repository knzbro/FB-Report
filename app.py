#!/usr/bin/env python3
# MDF Legends - REAL Facebook Reporting Tool
# Actually works - Not Fake!
# Powered By Al'mudafioon Force

import os
import sys
import time
import json
import random
import subprocess
import platform
from datetime import datetime
import threading

# Try to import selenium
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# ==================== TERMUX DETECTION ====================

def is_termux():
    return 'com.termux' in os.environ.get('PREFIX', '')

def is_android():
    return 'android' in platform.system().lower() or is_termux()

# ==================== COLORS ====================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    @staticmethod
    def success(msg): print(f"{Colors.GREEN}{msg}{Colors.END}")
    def error(msg): print(f"{Colors.RED}{msg}{Colors.END}")
    def warning(msg): print(f"{Colors.YELLOW}{msg}{Colors.END}")
    def info(msg): print(f"{Colors.CYAN}{msg}{Colors.END}")
    def header(msg): print(f"{Colors.BOLD}{Colors.HEADER}{msg}{Colors.END}")

# ==================== CHROMEDRIVER CHECK ====================

class ChromeDriverChecker:
    def __init__(self):
        self.driver_path = None
        self.chrome_path = None
    
    def check(self):
        """Check if ChromeDriver is available"""
        Colors.header("\n🔍 CHECKING CHROMEDRIVER...")
        
        # Check in PATH
        try:
            result = subprocess.run(['which', 'chromedriver'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.driver_path = result.stdout.strip()
                Colors.success(f"✅ ChromeDriver found: {self.driver_path}")
                
                # Check version
                version = subprocess.run([self.driver_path, '--version'], 
                                       capture_output=True, text=True)
                Colors.info(f"   Version: {version.stdout.strip()}")
                return True
        except:
            pass
        
        # Check in common Termux location
        termux_path = '/data/data/com.termux/files/usr/bin/chromedriver'
        if os.path.exists(termux_path):
            self.driver_path = termux_path
            Colors.success(f"✅ ChromeDriver found: {termux_path}")
            return True
        
        Colors.error("❌ ChromeDriver not found!")
        return False
    
    def check_browser(self):
        """Check for Chrome/Chromium"""
        if is_termux():
            # Termux: check chromium
            try:
                result = subprocess.run(['which', 'chromium'], 
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    self.chrome_path = result.stdout.strip()
                    Colors.success(f"✅ Chromium found: {self.chrome_path}")
                    return True
            except:
                pass
        else:
            # Other platforms: check chrome
            browsers = ['google-chrome', 'google-chrome-stable', 'chrome']
            for browser in browsers:
                try:
                    result = subprocess.run(['which', browser], 
                                           capture_output=True, text=True)
                    if result.returncode == 0:
                        self.chrome_path = result.stdout.strip()
                        Colors.success(f"✅ Chrome found: {self.chrome_path}")
                        return True
                except:
                    continue
        
        Colors.error("❌ No browser found!")
        return False

# ==================== REAL FACEBOOK REPORTER ====================

class RealFacebookReporter:
    def __init__(self, email, password, driver_path, chrome_path=None):
        self.email = email
        self.password = password
        self.driver_path = driver_path
        self.chrome_path = chrome_path
        self.driver = None
        self.wait = None
        self.logs = []
        
    def log(self, msg, type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
        
        if type == "success":
            Colors.success(log_entry)
        elif type == "error":
            Colors.error(log_entry)
        elif type == "warning":
            Colors.warning(log_entry)
        else:
            print(log_entry)
    
    def setup_driver(self):
        """Setup Chrome/Chromium driver"""
        self.log("🚀 Setting up browser driver...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Add random user agent to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')
        
        # Set binary location if provided
        if self.chrome_path:
            options.binary_location = self.chrome_path
        
        try:
            service = Service(self.driver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 15)
            self.log("✅ Browser setup complete", "success")
            return True
        except Exception as e:
            self.log(f"❌ Browser setup failed: {e}", "error")
            return False
    
    def login(self):
        """Real Facebook login"""
        self.log("\n🔑 Logging into Facebook...")
        
        try:
            self.driver.get("https://m.facebook.com")
            time.sleep(3)
            
            # Email field
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.send_keys(self.email)
            self.log("📧 Email entered")
            
            # Password field
            pass_field = self.driver.find_element(By.NAME, "pass")
            pass_field.send_keys(self.password)
            self.log("🔑 Password entered")
            
            # Random delay to simulate human
            time.sleep(random.uniform(1, 3))
            
            # Login button
            login_btn = self.driver.find_element(By.NAME, "login")
            login_btn.click()
            self.log("🔓 Login button clicked")
            
            time.sleep(5)
            
            # Check login success
            cookies = self.driver.get_cookies()
            for cookie in cookies:
                if cookie['name'] == 'c_user':
                    self.log(f"✅ Login successful! User ID: {cookie['value']}", "success")
                    return True
            
            self.log("❌ Login failed - Check credentials", "error")
            return False
            
        except Exception as e:
            self.log(f"❌ Login error: {e}", "error")
            return False
    
    def report_profile(self, profile_url, reason="Fake account"):
        """Real profile reporting"""
        self.log(f"\n🎯 Reporting profile: {profile_url}")
        
        try:
            # Use mobile version for better compatibility
            mobile_url = profile_url.replace("www.", "m.").replace("facebook.com", "m.facebook.com")
            self.driver.get(mobile_url)
            self.log("📍 Profile opened")
            time.sleep(4)
            
            # Click menu button
            menu_selectors = [
                "//div[@aria-label='Actions for this profile']",
                "//div[@aria-label='More']",
                "//div[@role='button']//span[text()='More']",
                "//div[contains(@class, 'x1i10hfl')]//span[text()='More']"
            ]
            
            menu_clicked = False
            for selector in menu_selectors:
                try:
                    menu = self.driver.find_element(By.XPATH, selector)
                    menu.click()
                    self.log("✅ Menu button clicked", "success")
                    menu_clicked = True
                    break
                except:
                    continue
            
            if not menu_clicked:
                self.log("❌ Menu button not found", "error")
                return False
            
            time.sleep(2)
            
            # Find report option
            report_selectors = [
                "//span[text()='Find support or report profile']",
                "//span[contains(text(), 'report profile')]",
                "//span[contains(text(), 'Report')]",
                "//div[@role='menuitem'][contains(text(), 'Report')]"
            ]
            
            report_clicked = False
            for selector in report_selectors:
                try:
                    report = self.driver.find_element(By.XPATH, selector)
                    report.click()
                    self.log("✅ Report option clicked", "success")
                    report_clicked = True
                    break
                except:
                    continue
            
            if not report_clicked:
                self.log("❌ Report option not found", "error")
                return False
            
            time.sleep(3)
            
            # Select reason
            reason_options = [reason, reason.lower(), reason.title()]
            reason_selected = False
            
            for r in reason_options:
                try:
                    reason_elem = self.driver.find_element(By.XPATH, f"//span[contains(text(), '{r}')]")
                    reason_elem.click()
                    self.log(f"✅ Reason selected: {reason}", "success")
                    reason_selected = True
                    break
                except:
                    continue
            
            if not reason_selected:
                self.log("⚠️ Could not select reason, continuing...", "warning")
            
            time.sleep(2)
            
            # Submit report
            submit_selectors = [
                "//div[@role='button'][contains(text(), 'Submit')]",
                "//span[text()='Submit']",
                "//button[contains(text(), 'Submit')]"
            ]
            
            for selector in submit_selectors:
                try:
                    submit = self.driver.find_element(By.XPATH, selector)
                    submit.click()
                    self.log("✅ Report submitted!", "success")
                    break
                except:
                    continue
            
            time.sleep(3)
            self.log("🎉 Reporting complete!", "success")
            return True
            
        except Exception as e:
            self.log(f"❌ Reporting error: {e}", "error")
            return False
    
    def close(self):
        """Close browser"""
        if self.driver:
            time.sleep(3)
            self.driver.quit()
            self.log("🚪 Browser closed")

# ==================== MAIN TERMINAL UI ====================

class TerminalUI:
    def __init__(self):
        self.checker = ChromeDriverChecker()
        self.accounts = []
        self.targets = []
        self.load_data()
    
    def load_data(self):
        """Load saved data"""
        try:
            with open('mdf_data.json', 'r') as f:
                data = json.load(f)
                self.accounts = data.get('accounts', [])
                self.targets = data.get('targets', [])
        except:
            self.accounts = []
            self.targets = []
    
    def save_data(self):
        """Save data"""
        data = {
            'accounts': self.accounts,
            'targets': self.targets
        }
        with open('mdf_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║              🔴 MDF LEGENDS - REAL FACEBOOK REPORTER             ║
║                    {Colors.YELLOW}*ACTUALLY WORKS*{Colors.RED}{Colors.BOLD}                          ║
║                Powered By {Colors.YELLOW}Al'mudafioon Force{Colors.RED}{Colors.BOLD}                ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def print_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗
║                         MAIN MENU                              ║
╠════════════════════════════════════════════════════════════════╣
║  {Colors.GREEN}1.{Colors.END} 🔍 Check ChromeDriver & Browser                          ║
║  {Colors.GREEN}2.{Colors.END} 👤 Add Facebook Account                                  ║
║  {Colors.GREEN}3.{Colors.END} 🎯 Add Target Profile                                    ║
║  {Colors.GREEN}4.{Colors.END} 📋 View Saved Data                                       ║
║  {Colors.GREEN}5.{Colors.END} 🚀 Start REAL Reporting                                  ║
║  {Colors.GREEN}6.{Colors.END} ❓ Help                                                  ║
║  {Colors.GREEN}0.{Colors.END} 🚪 Exit                                                  ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}
        """
        print(menu)
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Colors.GREEN}👉 Select option: {Colors.END}")
            
            if choice == '1':
                self.check_driver()
            elif choice == '2':
                self.add_account()
            elif choice == '3':
                self.add_target()
            elif choice == '4':
                self.view_data()
            elif choice == '5':
                self.start_reporting()
            elif choice == '6':
                self.show_help()
            elif choice == '0':
                Colors.success("\n👋 Goodbye!")
                sys.exit(0)
    
    def check_driver(self):
        self.clear_screen()
        self.print_banner()
        Colors.header("\n🔍 SYSTEM CHECK")
        
        driver_ok = self.checker.check()
        browser_ok = self.checker.check_browser()
        
        if driver_ok and browser_ok:
            Colors.success("\n✅ Ready to report!")
        else:
            Colors.error("\n❌ Please install missing components")
            self.show_install_instructions()
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def show_install_instructions(self):
        Colors.header("\n📦 INSTALLATION INSTRUCTIONS:")
        if is_termux():
            print("""
    pkg update
    pkg install tur-repo chromium -y
    pkg install python -y
    pip install selenium
            """)
        else:
            print("""
    pip install selenium webdriver-manager
    # Download ChromeDriver from https://chromedriver.chromium.org/
            """)
    
    def add_account(self):
        self.clear_screen()
        self.print_banner()
        Colors.header("\n👤 ADD FACEBOOK ACCOUNT")
        
        email = input("📧 Email/Phone: ")
        password = input("🔑 Password: ")
        
        self.accounts.append({
            'email': email,
            'password': password
        })
        self.save_data()
        Colors.success("✅ Account added!")
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def add_target(self):
        self.clear_screen()
        self.print_banner()
        Colors.header("\n🎯 ADD TARGET PROFILE")
        
        url = input("🔗 Facebook Profile URL: ")
        if 'facebook.com' in url:
            self.targets.append(url)
            self.save_data()
            Colors.success("✅ Target added!")
        else:
            Colors.error("❌ Invalid Facebook URL")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def view_data(self):
        self.clear_screen()
        self.print_banner()
        Colors.header("\n📋 SAVED DATA")
        
        print(f"\n{Colors.CYAN}Accounts ({len(self.accounts)}):{Colors.END}")
        for i, acc in enumerate(self.accounts, 1):
            print(f"  {i}. {acc['email']}")
        
        print(f"\n{Colors.CYAN}Targets ({len(self.targets)}):{Colors.END}")
        for i, target in enumerate(self.targets, 1):
            print(f"  {i}. {target[:60]}...")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def start_reporting(self):
        self.clear_screen()
        self.print_banner()
        
        # Check prerequisites
        if not self.accounts:
            Colors.error("❌ No accounts added!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        if not self.targets:
            Colors.error("❌ No targets added!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        if not self.checker.check() or not self.checker.check_browser():
            Colors.error("❌ ChromeDriver not ready!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        if not SELENIUM_AVAILABLE:
            Colors.error("❌ Selenium not installed!")
            input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
            return
        
        Colors.header("\n🚀 STARTING REAL REPORTING...")
        
        # Ask for reason
        print(f"\n{Colors.CYAN}Select reason:{Colors.END}")
        reasons = ['Fake account', 'Harassment', 'Hate speech', 'Scam', 'Nudity', 'Violence']
        for i, r in enumerate(reasons, 1):
            print(f"  {i}. {r}")
        
        try:
            reason_choice = int(input(f"\n{Colors.GREEN}Select reason (1-6): {Colors.END}")) - 1
            reason = reasons[reason_choice] if 0 <= reason_choice < len(reasons) else 'Fake account'
        except:
            reason = 'Fake account'
        
        # Ask for reports per target
        try:
            reports_per_target = int(input(f"\n{Colors.GREEN}Reports per target (1-10): {Colors.END}"))
            reports_per_target = max(1, min(10, reports_per_target))
        except:
            reports_per_target = 1
        
        Colors.header("\n📊 ATTACK CONFIGURATION:")
        print(f"   Accounts: {len(self.accounts)}")
        print(f"   Targets: {len(self.targets)}")
        print(f"   Reports per target: {reports_per_target}")
        print(f"   Reason: {reason}")
        
        confirm = input(f"\n{Colors.RED}Start REAL reporting? (yes/no): {Colors.END}")
        
        if confirm.lower() != 'yes':
            return
        
        # Start reporting
        total_reports = len(self.targets) * reports_per_target
        current_report = 0
        successful = 0
        failed = 0
        
        for target in self.targets:
            for report_num in range(reports_per_target):
                current_report += 1
                
                # Use account in round-robin
                account = self.accounts[(current_report - 1) % len(self.accounts)]
                
                print(f"\n{Colors.BOLD}{Colors.CYAN}[{current_report}/{total_reports}] Reporting to {target[:50]}...{Colors.END}")
                
                reporter = RealFacebookReporter(
                    account['email'],
                    account['password'],
                    self.checker.driver_path,
                    self.checker.chrome_path
                )
                
                if reporter.setup_driver():
                    if reporter.login():
                        if reporter.report_profile(target, reason):
                            successful += 1
                        else:
                            failed += 1
                    reporter.close()
                
                # Random delay between reports
                if current_report < total_reports:
                    delay = random.randint(30, 60)
                    print(f"\n{Colors.YELLOW}⏳ Waiting {delay} seconds before next report...{Colors.END}")
                    
                    # Show countdown
                    for i in range(delay, 0, -5):
                        if i > 5:
                            print(f"   {i} seconds remaining...")
                            time.sleep(5)
                        else:
                            time.sleep(i)
        
        Colors.header("\n🎉 REPORTING COMPLETE!")
        print(f"   Successful: {Colors.GREEN}{successful}{Colors.END}")
        print(f"   Failed: {Colors.RED}{failed}{Colors.END}")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def show_help(self):
        self.clear_screen()
        self.print_banner()
        Colors.header("\n❓ HELP")
        
        help_text = f"""
{Colors.GREEN}ABOUT:{Colors.END}
  This is a REAL Facebook reporting tool.
  It actually opens browser and submits reports.

{Colors.GREEN}REQUIREMENTS:{Colors.END}
  • Chrome/Chromium browser
  • ChromeDriver installed
  • Real Facebook account(s)
  • Target profile URLs

{Colors.GREEN}HOW TO USE:{Colors.END}
  1. Option 1: Check ChromeDriver
  2. Option 2: Add your Facebook account
  3. Option 3: Add target profiles
  4. Option 5: Start REAL reporting

{Colors.GREEN}TIPS:{Colors.END}
  • Use multiple accounts for more reports
  • Add delays to avoid detection
  • Facebook may limit reports
  • Always use responsibly

{Colors.RED}WARNING:{Colors.END}
  This tool actually sends reports to Facebook.
  Use on your own risk!
        """
        print(help_text)
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        ui = TerminalUI()
        ui.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}\n👋 Goodbye!{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
        sys.exit(1)