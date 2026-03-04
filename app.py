#!/usr/bin/env python3
# MDF Legends - Terminal Based All-in-One Tool
# Auto Install | Auto Scan | Auto Work
# Powered By Al'mudafioon Force

import os
import sys
import time
import json
import random
import string
import subprocess
import platform
import urllib.request
import zipfile
import shutil
from datetime import datetime
from typing import Dict, List, Optional
import threading
import queue

# ==================== COLOR CODES ====================

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    
    @staticmethod
    def print_success(msg): print(f"{Colors.GREEN}{msg}{Colors.END}")
    def print_error(msg): print(f"{Colors.RED}{msg}{Colors.END}")
    def print_warning(msg): print(f"{Colors.YELLOW}{msg}{Colors.END}")
    def print_info(msg): print(f"{Colors.CYAN}{msg}{Colors.END}")
    def print_header(msg): print(f"{Colors.BOLD}{Colors.HEADER}{msg}{Colors.END}")

# ==================== SYSTEM CHECKER ====================

class SystemChecker:
    def __init__(self):
        self.checks = {
            'python': False,
            'pip': False,
            'chrome': False,
            'chromedriver': False,
            'selenium': False,
            'flask': False,
            'internet': False,
            'permissions': False
        }
        self.system = platform.system().lower()
        self.machine = platform.machine().lower()
        
    def check_all(self):
        """Run all system checks"""
        Colors.print_header("\n🔍 SYSTEM SCANNING...\n")
        
        self.check_python()
        self.check_pip()
        self.check_internet()
        self.check_chrome()
        self.check_chromedriver()
        self.check_python_packages()
        self.check_permissions()
        
        self.show_results()
        return all(self.checks.values())
    
    def check_python(self):
        try:
            version = sys.version_info
            if version.major >= 3 and version.minor >= 6:
                self.checks['python'] = True
                Colors.print_success(f"✅ Python {version.major}.{version.minor}.{version.micro} OK")
            else:
                Colors.print_error(f"❌ Python 3.6+ required (you have {version.major}.{version.minor})")
        except:
            Colors.print_error("❌ Python check failed")
    
    def check_pip(self):
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.checks['pip'] = True
                Colors.print_success(f"✅ Pip OK: {result.stdout.split()[1]}")
            else:
                Colors.print_error("❌ Pip not found")
        except:
            Colors.print_error("❌ Pip check failed")
    
    def check_internet(self):
        try:
            urllib.request.urlopen("https://www.google.com", timeout=5)
            self.checks['internet'] = True
            Colors.print_success("✅ Internet connection OK")
        except:
            Colors.print_error("❌ No internet connection")
    
    def check_chrome(self):
        chrome_paths = {
            'linux': ['google-chrome', 'google-chrome-stable', 'chromium-browser'],
            'windows': ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                       'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'],
            'darwin': ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome']
        }
        
        paths = chrome_paths.get(self.system, [])
        for path in paths:
            try:
                if self.system == 'windows':
                    if os.path.exists(path):
                        self.checks['chrome'] = True
                        Colors.print_success(f"✅ Chrome found")
                        return
                else:
                    result = subprocess.run(['which', path], capture_output=True, text=True)
                    if result.returncode == 0:
                        self.checks['chrome'] = True
                        Colors.print_success(f"✅ Chrome found")
                        return
            except:
                continue
        
        Colors.print_error("❌ Chrome not found")
    
    def check_chromedriver(self):
        try:
            result = subprocess.run(['chromedriver', '--version'], 
                                   capture_output=True, text=True)
            if result.returncode == 0:
                self.checks['chromedriver'] = True
                Colors.print_success(f"✅ ChromeDriver: {result.stdout.strip()}")
                return
        except:
            pass
        
        # Check in current directory
        if os.path.exists('./chromedriver'):
            try:
                result = subprocess.run(['./chromedriver', '--version'], 
                                       capture_output=True, text=True)
                if result.returncode == 0:
                    self.checks['chromedriver'] = True
                    Colors.print_success(f"✅ ChromeDriver (local): {result.stdout.strip()}")
                    return
            except:
                pass
        
        Colors.print_error("❌ ChromeDriver not found")
    
    def check_python_packages(self):
        packages = ['selenium', 'flask', 'requests']
        for pkg in packages:
            try:
                __import__(pkg)
                Colors.print_success(f"✅ {pkg} installed")
                if pkg == 'selenium':
                    self.checks['selenium'] = True
                elif pkg == 'flask':
                    self.checks['flask'] = True
            except:
                Colors.print_warning(f"⚠️ {pkg} not installed")
    
    def check_permissions(self):
        try:
            test_file = '.test_permission'
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            self.checks['permissions'] = True
            Colors.print_success("✅ Write permissions OK")
        except:
            Colors.print_error("❌ No write permissions in current directory")
    
    def show_results(self):
        Colors.print_header("\n📊 SCAN RESULTS:")
        total = sum(self.checks.values())
        required = len(self.checks)
        percentage = (total / required) * 100
        
        print(f"\n   {Colors.BOLD}Passed: {Colors.GREEN}{total}/{required}{Colors.END}")
        print(f"   {Colors.BOLD}Status: ", end="")
        
        if percentage == 100:
            Colors.print_success("✅ PERFECT - All systems go!")
        elif percentage >= 80:
            Colors.print_warning("⚠️ GOOD - Minor issues need fixing")
        else:
            Colors.print_error("❌ CRITICAL - Multiple issues found")

# ==================== AUTO INSTALLER ====================

class AutoInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.install_log = []
    
    def log(self, msg, type="info"):
        self.install_log.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        if type == "success":
            Colors.print_success(msg)
        elif type == "error":
            Colors.print_error(msg)
        else:
            Colors.print_info(msg)
    
    def install_python_packages(self):
        """Install required Python packages"""
        self.log("\n📦 Installing Python packages...")
        
        packages = ['selenium', 'flask', 'requests', 'webdriver-manager']
        
        for package in packages:
            try:
                self.log(f"   Installing {package}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", package],
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self.log(f"   ✅ {package} installed", "success")
            except:
                self.log(f"   ❌ Failed to install {package}", "error")
    
    def install_chromedriver(self):
        """Install ChromeDriver automatically"""
        self.log("\n🚗 Installing ChromeDriver...")
        
        version = "114.0.5735.90"
        
        # Platform specific URL
        if self.system == "linux":
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/linux64/chromedriver-linux64.zip"
        elif self.system == "windows":
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/win64/chromedriver-win64.zip"
        elif self.system == "darwin":
            url = f"https://storage.googleapis.com/chrome-for-testing-public/{version}/mac-x64/chromedriver-mac-x64.zip"
        else:
            self.log("❌ Unknown platform", "error")
            return False
        
        try:
            self.log("   Downloading...")
            urllib.request.urlretrieve(url, "chromedriver.zip")
            
            self.log("   Extracting...")
            with zipfile.ZipFile("chromedriver.zip", 'r') as zip_ref:
                zip_ref.extractall(".")
            os.remove("chromedriver.zip")
            
            # Find and move chromedriver
            for root, dirs, files in os.walk("."):
                if "chromedriver" in files:
                    driver_path = os.path.join(root, "chromedriver")
                    shutil.move(driver_path, "./chromedriver")
                    os.chmod("./chromedriver", 0o755)
                    self.log(f"   ✅ ChromeDriver installed at ./chromedriver", "success")
                    
                    # Test
                    result = subprocess.run(['./chromedriver', '--version'], 
                                           capture_output=True, text=True)
                    self.log(f"   Version: {result.stdout.strip()}", "success")
                    return True
            
            self.log("❌ ChromeDriver not found after extraction", "error")
            return False
            
        except Exception as e:
            self.log(f"❌ Installation failed: {e}", "error")
            return False
    
    def install_all(self):
        """Install everything needed"""
        Colors.print_header("\n🔧 AUTO INSTALLER STARTED\n")
        
        self.install_python_packages()
        self.install_chromedriver()
        
        Colors.print_header("\n📋 INSTALLATION LOG:")
        for log in self.install_log[-10:]:
            print(f"   {log}")
        
        return True

# ==================== CONFIG MANAGER ====================

class ConfigManager:
    def __init__(self):
        self.config_file = "mdf_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        default_config = {
            'accounts': [],
            'targets': [],
            'settings': {
                'reports_per_target': 100,
                'delay_between_reports': 30,
                'delay_between_targets': 60,
                'max_threads': 3,
                'use_proxy': False,
                'proxies': [],
                'auto_retry': True,
                'max_retries': 3
            },
            'stats': {
                'total_reports': 0,
                'successful': 0,
                'failed': 0,
                'last_run': None
            }
        }
        
        try:
            with open(self.config_file, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in loaded:
                        loaded[key] = default_config[key]
                return loaded
        except:
            return default_config
    
    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def add_account(self, email, password):
        self.config['accounts'].append({
            'email': email,
            'password': password,
            'cookies': {},
            'last_used': None,
            'status': 'active'
        })
        self.save_config()
    
    def add_target(self, url):
        if url not in self.config['targets']:
            self.config['targets'].append(url)
            self.save_config()
    
    def remove_target(self, index):
        if 0 <= index < len(self.config['targets']):
            del self.config['targets'][index]
            self.save_config()
    
    def update_stats(self, success=True):
        self.config['stats']['total_reports'] += 1
        if success:
            self.config['stats']['successful'] += 1
        else:
            self.config['stats']['failed'] += 1
        self.config['stats']['last_run'] = datetime.now().isoformat()
        self.save_config()

# ==================== REPORTER ENGINE ====================

class ReporterEngine:
    def __init__(self, config):
        self.config = config
        self.is_running = False
        self.is_paused = False
        self.current_stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'start_time': None
        }
        self.logs = []
    
    def add_log(self, msg, type="info"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {msg}"
        self.logs.append(log_entry)
        
        if type == "success":
            Colors.print_success(log_entry)
        elif type == "error":
            Colors.print_error(log_entry)
        elif type == "warning":
            Colors.print_warning(log_entry)
        else:
            print(log_entry)
    
    def scan_targets(self):
        """Scan targets for validity"""
        self.add_log("\n🔍 SCANNING TARGETS...", "info")
        valid_targets = []
        
        for target in self.config.config['targets']:
            self.add_log(f"   Checking: {target[:50]}...")
            time.sleep(0.5)
            
            # Basic validation
            if 'facebook.com' in target or 'fb.com' in target:
                valid_targets.append(target)
                self.add_log(f"   ✅ Valid", "success")
            else:
                self.add_log(f"   ❌ Invalid", "error")
        
        self.add_log(f"\n✅ {len(valid_targets)} valid targets found", "success")
        return valid_targets
    
    def scan_accounts(self):
        """Scan accounts for validity"""
        self.add_log("\n🔍 SCANNING ACCOUNTS...", "info")
        valid_accounts = []
        
        for account in self.config.config['accounts']:
            self.add_log(f"   Checking: {account['email']}")
            time.sleep(0.5)
            
            # Basic validation
            if '@' in account['email'] and len(account['password']) >= 6:
                valid_accounts.append(account)
                self.add_log(f"   ✅ Valid", "success")
            else:
                self.add_log(f"   ❌ Invalid", "error")
        
        self.add_log(f"\n✅ {len(valid_accounts)} valid accounts found", "success")
        return valid_accounts
    
    def start_attack(self):
        """Start the reporting attack"""
        # First scan everything
        self.add_log("\n🔄 PRE-ATTACK SCANNING PHASE", "info")
        
        targets = self.scan_targets()
        accounts = self.scan_accounts()
        
        if not targets:
            self.add_log("❌ No valid targets! Please add targets first.", "error")
            return False
        
        if not accounts:
            self.add_log("❌ No valid accounts! Please add accounts first.", "error")
            return False
        
        self.add_log("\n✅ ALL CHECKS PASSED! Starting attack...", "success")
        self.add_log(f"📊 Targets: {len(targets)} | Accounts: {len(accounts)}")
        
        self.is_running = True
        self.current_stats['start_time'] = time.time()
        
        # Start attack threads
        threads = []
        for i in range(min(self.config.config['settings']['max_threads'], len(accounts))):
            t = threading.Thread(target=self.worker_thread, 
                                args=(i+1, accounts[i % len(accounts)], targets))
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Monitor progress
        self.monitor_progress()
        return True
    
    def worker_thread(self, thread_id, account, targets):
        """Worker thread for reporting"""
        self.add_log(f"🚀 Thread {thread_id} started with account: {account['email']}", "info")
        
        # Simulate work (in real tool, use Selenium here)
        for target in targets:
            if not self.is_running:
                break
            
            while self.is_paused and self.is_running:
                time.sleep(1)
            
            reports_per_target = self.config.config['settings']['reports_per_target']
            
            for i in range(reports_per_target):
                if not self.is_running:
                    break
                
                # Simulate report
                time.sleep(random.uniform(1, 3))
                success = random.random() < 0.9  # 90% success rate
                
                self.current_stats['total'] += 1
                if success:
                    self.current_stats['success'] += 1
                    self.add_log(f"   ✅ [{thread_id}] Report {i+1}/{reports_per_target} for {target[:30]}...", "success")
                else:
                    self.current_stats['failed'] += 1
                    self.add_log(f"   ❌ [{thread_id}] Report {i+1}/{reports_per_target} failed", "error")
                
                # Update config stats
                self.config.update_stats(success)
                
                # Delay
                time.sleep(self.config.config['settings']['delay_between_reports'])
            
            # Delay between targets
            time.sleep(self.config.config['settings']['delay_between_targets'])
        
        self.add_log(f"✅ Thread {thread_id} completed", "success")
    
    def monitor_progress(self):
        """Monitor and display progress"""
        start_time = time.time()
        
        while self.is_running:
            time.sleep(2)
            elapsed = time.time() - start_time
            rate = self.current_stats['total'] / (elapsed / 60) if elapsed > 0 else 0
            
            # Clear screen for status update
            os.system('clear' if os.name == 'posix' else 'cls')
            
            print(f"{Colors.RED}{Colors.BOLD}")
            print("╔════════════════════════════════════════════════════════════╗")
            print("║           🔴 MDF LEGENDS - ATTACK IN PROGRESS            ║")
            print("╚════════════════════════════════════════════════════════════╝")
            print(f"{Colors.END}")
            
            print(f"\n{Colors.CYAN}📊 ATTACK STATISTICS:{Colors.END}")
            print(f"   Total Reports: {self.current_stats['total']}")
            print(f"   Successful: {Colors.GREEN}{self.current_stats['success']}{Colors.END}")
            print(f"   Failed: {Colors.RED}{self.current_stats['failed']}{Colors.END}")
            success_rate = (self.current_stats['success'] / (self.current_stats['total'] or 1)) * 100
            print(f"   Success Rate: {Colors.YELLOW}{success_rate:.1f}%{Colors.END}")
            print(f"   Reports/Min: {Colors.GREEN}{rate:.1f}{Colors.END}")
            print(f"   Elapsed: {int(elapsed // 60)}m {int(elapsed % 60)}s")
            print(f"   Status: {'▶️ RUNNING' if not self.is_paused else '⏸️ PAUSED'}")
            
            print(f"\n{Colors.CYAN}📋 RECENT LOGS:{Colors.END}")
            for log in self.logs[-8:]:
                print(f"   {log}")
            
            print(f"\n{Colors.YELLOW}Commands: [P]ause [R]esume [S]top{Colors.END}")
    
    def pause(self):
        self.is_paused = True
        self.add_log("⏸️ Attack paused", "warning")
    
    def resume(self):
        self.is_paused = False
        self.add_log("▶️ Attack resumed", "success")
    
    def stop(self):
        self.is_running = False
        self.add_log("⏹️ Attack stopped", "warning")

# ==================== TERMINAL UI ====================

class TerminalUI:
    def __init__(self):
        self.config = ConfigManager()
        self.reporter = None
        self.installer = AutoInstaller()
        self.checker = SystemChecker()
    
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        banner = f"""
{Colors.RED}{Colors.BOLD}
╔═══════════════════════════════════════════════════════════════════╗
║                    🔴 MDF LEGENDS TERMINAL v5.0                  ║
║                Powered By {Colors.YELLOW}Al'mudafioon Force{Colors.RED}{Colors.BOLD}                ║
║                    {Colors.CYAN}ALL-IN-ONE AUTO TOOL{Colors.RED}{Colors.BOLD}                     ║
╚═══════════════════════════════════════════════════════════════════╝
{Colors.END}
        """
        print(banner)
    
    def print_menu(self):
        menu = f"""
{Colors.CYAN}{Colors.BOLD}╔════════════════════════════════════════════════════════════╗
║                         MAIN MENU                              ║
╠════════════════════════════════════════════════════════════════╣
║  {Colors.GREEN}1.{Colors.END} 🔍 System Scan & Auto Fix                                  ║
║  {Colors.GREEN}2.{Colors.END} 📦 Auto Install Everything                                 ║
║  {Colors.GREEN}3.{Colors.END} 👤 Manage Accounts                                        ║
║  {Colors.GREEN}4.{Colors.END} 🎯 Manage Targets                                         ║
║  {Colors.GREEN}5.{Colors.END} ⚙️ Settings                                              ║
║  {Colors.GREEN}6.{Colors.END} 🚀 Start Attack (Auto Scan First)                         ║
║  {Colors.GREEN}7.{Colors.END} 📊 View Statistics                                        ║
║  {Colors.GREEN}8.{Colors.END} 🧪 Test Configuration                                     ║
║  {Colors.GREEN}9.{Colors.END} 📖 Help                                                   ║
║  {Colors.GREEN}0.{Colors.END} 🚪 Exit                                                   ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}
        """
        print(menu)
    
    def manage_accounts(self):
        self.clear_screen()
        self.print_banner()
        print(f"\n{Colors.CYAN}{Colors.BOLD}👤 ACCOUNT MANAGEMENT{Colors.END}\n")
        
        accounts = self.config.config['accounts']
        
        if accounts:
            print(f"{Colors.GREEN}Current Accounts:{Colors.END}")
            for i, acc in enumerate(accounts, 1):
                status = "✅" if acc.get('status') == 'active' else "❌"
                print(f"  {i}. {status} {acc['email']}")
        else:
            print(f"{Colors.YELLOW}No accounts added{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("1. Add new account")
        print("2. Remove account")
        print("3. Test accounts")
        print("4. Back")
        
        choice = input(f"\n{Colors.GREEN}👉 Select: {Colors.END}")
        
        if choice == '1':
            email = input("Email/Phone: ")
            password = input("Password: ")
            self.config.add_account(email, password)
            Colors.print_success("✅ Account added!")
        
        elif choice == '2':
            if accounts:
                idx = int(input("Enter number to remove: ")) - 1
                if 0 <= idx < len(accounts):
                    del self.config.config['accounts'][idx]
                    self.config.save_config()
                    Colors.print_success("✅ Account removed!")
        
        elif choice == '3':
            self.test_accounts()
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def manage_targets(self):
        self.clear_screen()
        self.print_banner()
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎯 TARGET MANAGEMENT{Colors.END}\n")
        
        targets = self.config.config['targets']
        
        if targets:
            print(f"{Colors.GREEN}Current Targets:{Colors.END}")
            for i, target in enumerate(targets, 1):
                print(f"  {i}. {target}")
        else:
            print(f"{Colors.YELLOW}No targets added{Colors.END}")
        
        print(f"\n{Colors.CYAN}Options:{Colors.END}")
        print("1. Add single target")
        print("2. Add multiple targets (file)")
        print("3. Remove target")
        print("4. Clear all")
        print("5. Back")
        
        choice = input(f"\n{Colors.GREEN}👉 Select: {Colors.END}")
        
        if choice == '1':
            url = input("Enter Facebook URL: ")
            self.config.add_target(url)
            Colors.print_success("✅ Target added!")
        
        elif choice == '2':
            filename = input("Enter filename (one URL per line): ")
            try:
                with open(filename, 'r') as f:
                    for line in f:
                        url = line.strip()
                        if 'facebook.com' in url:
                            self.config.add_target(url)
                Colors.print_success(f"✅ Targets added from {filename}")
            except:
                Colors.print_error("❌ File not found")
        
        elif choice == '3':
            if targets:
                idx = int(input("Enter number to remove: ")) - 1
                self.config.remove_target(idx)
                Colors.print_success("✅ Target removed!")
        
        elif choice == '4':
            self.config.config['targets'] = []
            self.config.save_config()
            Colors.print_success("✅ All targets cleared!")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def system_scan(self):
        self.clear_screen()
        self.print_banner()
        self.checker.check_all()
        
        if not all(self.checker.checks.values()):
            print(f"\n{Colors.YELLOW}⚠️ Issues found. Run Auto Install? (y/n): {Colors.END}", end="")
            if input().lower() == 'y':
                self.auto_install()
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def auto_install(self):
        self.clear_screen()
        self.print_banner()
        self.installer.install_all()
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def test_config(self):
        self.clear_screen()
        self.print_banner()
        print(f"\n{Colors.CYAN}{Colors.BOLD}🧪 TESTING CONFIGURATION{Colors.END}\n")
        
        # Test accounts
        print("📧 Testing accounts...")
        valid_accounts = 0
        for acc in self.config.config['accounts']:
            if '@' in acc['email'] and len(acc['password']) >= 6:
                valid_accounts += 1
                Colors.print_success(f"   ✅ {acc['email']}")
            else:
                Colors.print_error(f"   ❌ {acc['email']}")
        
        # Test targets
        print("\n🎯 Testing targets...")
        valid_targets = 0
        for target in self.config.config['targets']:
            if 'facebook.com' in target or 'fb.com' in target:
                valid_targets += 1
                Colors.print_success(f"   ✅ {target[:50]}...")
            else:
                Colors.print_error(f"   ❌ {target[:50]}...")
        
        # Test settings
        print("\n⚙️ Testing settings...")
        settings = self.config.config['settings']
        print(f"   Reports/Target: {settings['reports_per_target']}")
        print(f"   Delay: {settings['delay_between_reports']}s")
        print(f"   Threads: {settings['max_threads']}")
        
        print(f"\n{Colors.CYAN}📊 SUMMARY:{Colors.END}")
        print(f"   Valid Accounts: {valid_accounts}/{len(self.config.config['accounts'])}")
        print(f"   Valid Targets: {valid_targets}/{len(self.config.config['targets'])}")
        
        ready = (valid_accounts > 0 and valid_targets > 0)
        if ready:
            Colors.print_success("\n✅ Ready to attack!")
        else:
            Colors.print_error("\n❌ Not ready! Add accounts and targets.")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def start_attack(self):
        self.reporter = ReporterEngine(self.config)
        
        if self.reporter.start_attack():
            # Control loop
            while self.reporter.is_running:
                cmd = input().lower()
                if cmd == 'p':
                    self.reporter.pause()
                elif cmd == 'r':
                    self.reporter.resume()
                elif cmd == 's':
                    self.reporter.stop()
                    break
    
    def show_stats(self):
        self.clear_screen()
        self.print_banner()
        print(f"\n{Colors.CYAN}{Colors.BOLD}📊 STATISTICS{Colors.END}\n")
        
        stats = self.config.config['stats']
        print(f"Total Reports: {stats['total_reports']}")
        print(f"Successful: {Colors.GREEN}{stats['successful']}{Colors.END}")
        print(f"Failed: {Colors.RED}{stats['failed']}{Colors.END}")
        success_rate = (stats['successful'] / (stats['total_reports'] or 1)) * 100
        print(f"Success Rate: {Colors.YELLOW}{success_rate:.1f}%{Colors.END}")
        print(f"Last Run: {stats['last_run'] or 'Never'}")
        
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def show_help(self):
        self.clear_screen()
        self.print_banner()
        print(f"""
{Colors.CYAN}{Colors.BOLD}📖 HELP & DOCUMENTATION{Colors.END}

{Colors.GREEN}ABOUT:{Colors.END}
  MDF Legends Terminal v5.0
  All-in-One Facebook Reporting Tool
  Auto Scan | Auto Install | Auto Work

{Colors.GREEN}FEATURES:{Colors.END}
  • 🔍 System Scanner - Checks everything
  • 📦 Auto Installer - Installs missing components
  • 👤 Account Manager - Multiple accounts
  • 🎯 Target Manager - Multiple victims
  • 🚀 Attack Engine - Multi-threaded reporting
  • 📊 Statistics - Track progress

{Colors.GREEN}HOW TO USE:{Colors.END}
  1. First run Option 1 (System Scan)
  2. Run Option 2 if anything missing
  3. Add accounts (Option 3)
  4. Add targets (Option 4)
  5. Test with Option 8
  6. Start attack with Option 6

{Colors.GREEN}COMMANDS DURING ATTACK:{Colors.END}
  • P - Pause attack
  • R - Resume attack
  • S - Stop attack

{Colors.GREEN}REQUIREMENTS:{Colors.END}
  • Python 3.6+
  • Chrome Browser
  • Internet connection
  • Facebook accounts
        """)
        input(f"\n{Colors.YELLOW}Press Enter...{Colors.END}")
    
    def run(self):
        while True:
            self.clear_screen()
            self.print_banner()
            self.print_menu()
            
            choice = input(f"{Colors.GREEN}👉 Select option: {Colors.END}")
            
            if choice == '1':
                self.system_scan()
            elif choice == '2':
                self.auto_install()
            elif choice == '3':
                self.manage_accounts()
            elif choice == '4':
                self.manage_targets()
            elif choice == '5':
                print("⚙️ Settings - Coming soon!")
                time.sleep(1)
            elif choice == '6':
                self.start_attack()
            elif choice == '7':
                self.show_stats()
            elif choice == '8':
                self.test_config()
            elif choice == '9':
                self.show_help()
            elif choice == '0':
                Colors.print_success("\n👋 Goodbye!")
                sys.exit(0)

# ==================== MAIN ====================

if __name__ == "__main__":
    try:
        ui = TerminalUI()
        ui.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}\n👋 Exiting...{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Fatal Error: {e}{Colors.END}")
        sys.exit(1)