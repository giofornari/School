import os
import sys
import time

banner = """


"""
print(banner)
dict = ["pyautogui", "pynput", "keyboard", "mouse", "pillow", "numpy"]
print("Starting setup.py...")
for pkg in dict:
    os.system("pip install {pkg}")
    print(f"Installed {pkg}")

print("All packages installed successfully.")
