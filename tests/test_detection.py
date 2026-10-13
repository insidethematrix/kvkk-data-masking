from kvkk.detection import find_all, find_emails, find_phones


# ---------- E-posta ----------

def test_email_is_found():
    findings = find_emails("İletişim: deneme.kisi@ornek.com adresine yazın.")
    assert len(findings) == 1
    assert findings[0].value == "deneme.kisi@ornek.com"


def test_text_without_email():
    assert find_emails("Bu metinde @ işareti var ama adres yok.") == []


# ---------- Telefon ----------

def test_phone_format_variations():
    samples = [
        "0532 123 45 67",
        "05321234567",
        "+90 532 123 45 67",
        "+905321234567",
        "0090 532 123 45 67",
        "532-123-45-67",
    ]
    for sample in samples:
        findings = find_phones("Tel: " + sample + " arayın")
        assert len(findings) == 1, sample
        assert findings[0].value == sample


def test_non_phone_numbers_are_ignored():
    # 5 ile başlamayan 10 hane ve 11 haneli bir sayının içi telefon sayılmamalı
    assert find_phones("Sipariş no: 1234567890") == []
    assert find_phones("Numara: 53212345678") == []


# ---------- Birlikte ----------

def test_find_all_returns_sorted():
    text = "Tel 0532 123 45 67, posta a@ornek.com"
    findings = find_all(text)
    assert [f.kind for f in findings] == ["PHONE", "EMAIL"]
    # Konumlar metindeki gerçek değeri göstermeli
    for f in findings:
        assert text[f.start:f.end] == f.value
