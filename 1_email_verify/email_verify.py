#!/usr/bin/env python3
import re
import sys
import smtplib
import socket
from email.utils import parseaddr
from typing import List

try:
    import dns.resolver
except ImportError:
    print("Установите зависимость: pip install dnspython", file=sys.stderr)
    sys.exit(1)

EMAIL_RE = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
SMTP_TIMEOUT = 15
STATUS_VALID = "домен валиден"
STATUS_ABSENT = "домен отсутствует"
STATUS_NO_MX = "MX-записи отсутствуют или некорректны"


def is_valid_email(s: str) -> bool:
    s = (s or "").strip()
    return bool(s and EMAIL_RE.match(s))


def get_domain(email: str) -> str:
    _, addr = parseaddr(f"<{email}>")
    if "@" in addr:
        return addr.split("@", 1)[1].lower()
    return ""


def get_mx_hosts(domain: str):
    """
    Returns (list of hosts, error_type)
    error_type: None, 'nxdomain', 'no_mx', 'error'
    """
    try:
        answers = dns.resolver.resolve(domain, "MX")
        sorted_mx = sorted(answers, key=lambda r: r.preference)
        hosts = [str(r.exchange).rstrip(".") for r in sorted_mx]
        return hosts, None
    except dns.resolver.NXDOMAIN:
        return [], "nxdomain"
    except (dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        return [], "no_mx"
    except dns.exception.DNSException:
        return [], "error"


def smtp_verify(email: str, mx_host: str) -> str:
    host = str(mx_host).strip() if mx_host else ""
    if not host:
        return STATUS_ABSENT
    try:
        with smtplib.SMTP(timeout=SMTP_TIMEOUT) as smtp:
            smtp.set_debuglevel(0)
            smtp.connect(host, 25)
            smtp.ehlo()
            smtp.mail("verify@example.com")
            code, _ = smtp.rcpt(email)
            if code in (250, 251):
                return STATUS_VALID
            return STATUS_ABSENT
    except (smtplib.SMTPRecipientsRefused, smtplib.SMTPResponseException) as e:
        if hasattr(e, "smtp_code") and 400 <= getattr(e, "smtp_code", 0) < 500:
            return STATUS_ABSENT
        return STATUS_ABSENT
    except (socket.timeout, socket.error, smtplib.SMTPException, OSError):
        return STATUS_ABSENT


def check_email(email: str) -> str:
    email = (email or "").strip()
    if not email:
        return STATUS_NO_MX
    if not is_valid_email(email):
        return STATUS_NO_MX
    domain = get_domain(email)
    if not domain:
        return STATUS_NO_MX
    hosts, err = get_mx_hosts(domain)
    if err or not hosts:
        return STATUS_NO_MX
    return smtp_verify(email, hosts[0])


def load_emails_from_file(path: str) -> List[str]:
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python email_verify.py <email1> [email2 ...] | python email_verify.py --file <path.txt>")
        sys.exit(1)
    if sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("Usage: python email_verify.py --file <path.txt>")
            sys.exit(1)
        emails = load_emails_from_file(sys.argv[2])
    else:
        emails = [e.strip() for e in sys.argv[1:] if e.strip()]
    for addr in emails:
        status = check_email(addr)
        print(f"{addr}\t{status}")


if __name__ == "__main__":
    main()
