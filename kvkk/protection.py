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


def _mask_digits(value, keep_first, keep_last):
    # Değerdeki rakamları yıldızlar; baştan keep_first ve sondan keep_last rakam görünür kalır.
    # Rakam olmayan karakterler (boşluk, nokta, "TR") olduğu gibi bırakılır,
    # böylece maskelenmiş değer orijinal yazım biçimini korur.
    total_digits = len(digits_only(value))
    result = ""
    digit_index = 0
    for char in value:
        if char.isdigit():
            if digit_index < keep_first or digit_index >= total_digits - keep_last:
                result += char
            else:
                result += "*"
            digit_index += 1
        else:
            result += char
    return result


def mask(finding):
    # Bulgunun türüne göre uygun maskeleme kuralını uygular.
    if finding.kind == "PHONE":
        return _mask_phone(finding.value)
    if finding.kind == "EMAIL":
        return _mask_email(finding.value)
    if finding.kind == "TCKN":
        # 12345678950 -> 123******50
        return _mask_digits(finding.value, 3, 2)
    if finding.kind == "IBAN":
        # TR40 0006 1000 ... 4567 89 -> TR40 **** **** ... **67 89 (kontrol haneleri ve son 4 hane)
        return _mask_digits(finding.value, 2, 4)
    if finding.kind == "CREDIT_CARD":
        # PCI DSS'e uygun olarak sadece son 4 hane görünür: **** **** **** 1111
        return _mask_digits(finding.value, 0, 4)
    if finding.kind == "BIRTH_DATE":
        # 15.06.1990 -> **.**.1990 (genelleştirme: sadece yıl kalır)
        return _mask_digits(finding.value, 0, 4)
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
