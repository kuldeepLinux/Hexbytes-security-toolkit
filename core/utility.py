import re
from urllib.parse import urlparse

def clean_domain(domain: str) -> str:
    """Strip protocol, path, www from input."""
    domain = domain.strip().lower()
    if "://" in domain:
        domain = urlparse(domain).netloc
    domain = re.sub(r"^www\.", "", domain)
    return domain.split("/")[0]

def is_valid_domain(domain: str) -> bool:
    pattern = r"^(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z0-9-]{1,63})+$"
    return bool(re.match(pattern, domain))
