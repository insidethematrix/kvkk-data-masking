import re


def digits_only(value):
    # Bir metindeki rakam dışı tüm karakterleri (boşluk, tire, +, parantez) atar.
    return re.sub(r"\D", "", value)


def _mask_phone(value):
    # 0532 123 45 67 -> 532***4567 (ilk 3 ve son 4 hane görünür kalır).
    digits = digits_only(value)[-10:]
    return digits[:3] + "***" + digits[-4:]


def _mask_email(value):
    # ahmet@ornek.com -> a***@ornek.com (kullanıcı adının ilk harfi kalır).
    local_part, domain = value.split("@", 1)
    return local_part[0] + "***@" + domain


def mask(finding):
    # Bulgunun türüne göre uygun maskeleme fonksiyonunu çağırır.
    if finding.kind == "PHONE":
        return _mask_phone(finding.value)
    if finding.kind == "EMAIL":
        return _mask_email(finding.value)
    # Henüz özel kuralı olmayan türler tamamen yıldızlanır.
    return "*" * len(finding.value)


def protect_text(text, findings, method="mask"):
    # Metindeki tüm bulguları seçilen yönteme göre değiştirir.
    # Değiştirmeyi sondan başa yapıyoruz: böylece öndeki bulguların
    # start/end indeksleri, arkadaki değişikliklerden etkilenmez.
    if method != "mask":
        raise ValueError("Unknown protection method: " + method)

    result = text
    for finding in sorted(findings, key=lambda f: f.start, reverse=True):
        replacement = mask(finding)
        result = result[:finding.start] + replacement + result[finding.end:]
    return result
