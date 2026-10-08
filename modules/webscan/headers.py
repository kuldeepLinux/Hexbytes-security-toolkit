import requests
from core.utils import clean_domain

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
    "Permissions-Policy",
    "X-XSS-Protection",
]

def check_headers(url: str, timeout: int = 10) -> dict:
    """Check security headers of a URL."""
    url = clean_domain(url)
    if not url.startswith("http"):
        url = f"https://{url}"

    print(f"[*] Checking security headers for: {url}")

    try:
        r = requests.get(url, timeout=timeout, allow_redirects=True)
    except Exception as e:
        print(f"[-] Failed to connect: {e}")
        return {"error": str(e)}

    present = []
    missing = []

    for header in SECURITY_HEADERS:
        if header in r.headers:
            present.append((header, r.headers[header]))
            print(f"    [+] {header}: present")
        else:
            missing.append(header)
            print(f"    [-] {header}: MISSING")

    return {
        "url": url,
        "status_code": r.status_code,
        "present": present,
        "missing": missing,
        "score": f"{len(present)}/{len(SECURITY_HEADERS)}",
    }
