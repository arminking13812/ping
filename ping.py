import requests
import socket
import time
import re

def is_valid_url(url):
    # Simple regex to validate URL
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# دریافت آدرس سایت از کاربر
s = input("Enter Site Address: ")

if not is_valid_url(s):
    print("Invalid URL format. Please enter a valid URL.")
else:
    # تلاش برای گرفتن پاسخ از سایت
    try:
        start_time = time.time()
        response = requests.get(s, timeout=10, headers={'User -Agent': 'Mozilla/5.0'})
        response_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"Connection Successful! Status: OK!")
            print(f"Response Time: {response_time:.2f} seconds")
            
            # گرفتن IP سایت
            domain = s.replace('https://', '').replace('http://', '').split('/')[0]
            ip = socket.gethostbyname(domain)
            print(f"IP Address of {s}: {ip}")
        else:
            print(f"Failed to connect to {s}. Status Code: {response.status_code}")
    except requests.exceptions.Timeout:
        print("Error: The request timed out.")
    except requests.exceptions.TooManyRedirects:
        print("Error: Too many redirects.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except socket.gaierror:
        print("Error: Could not resolve the hostname.")