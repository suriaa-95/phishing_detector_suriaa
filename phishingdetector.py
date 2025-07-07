import tkinter as tk
from tkinter import messagebox
import pandas as pd
import re

# Rule-based phishing detection function
def check_phishing(url):
    score = 0

    # Rule 1: IP address usage
    if re.search(r'https?://(?:\d{1,3}\.){3}\d{1,3}', url):
        score += 2

    # Rule 2: Suspicious keywords
    if any(keyword in url.lower() for keyword in ['login', 'verify', 'secure', 'bank']):
        score += 1

    # Rule 3: Too many dots
    if url.count('.') > 3:
        score += 1

    # Rule 4: Missing HTTPS
    if not url.startswith('https://'):
        score += 1

    return 'Phishing' if score >= 3 else 'Legit'

# Initialize log DataFrame
log_df = pd.DataFrame(columns=['Entered URL', 'Detection Result'])

# Callback for the Analyze button
def analyze_url():
    url = entry.get()
    if not url:
        messagebox.showwarning("Missing Input", "Please enter a URL to analyze.")
        return
    result = check_phishing(url)
    messagebox.showinfo("Detection Result", f"The URL is likely: {result}")

    # Log to DataFrame
    global log_df
    log_df.loc[len(log_df)] = [url, result]

# Callback to export log to CSV
def export_log():
    if log_df.empty:
        messagebox.showinfo("No Data", "No URL checks to export.")
    else:
        log_df.to_csv("url_detection_log.csv", index=False)
        messagebox.showinfo("Export Complete", "Results saved to 'url_detection_log.csv'.")

# GUI layout
window = tk.Tk()
window.title("Phishing URL Detector")
window.geometry("470x220")
window.configure(bg="#f0f4f7")

# Widgets
tk.Label(window, text="🔗 Enter a URL to check:", font=("Arial", 12), bg="#f0f4f7").pack(pady=10)
entry = tk.Entry(window, width=55, font=("Courier", 11))
entry.pack(pady=5)

tk.Button(window, text="Analyze", command=analyze_url,
          bg="#4CAF50", fg="white", font=("Arial", 11)).pack(pady=8)

tk.Button(window, text="Export Log", command=export_log,
          bg="#2196F3", fg="white", font=("Arial", 10)).pack(pady=5)

# Start the GUI loop
window.mainloop()
