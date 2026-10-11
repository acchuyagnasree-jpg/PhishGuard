# 🛡️ PhishGuard — Phishing URL Detection System

PhishGuard is a Python-based cybersecurity project that analyzes website URLs for potential phishing warning signs. It combines rule-based URL checks with a machine-learning model through an interactive Streamlit dashboard.

## Features

- Scan website URLs for suspicious patterns.
- Detect warning signs such as suspicious keywords, unusually long URLs, and IP-based hosts.
- Display machine-learning predictions.
- View scan history during the current session.
- Learn basic website security practices through the dashboard.

## Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas

## How to Run

1. Install Python.
2. Install the required packages.
3. Open a terminal in the project directory.
4. Run:

   `python -m streamlit run app.py`

5. Open the local address shown in the terminal.

## Project Status

Educational prototype.

## Limitations

The model has not been validated sufficiently for real-world phishing detection. A warning does not prove a URL is malicious, and a URL without warnings is not guaranteed to be safe. Do not rely on this application alone for security decisions.

## Future Improvements

- Train and evaluate the model using a verified, labeled dataset.
- Add model evaluation metrics.
- Improve phishing detection and testing.

## Author

**Acchu Yagna Sree**

GitHub: https://github.com/acchuyagnasree-jpg