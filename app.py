
import streamlit as st
from urllib.parse import urlparse
import ipaddress
import pickle
from pathlib import Path

st.set_page_config(
    page_title="PhishGuard",
    page_icon="🛡️",
    layout="centered"
)

# Dashboard styling
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #f1f5f9;
}
h1 {
    color: #38bdf8 !important;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 17px;
}
div.stButton > button {
    background-color: #0284c7;
    color: white;
    width: 100%;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Load the trained model
MODEL_PATH = Path(__file__).with_name("phishguard_model.pkl")


@st.cache_resource
def load_model():
    with open(MODEL_PATH, "rb") as file:
        return pickle.load(file)


try:
    vectorizer, model = load_model()
    model_loaded = True
except (FileNotFoundError, EOFError, pickle.UnpicklingError):
    model_loaded = False

# Store history for this session
if "scan_history" not in st.session_state:
    st.session_state.scan_history = []

st.title("🛡️ PhishGuard")
st.markdown(
    '<p class="subtitle">Smart URL Security Scanner</p>',
    unsafe_allow_html=True
)

st.divider()

if model_loaded:
    st.success("✅ Machine-learning model loaded")
else:
    st.error(
        "Model file not found or could not be loaded. "
        "Make sure phishguard_model.pkl is in the project folder."
    )

st.info(
    "Check a link for common phishing warning signs. "
    "This educational prototype uses simple rules and a "
    "machine-learning model trained on illustrative examples."
)


def check_url(url):
    reasons = []
    clean_url = url.strip()

    if not clean_url:
        return True, ["Please enter a URL."], None

    # Add a default scheme when omitted
    if "://" not in clean_url:
        clean_url = "https://" + clean_url

    try:
        parsed = urlparse(clean_url)
        hostname = parsed.hostname

        if parsed.scheme not in ("http", "https"):
            reasons.append("Unusual URL protocol.")

        if not hostname:
            return True, ["Invalid hostname."], None

        if parsed.username or parsed.password:
            reasons.append("URL contains embedded login information.")

        try:
            ipaddress.ip_address(hostname)
            reasons.append(
                "Uses an IP address instead of a domain name."
            )
        except ValueError:
            pass

        if hostname.startswith("xn--") or ".xn--" in hostname:
            reasons.append("Contains an internationalized hostname.")

        if len(clean_url) > 100:
            reasons.append("URL is unusually long.")

        if "@" in clean_url:
            reasons.append("Contains an @ symbol.")

        if hostname.count(".") >= 4:
            reasons.append("Contains many subdomains.")

        suspicious_words = [
            "login", "verify", "account", "update",
            "secure", "password", "banking", "free",
            "gift", "wallet"
        ]

        found_words = [
            word for word in suspicious_words
            if word in clean_url.lower()
        ]

        if found_words:
            reasons.append(
                "Potentially suspicious keywords: "
                + ", ".join(found_words)
            )

        if parsed.scheme == "http":
            reasons.append("Uses HTTP instead of HTTPS.")

    except ValueError:
        reasons.append("Could not parse this URL.")

    # Get machine-learning prediction
    prediction = None

    if model_loaded:
        features = vectorizer.transform([clean_url])
        prediction = int(model.predict(features)[0])

    return bool(reasons), reasons, prediction


st.subheader("🔍 Scan a URL")

url = st.text_input(
    "Website link",
    placeholder="https://example.com"
)

if st.button("🛡️ Scan URL", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL before scanning.")
    else:
        suspicious, reasons, prediction = check_url(url)

        flagged = suspicious or prediction == 1

        result = (
            "Warning signs detected"
            if flagged
            else "No obvious warning signs detected"
        )

        if prediction is None:
            model_result = "Model unavailable"
        elif prediction == 1:
            model_result = "Model flagged this URL"
        else:
            model_result = "Model did not flag this URL"

        st.session_state.scan_history.insert(
            0,
            {
                "url": url.strip(),
                "result": result,
                "reasons": reasons,
                "model_result": model_result
            }
        )

        st.session_state.last_scan = {
            "url": url.strip(),
            "flagged": flagged,
            "reasons": reasons,
            "model_result": model_result
        }

# Display most recent scan
if "last_scan" in st.session_state:
    scan = st.session_state.last_scan

    st.divider()
    st.subheader("📊 Scan Results")
    st.write("**Scanned URL:**", scan["url"])
    st.write("**Machine-learning result:**", scan["model_result"])

    if scan["flagged"]:
        st.error("⚠️ Warning signs detected")

        if scan["reasons"]:
            for reason in scan["reasons"]:
                st.write("- ", reason)
        else:
            st.write(
                "The model flagged this URL based on its learned patterns."
            )

        st.warning(
            "Verify the website independently before sharing "
            "passwords or personal information."
        )
    else:
        st.success("No obvious warning signs detected.")
        st.info(
            "This result does not prove the website is safe. "
            "The model uses a very small illustrative dataset."
        )

st.divider()

# Scan history
st.subheader("🕘 Scan History")

if st.session_state.scan_history:
    for index, item in enumerate(
        st.session_state.scan_history, start=1
    ):
        with st.expander(f"{index}. {item['url']}"):
            st.write("**Result:**", item["result"])
            st.write("**Model:**", item["model_result"])

            for reason in item["reasons"]:
                st.write("- ", reason)

    if st.button("🗑️ Clear History"):
        st.session_state.scan_history = []
        st.session_state.pop("last_scan", None)
        st.rerun()
else:
    st.caption("No URLs scanned yet. Your scan history appears here.")

st.divider()

st.subheader("🔐 Security Tips")
st.markdown("""
- Check the spelling of the website domain.
- Be careful with unexpected login or payment links.
- HTTPS alone does not guarantee a website is trustworthy.
- Never share passwords or OTPs with suspicious websites.
""")

st.caption(
    "PhishGuard | Educational cybersecurity prototype | "
    "Not a guarantee of website safety."
)
