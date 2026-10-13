import pytest

from kvkk.detection import Finding, find_all
from kvkk.protection import mask, protect_text


def test_phone_masking():
    assert mask(Finding("PHONE", "0532 123 45 67", 0, 14)) == "532***4567"
    assert mask(Finding("PHONE", "+905321234567", 0, 13)) == "532***4567"


def test_email_masking():
    assert mask(Finding("EMAIL", "deneme@ornek.com", 0, 16)) == "d***@ornek.com"


def test_positions_do_not_shift_with_multiple_findings():
    text = "A: 0532 123 45 67, B: x@ornek.com, C: 0555 999 88 77 son."
    result = protect_text(text, find_all(text))
    assert result == "A: 532***4567, B: x***@ornek.com, C: 555***8877 son."


def test_text_without_findings_is_unchanged():
    text = "Burada kişisel veri yok."
    assert protect_text(text, find_all(text)) == text


def test_unknown_method_raises_error():
    with pytest.raises(ValueError):
        protect_text("metin", [], method="magic")
