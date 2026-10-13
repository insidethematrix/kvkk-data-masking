from datetime import datetime


def is_valid_tckn(tckn):
    # TC kimlik numarasının resmi kontrol algoritmasına uyup uymadığını kontrol eder.
    # Kurallar: 11 hane, sadece rakam, ilk hane 0 olamaz,
    # 10. ve 11. haneler ilk hanelerden hesaplanan kontrol haneleridir.
    if len(tckn) != 11 or not tckn.isdigit() or tckn[0] == "0":
        return False

    digits = [int(char) for char in tckn]
    even_index_sum , odd_index_sum = 0 , 0

    for i in range(0 , 9):
        if i % 2 == 0:
            even_index_sum+=digits[i]
        else:
            odd_index_sum+=digits[i]
    tenth_digit = (7 * even_index_sum - odd_index_sum) % 10
    eleventh_digit = sum(digits[:10]) % 10

    return digits[9] == tenth_digit and digits[10] == eleventh_digit


def is_valid_luhn(number):
    # Kredi kartı numarasının Luhn algoritmasına uyup uymadığını kontrol eder.
    # Boşluk ve tireler yok sayılır; 13-19 hane kabul edilir.
    digits = number.replace(" ", "").replace("-", "")
    if not digits.isdigit() or not (13 <= len(digits) <= 19):
        return False

    total = 0
    # Sağdan sola gidiyoruz; sağdan 2., 4., 6. ... haneler iki katına çıkar.
    for position, char in enumerate(reversed(digits)):
        digit = int(char)
        if position % 2 == 1:
            digit = digit * 2
            if digit > 9:
                digit = digit - 9
        total += digit
    return total % 10 == 0


def is_valid_iban(iban):
    # Türk IBAN'ının uzunluğunu ve mod-97 kontrolünü yapar.
    # Boşluklar silinir, küçük harf büyük harfe çevrilir.
    iban = iban.replace(" ", "").upper()
    if len(iban) != 26 or not iban.startswith("TR") or not iban[2:].isdigit():
        return False

    # İlk 4 karakter (TR + kontrol haneleri) sona taşınır.
    rearranged = iban[4:] + iban[:4]

    # Harfler sayıya çevrilir: A=10, B=11, ..., Z=35 (T=29, R=27).
    numeric_text = ""
    for char in rearranged:
        if char.isalpha():
            numeric_text += str(ord(char) - ord("A") + 10)
        else:
            numeric_text += char

    # Python int'i çok büyük sayıları sorunsuz taşır.
    return int(numeric_text) % 97 == 1


def is_valid_date(date_text):
    # "gg.aa.yyyy", "gg/aa/yyyy" veya "gg-aa-yyyy" biçimindeki tarihin
    # takvimde gerçekten var olup olmadığını kontrol eder (31.02 gibi tarihler elenir).
    date_text = date_text.replace("/", ".").replace("-", ".")
    try:
        datetime.strptime(date_text, "%d.%m.%Y")
        return True
    except ValueError:
        return False
