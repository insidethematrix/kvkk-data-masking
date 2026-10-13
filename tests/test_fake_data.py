import random

from kvkk.detection import find_emails, find_phones
from kvkk.validation import is_valid_date, is_valid_iban, is_valid_luhn, is_valid_tckn
from scripts.generate_fake_data import (
    build_sample_table,
    build_sample_text,
    fake_birth_date,
    fake_card,
    fake_email,
    fake_iban,
    fake_person,
    fake_phone_digits,
    fake_tckn,
    format_phone,
    luhn_check_digit,
)

# Üretici ve doğrulayıcı birbirinden bağımsız yazıldı; bu testler ikisini çapraz kontrol eder.
SAMPLE_COUNT = 100


def test_fake_tckn_is_valid():
    random.seed(1)
    for _ in range(SAMPLE_COUNT):
        assert is_valid_tckn(fake_tckn())


def test_fake_iban_is_valid():
    random.seed(2)
    for _ in range(SAMPLE_COUNT):
        assert is_valid_iban(fake_iban())
        assert is_valid_iban(fake_iban(spaced=True))


def test_luhn_check_digit_known_example():
    # 4111 1111 1111 111? -> bilinen test kartı 4111 1111 1111 1111
    assert luhn_check_digit("411111111111111") == 1


def test_fake_card_is_valid():
    random.seed(3)
    for _ in range(SAMPLE_COUNT):
        assert is_valid_luhn(fake_card())
        assert is_valid_luhn(fake_card(spaced=False))


def test_fake_phone_formats_are_detected():
    random.seed(4)
    for style in ["spaced", "international", "dashed", "plain"]:
        phone = format_phone(fake_phone_digits(), style)
        assert len(find_phones("Tel: " + phone)) == 1, phone


def test_fake_email_is_ascii_and_detected():
    email = fake_email("Gülşen", "Öztürk")
    assert email.startswith("gulsen.ozturk@")
    assert len(find_emails(email)) == 1


def test_fake_birth_date_is_valid():
    random.seed(5)
    for _ in range(SAMPLE_COUNT):
        assert is_valid_date(fake_birth_date())


def test_same_seed_gives_same_person():
    random.seed(42)
    first = fake_person()
    random.seed(42)
    second = fake_person()
    assert first == second


def test_sample_text_contains_person_data():
    random.seed(6)
    person = fake_person()
    text = build_sample_text(person)
    for field in ["full_name", "tckn", "phone", "email", "iban", "credit_card", "birth_date"]:
        assert person[field] in text


def test_sample_table_has_duplicate_last_row():
    random.seed(7)
    table = build_sample_table(5)
    assert len(table) == 6
    assert table.iloc[0].equals(table.iloc[-1])
