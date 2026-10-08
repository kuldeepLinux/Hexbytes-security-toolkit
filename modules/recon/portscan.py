import socket
from concurrent.futures import ThreadPoolExecutor str, port: int
from core.utils import clean_domain

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def scan_port(host:, timeout: float = 1.0) -> tuple:
    """Scan a single port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = COMMON_PORTS.get(port, "unknown")
                return (port, True, service)
    except Exception:
        pass
    return (port, False, None)

def scan_ports(host: str, ports: list = None, threads: int = 100, timeout: float = 1.0) -> list:
    """Scan multiple ports on a host."""
    host = clean_domain(host)
    if ports is None:
        ports = list(COMMON_PORTS.keys())

    print(f"[*] Scanning {len(ports)} ports on {host}...")

    open_ports = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port, is_open, service in executor.map(lambda p: scan_port(host, p, timeout), ports):
            if is_open:
                open_ports.append((port, service))
                print(f"    [+] Port {port} OPEN ({service})")

    print(f"[+] Done: {len(open_ports)} open ports found")
    return open_ports
