import streamlit as st
import requests
import socket
from concurrent.futures import ThreadPoolExecutor

# ============ PAGE CONFIG ============
st.set_page_config(
    page_title="HexBytes Security Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============ CUSTOM CSS ============
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00ff88, #00aaff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: 800;
        margin-bottom: 0;
    }
    .sub-header { color: #888; font-size: 1.1em; margin-top: 0; }
    .warn-box {
        background: #ff990015;
        border-left: 4px solid #ff9900;
        padding: 14px 18px;
        border-radius: 8px;
        color: #ffbb55;
        margin: 20px 0;
    }
    .footer {
        text-align: center;
        color: #666;
        padding: 30px 0;
        margin-top: 40px;
        border-top: 1px solid #333;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

# ============ SIDEBAR ============
with st.sidebar:
    st.markdown("### 🛡️ HexBytes Toolkit")
    st.markdown("---")
    st.markdown("**Made by Kuldeep**")
    st.markdown("Ethical Hacking Suite")
    st.markdown("---")
    st.markdown("🔍 Subdomain Scan")
    st.markdown("🌐 Port Scan")
    st.markdown("🛡️ Security Headers")
    st.markdown("---")
    st.caption("v0.2.0 — Authorized use only")

# ============ HERO ============
st.markdown('<h1 class="main-header">🛡️ HexBytes Security Toolkit</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ethical Hacking & Penetration Testing Suite</p>', unsafe_allow_html=True)

st.markdown("""
<div class="warn-box">
⚠️ <strong>Authorized Use Only</strong> — Ye tool sirf company ke permitted targets pe use karna hai.
</div>
""", unsafe_allow_html=True)

# ============ HELPER FUNCTIONS ============
def get_subdomains(domain):
    subs = set()
    try:
        r = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=30)
        if r.status_code == 200:
            for entry in r.json():
                for name in entry.get("name_value", "").split("\n"):
                    name = name.strip().lower()
                    if name and "*" not in name and domain in name:
                        subs.add(name)
    except Exception as e:
        st.error(f"Error: {e}")
    return sorted(subs)

def check_alive(sub):
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{sub}", timeout=5, allow_redirects=True)
            return (sub, "LIVE", r.status_code)
        except:
            continue
    return (sub, "dead", "-")

def scan_port(host, port, timeout=1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((host, port)) == 0:
                try:
                    return (port, socket.getservbyport(port))
                except:
                    return (port, "unknown")
    except:
        pass
    return None

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection",
]

# ============ TABS ============
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Subdomain Scan", "🌐 Port Scan", "🛡️ Security Headers", "ℹ️ About"])

# ---------- TAB 1: SUBDOMAIN ----------
with tab1:
    st.subheader("🔍 Subdomain Enumeration")
    st.caption("crt.sh certificate transparency logs se subdomains discover karo")
    domain = st.text_input("Domain", "example.com", key="d1")
    check_live = st.checkbox("Live status check karo (slow but useful)", value=True)
    
    if st.button("🚀 Scan Subdomains", key="b1", type="primary"):
        if not domain:
            st.warning("Domain daalo")
        else:
            with st.spinner(f"Scanning {domain}..."):
                subs = get_subdomains(domain)
                if subs:
                    st.success(f"✅ {len(subs)} subdomains mile")
                    if check_live:
                        with st.spinner("Live status check..."):
                            with ThreadPoolExecutor(max_workers=20) as ex:
                                results = list(ex.map(check_alive, subs))
                        st.dataframe(results, use_container_width=True, 
                                     column_config={"0": "Subdomain", "1": "Status", "2": "HTTP"})
                    else:
                        st.dataframe(subs, use_container_width=True)
                else:
                    st.warning("Koi subdomain nahi mila")

# ---------- TAB 2: PORT SCAN ----------
with tab2:
    st.subheader("🌐 Port Scanner")
    st.caption("Common ports pe fast TCP connect scan")
    host = st.text_input("Host (domain or IP)", "example.com", key="h2")
    custom_ports = st.text_input("Custom ports (comma-separated, blank = common)", "", key="p2")
    
    if st.button("🚀 Scan Ports", key="b2", type="primary"):
        if not host:
            st.warning("Host daalo")
        else:
            if custom_ports:
                ports = [int(x.strip()) for x in custom_ports.split(",") if x.strip().isdigit()]
            else:
                ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 6379, 8080, 8443, 27017]
            
            with st.spinner(f"Scanning {len(ports)} ports on {host}..."):
                results = []
                with ThreadPoolExecutor(max_workers=100) as ex:
                    for r in ex.map(lambda p: scan_port(host, p), ports):
                        if r:
                            results.append(r)
                
                if results:
                    st.success(f"✅ {len(results)} open ports mile")
                    st.dataframe(results, use_container_width=True,
                                 column_config={"0": "Port", "1": "Service"})
                else:
                    st.warning("Koi open port nahi mila")

# ---------- TAB 3: HEADERS ----------
with tab3:
    st.subheader("🛡️ Security Headers Check")
    st.caption("OWASP recommended security headers check + score")
    url = st.text_input("URL", "https://example.com", key="u3")
    
    if st.button("🚀 Check Headers", key="b3", type="primary"):
        if not url:
            st.warning("URL daalo")
        else:
            if not url.startswith("http"):
                url = f"https://{url}"
            with st.spinner("Checking headers..."):
                try:
                    r = requests.get(url, timeout=10, allow_redirects=True)
                    present = []
                    missing = []
                    for h in SECURITY_HEADERS:
                        if h in r.headers:
                            present.append((h, r.headers[h]))
                        else:
                            missing.append(h)
                    
                    score = f"{len(present)}/{len(SECURITY_HEADERS)}"
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Status Code", r.status_code)
                    col2.metric("Score", score)
                    col3.metric("Missing", len(missing))
                    
                    st.markdown("### ✅ Present Headers")
                    if present:
                        st.dataframe(present, use_container_width=True, 
                                     column_config={"0": "Header", "1": "Value"})
                    else:
                        st.info("Koi header present nahi")
                    
                    st.markdown("### ❌ Missing Headers")
                    if missing:
                        for h in missing:
                            st.markdown(f"- `{h}`")
                    else:
                        st.success("Sab headers present! 🎉")
                except Exception as e:
                    st.error(f"Error: {e}")

# ---------- TAB 4: ABOUT ----------
with tab4:
    st.subheader("ℹ️ About HexBytes Security Toolkit")
    st.markdown("""
    **HexBytes Security Toolkit** ek internal penetration testing suite hai jo 
    ethical hackers aur security researchers ke liye banaya gaya hai.
    
    ### 🔧 Features
    - 🔍 **Subdomain Enumeration** — crt.sh based, live status check
    - 🌐 **Port Scanner** — multi-threaded TCP connect scan
    - 🛡️ **Security Headers** — OWASP recommended headers + score
    - 📄 **Reports** — HTML report generation (CLI)
    
    ### 👤 Author
    **Kuldeep** — Security Researcher / Ethical Hacker
    
    ### ⚖️ Disclaimer
    Ye tool sirf **authorized testing** ke liye hai. Company ke written permission 
    ke bina kisi bhi target pe scan mat karo.
    
    ### 🔗 Links
    - [GitHub Repository](https://github.com/kuldeepLinux/Hexbytes-security-toolkit)
    - [Landing Page](https://kuldeeplinux.github.io/Hexbytes-security-toolkit/)
    """)

# ============ FOOTER ============
st.markdown("""
<div class="footer">
    🛡️ HexBytes Security Toolkit — Made by <strong>Kuldeep</strong><br>
    © 2026 — Authorized Use Only
</div>
""", unsafe_allow_html=True)
