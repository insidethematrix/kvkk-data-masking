from kvkk.validation import is_valid_date, is_valid_iban, is_valid_luhn, is_valid_tckn

# Not: Buradaki numaralar elle hesaplanmış, hiçbir kişiye ait olmayan örneklerdir.


# ---------- TC Kimlik ----------

def test_valid_tckn():
    assert is_valid_tckn("12345678950") is True
    assert is_valid_tckn("10000000146") is True
    # Ara değer negatif çıkıyor: 7*1 - 36 = -29, mod 10 = 1
    assert is_valid_tckn("19090909018") is True


def test_tckn_with_wrong_check_digit():
    assert is_valid_tckn("12345678951") is False   # 11. hane yanlış
    assert is_valid_tckn("12345678940") is False   # 10. hane yanlış


def test_malformed_tckn():
    assert is_valid_tckn("02345678950") is False   # 0 ile başlıyor
    assert is_valid_tckn("1234567895") is False    # 10 hane
    assert is_valid_tckn("1234567895a") is False   # harf içeriyor


# ---------- Luhn ----------

def test_valid_card():
    assert is_valid_luhn("4111 1111 1111 1111") is True
    assert is_valid_luhn("4111-1111-1111-1111") is True


def test_invalid_card():
    assert is_valid_luhn("4111 1111 1111 1112") is False  # son hane değişti
    assert is_valid_luhn("1234") is False                 # çok kısa
    assert is_valid_luhn("4111 1111 abcd 1111") is False


# ---------- IBAN ----------

def test_valid_iban():
    assert is_valid_iban("TR400006100000000123456789") is True
    assert is_valid_iban("TR40 0006 1000 0000 0123 4567 89") is True
    assert is_valid_iban("tr400006100000000123456789") is True


def test_invalid_iban():
    assert is_valid_iban("TR410006100000000123456789") is False  # kontrol hanesi
    assert is_valid_iban("TR40000610000000012345678") is False   # 25 karakter
    assert is_valid_iban("DE400006100000000123456789") is False  # TR değil


# ---------- Tarih ----------

def test_date_validation():
    assert is_valid_date("15.06.1990") is True
    assert is_valid_date("15/06/1990") is True
    assert is_valid_date("29.02.2000") is True    # artık yıl
    assert is_valid_date("31.02.1990") is False
    assert is_valid_date("29.02.1999") is False
