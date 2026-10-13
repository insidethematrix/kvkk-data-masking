"""Algoritmaya uygun ama hiçbir gerçek kişiye bağlı olmayan sahte kişisel veri üretir.

Çalıştırma (proje kök klasöründen):
    python -m scripts.generate_fake_data

Not: Bu modül kontrol hanelerini kvkk/validation.py'yi KULLANMADAN, kendi başına hesaplar.
Böylece testlerde üretici ile doğrulayıcı birbirini bağımsız olarak kontrol etmiş olur.
"""

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

FIRST_NAMES = ["Ahmet", "Ayşe", "Mehmet", "Fatma", "Mustafa", "Zeynep", "Emre", "Elif",
               "Can", "Merve", "Burak", "Selin", "Oğuz", "Gülşen", "İsmail", "Şule"]
LAST_NAMES = ["Yılmaz", "Kaya", "Demir", "Şahin", "Çelik", "Yıldız", "Aydın", "Öztürk",
              "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Koç", "Kurt", "Özdemir"]

# RFC 2606 ile test amaçlı ayrılmış alan adları; gerçek bir posta kutusuna denk gelmez.
EMAIL_DOMAINS = ["example.com", "example.org", "example.net"]

# Türkiye'deki cep telefonu operatör ön ekleri (5XX'in ilk iki hanesi).
PHONE_PREFIXES = ["50", "53", "54", "55"]

# Banka kodu 5 hanedir; burada rastgele seçilecek birkaç örnek kod kullanılıyor.
BANK_CODES = ["00010", "00012", "00046", "00062", "00064", "00111"]

SAMPLE_DATA_DIR = Path(__file__).resolve().parent.parent / "sample_data"


def random_digits(count):
    # İstenen uzunlukta rastgele rakamlardan oluşan bir metin üretir.
    return "".join(str(random.randint(0, 9)) for _ in range(count))


def fake_tckn():
    # TC kimlik algoritmasına uyan sahte bir numara üretir.
    # İlk 9 hane rastgele seçilir (ilk hane 0 olamaz), son 2 hane hesaplanır.
    digits = [random.randint(1, 9)] + [random.randint(0, 9) for _ in range(8)]
    odd_positions_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8]
    even_positions_sum = digits[1] + digits[3] + digits[5] + digits[7]
    digits.append((odd_positions_sum * 7 - even_positions_sum) % 10)
    digits.append(sum(digits) % 10)
    return "".join(str(d) for d in digits)


def fake_iban(spaced=False):
    # mod-97 kontrolünden geçen sahte bir TR IBAN üretir.
    # Yapı: TR + 2 kontrol hanesi + 5 banka kodu + 1 rezerv (0) + 16 hesap no.
    bban = random.choice(BANK_CODES) + "0" + random_digits(16)
    # Kontrol haneleri "00" kabul edilip hesaplanır: TR -> 2927, sonra 98 - kalan.
    remainder = int(bban + "2927" + "00") % 97
    check_digits = str(98 - remainder).zfill(2)
    iban = "TR" + check_digits + bban
    if spaced:
        # 4'erli gruplar: TR40 0006 1000 ...
        iban = " ".join(iban[i:i + 4] for i in range(0, len(iban), 4))
    return iban


def luhn_check_digit(partial_number):
    # Luhn kontrol hanesi olmadan verilen numaraya (ör. 15 hane) eklenecek
    # son haneyi (0-9) hesaplar; sonuç eklendiğinde numara Luhn testinden geçer.
    # Kontrol hanesi henüz yok, bu yüzden sağdan 1., 3., 5. ... haneler ikiye katlanır.
    whole_sum = 0
    for index, value in enumerate(reversed(partial_number)):
        if index % 2 == 0:
            new_value = int(value) * 2
            if new_value > 9:
                new_value -= 9
            whole_sum += new_value
        else:
            whole_sum += int(value)

    # Toplamı 10'un katına tamamlayan rakam kontrol hanesidir.
    for i in range(0 , 10):
        if (whole_sum + i) % 10 == 0:
            return i


def fake_card(spaced=True):
    # Luhn algoritmasına uyan sahte bir 16 haneli kart numarası üretir.
    # "4" ile başlar (Visa biçimi); 15 hane belirlenir, 16. hane Luhn'a göre hesaplanır.
    partial = "4" + random_digits(14)
    number = partial + str(luhn_check_digit(partial))
    if spaced:
        number = " ".join(number[i:i + 4] for i in range(0, 16, 4))
    return number


def format_phone(ten_digits, style):
    # 10 haneli numarayı (5321234567) farklı yazım biçimlerinden birine dönüştürür.
    a, b, c, d = ten_digits[:3], ten_digits[3:6], ten_digits[6:8], ten_digits[8:]
    if style == "spaced":
        return f"0{a} {b} {c} {d}"
    if style == "international":
        return f"+90 {a} {b} {c} {d}"
    if style == "dashed":
        return f"{a}-{b}-{c}-{d}"
    return "0" + ten_digits  # "plain": 05321234567


def fake_phone_digits():
    # Ön eki olmayan, 5 ile başlayan 10 haneli sahte cep numarası üretir.
    return random.choice(PHONE_PREFIXES) + random_digits(8)


def to_ascii(text):
    # E-posta adresinde kullanmak için Türkçe karakterleri ASCII karşılıklarına çevirir.
    table = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return text.translate(table)


def fake_email(first_name, last_name):
    # Ad ve soyaddan test alan adına sahip bir e-posta üretir: ahmet.yilmaz@example.com
    local_part = to_ascii(first_name).lower() + "." + to_ascii(last_name).lower()
    return local_part + "@" + random.choice(EMAIL_DOMAINS)


def fake_birth_date():
    # 1950-2005 arasında rastgele bir doğum tarihini gg.aa.yyyy biçiminde üretir.
    start = date(1950, 1, 1)
    end = date(2005, 12, 31)
    day_offset = random.randint(0, (end - start).days)
    return (start + timedelta(days=day_offset)).strftime("%d.%m.%Y")


def fake_person():
    # Tüm alanları tutarlı tek bir sahte kişi kaydı üretir (sözlük olarak).
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return {
        "full_name": first_name + " " + last_name,
        "tckn": fake_tckn(),
        "phone": format_phone(fake_phone_digits(), "spaced"),
        "email": fake_email(first_name, last_name),
        "iban": fake_iban(spaced=True),
        "credit_card": fake_card(),
        "birth_date": fake_birth_date(),
    }


def build_sample_text(person):
    # Uygulamaya yapıştırılıp denenebilecek örnek bir Türkçe metin oluşturur.
    # Aynı telefon bilerek iki farklı biçimde geçer (takma ad tutarlılığını denemek için),
    # ayrıca yanlış pozitif denemesi için geçersiz bir TC ve geçersiz bir tarih içerir.
    phone_digits = person["phone"].replace(" ", "")[1:]
    return (
        f"Sayın {person['full_name']},\n"
        f"{person['birth_date']} doğumlu, {person['tckn']} TC kimlik numaralı müşterimizin "
        f"başvurusu alınmıştır. İletişim: {person['phone']} / {person['email']}.\n"
        f"İade, {person['iban']} numaralı hesaba yapılacaktır. "
        f"Ödeme {person['credit_card']} numaralı kart ile alınmıştır.\n"
        f"Müşteri diyabet hastası olduğunu ve sendika üyesi olduğunu belirtmiştir.\n"
        f"Acil durumda {format_phone(phone_digits, 'international')} numarasından ulaşılabilir.\n"
        f"Sipariş no: 12345678951, fatura tarihi: 31.02.2024."
    )


def build_sample_table(row_count):
    # CSV/Excel denemeleri için sahte kişilerden oluşan bir pandas DataFrame üretir.
    # Son satır ilk satırın kopyasıdır: aynı kişinin farklı satırlarda aynı takma adı
    # alıp almadığını denemek için.
    rows = [fake_person() for _ in range(row_count)]
    rows.append(dict(rows[0]))
    return pd.DataFrame(rows)


def main():
    # Sabit tohum (seed) ile her çalıştırmada aynı örnek dosyaları üretir.
    random.seed(42)
    SAMPLE_DATA_DIR.mkdir(exist_ok=True)

    text = build_sample_text(fake_person())
    (SAMPLE_DATA_DIR / "sample_text.txt").write_text(text, encoding="utf-8")

    table = build_sample_table(10)
    # utf-8-sig: Excel'in CSV'deki Türkçe karakterleri doğru göstermesi için BOM ekler.
    table.to_csv(SAMPLE_DATA_DIR / "sample_people.csv", index=False, encoding="utf-8-sig")
    table.to_excel(SAMPLE_DATA_DIR / "sample_people.xlsx", index=False)

    print(f"Sample files written to {SAMPLE_DATA_DIR}")


if __name__ == "__main__":
    main()
