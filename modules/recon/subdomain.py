import requests
from concurrent.futures import ThreadPoolExecutor
from core.logger import log
from core.utils import clean_domain

CRT_SH_URL = "https://crt.sh/?q=%25.{}&output=json"

def fetch_crtsh(domain: str) -> set:
    """Fetch subdomains from crt.sh certificate transparency logs."""
    subs = set()
    try:
        r = requests.get(CRT_SH_URL.format(domain), timeout=30)
        if r.status_code == 200:
            for entry in r.json():
                for name in entry.get("name_value", "").split("\n"):
                    name = name.strip().lower()
                    if name and "*" not in name and domain in name:
                        subs.add(name)
        log.info(f"crt.sh: {len(subs)} subdomains found")
    except Exception as e:
        log.error(f"crt.sh failed: {e}")
    return subs

def check_alive(subdomain: str, timeout: int = 5) -> tuple:
    """Check if subdomain resolves via HTTP."""
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{subdomain}", timeout=timeout, allow_redirects=True)
            return (subdomain, True, r.status_code)
        except Exception:
            continue
    return (subdomain, False, None)

def enumerate_subdomains(domain: str, check_live: bool = True, threads: int = 20) -> list:
    domain = clean_domain(domain)
    log.info(f"Starting subdomain enumeration for: {domain}")

    subs = fetch_crtsh(domain)

    results = []
    if check_live and subs:
        log.info(f"Checking {len(subs)} subdomains for live status...")
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for result in executor.map(check_alive, subs):
                results.append(result)
                status = "LIVE" if result[1] else "dead"
                log.debug(f"{result[0]} -> {status}")
    else:
        results = [(s, None, None) for s in subs]

    live_count = sum(1 for r in results if r[1])
    log.success(f"Done: {len(results)} total, {live_count} live")
    return results
