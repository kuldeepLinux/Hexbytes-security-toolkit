import streamlit as st
from modules.recon.subdomain import enumerate_subdomains
from modules.recon.portscan import scan_ports
from modules.webscan.headers import check_headers

st.set_page_config(page_title="HexBytes Toolkit", page_icon="🛡️", layout="wide")
st.title("🛡️ HexBytes Security Toolkit")
st.caption("Made by Kuldeep — Authorized use only")

tab1, tab2, tab3 = st.tabs(["🔍 Subdomain Scan", "🌐 Port Scan", "🛡️ Security Headers"])

with tab1:
    domain = st.text_input("Domain", "example.com", key="d")
    if st.button("Scan Subdomains", key="b1"):
        with st.spinner("Scanning..."):
            try:
                results = enumerate_subdomains(domain, check_live=True)
                live = [(s, "LIVE" if a else "dead", c) for s, a, c in results]
                st.dataframe(live, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

with tab2:
    host = st.text_input("Host", "example.com", key="h")
    ports = st.text_input("Ports (comma-separated, blank = common)", "", key="p")
    if st.button("Scan Port"):
        with st.spinner("Scanning..."):
            try:
                pl = [int(x.strip()) for x in ports.split(",")] if ports else None
                results = scan_ports(host, ports=pl)
                st.dataframe(results, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    url = st.text_input("URL", "https://example.com", key="u")
    if st.button("Check Headers", key="b3"):
        with st.spinner("Checking..."):
            try:
                result = check_headers(url)
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.metric("Score", result["score"])
                    st.write("**Present:**", [h for h, _ in result["present"]])
                    st.write("**Missing:**", result["missing"])
            except Exception as e:
                st.error(f"Error: {e}")
