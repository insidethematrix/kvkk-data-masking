import re
from dataclasses import dataclass


@dataclass
class Finding:
    # Metinde bulunan tek bir kişisel veriyi temsil eder.
    kind: str     # Veri türü: "EMAIL", "PHONE", ...
    value: str    # Metinde geçtiği haliyle değer
    start: int    # Metindeki başlangıç indeksi
    end: int      # Metindeki bitiş indeksi (dahil değil, Python dilimleme mantığı)


# E-posta: kullanıcı adı @ alan adı . uzantı
EMAIL_PATTERN = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# Türkiye cep telefonu: isteğe bağlı +90 / 0090 / 0 öneki, ardından 5XX XXX XX XX.
# Gruplar arasında boşluk veya tire olabilir. (?<![\d+]) ve (?!\d) sayesinde
# daha uzun bir sayının (örneğin 11 haneli TC) ortasından parça yakalanmaz.
PHONE_PATTERN = re.compile(
    r"(?<![\d+])"
    r"(?:(?:\+90|0090|0)[\s-]?)?"
    r"\(?5\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}"
    r"(?!\d)"
)


def _find_with_pattern(text, pattern, kind):
    # Verilen regex desenine uyan tüm parçaları Finding listesi olarak döndürür.
    findings = []
    for match in pattern.finditer(text):
        findings.append(Finding(kind, match.group(), match.start(), match.end()))
    return findings


def find_emails(text):
    # Metindeki e-posta adreslerini bulur.
    return _find_with_pattern(text, EMAIL_PATTERN, "EMAIL")


def find_phones(text):
    # Metindeki cep telefonu numaralarını bulur.
    return _find_with_pattern(text, PHONE_PATTERN, "PHONE")


def find_all(text):
    # Tüm veri türlerini arar ve bulguları metindeki sıraya göre döndürür.
    findings = find_emails(text) + find_phones(text)
    findings.sort(key=lambda f: f.start)
    return findings
