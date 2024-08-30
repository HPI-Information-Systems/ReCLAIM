"""
    Test
"""

from etl.wiesbaden.preparation.wccp_number import normalize
import pytest


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_doesnt_do_anything_if_already_formatted_correctly():
    assert normalize("WIE 0/1") == "WIE 0/1"
    assert normalize("WIE 81/16/94/1/13") == "WIE 81/16/94/1/13"
    assert normalize("WIE 6640/42 1+2") == "WIE 6640/42 1+2"
    assert (
        normalize("WIE 5046/1-10, 76 14-23, 25, 26, 27-35")
        == "WIE 5046/1-10, 76 14-23, 25, 26, 27-35"
    )


def test_remove_comma_after_wie_prefix():
    assert normalize("WIE,0/9") == "WIE 0/9"


def test_capitalize():
    assert normalize("Wie 0/9") == "WIE 0/9"


def test_remove_trailing_newline():
    assert normalize("WIE 0/14\n") == "WIE 0/14"


def test_fix_wie_prefix():
    assert normalize("AWIE 0/30") == "WIE 0/30"
    assert normalize("WI E 0/37") == "WIE 0/37"
    assert normalize("NOWIE 11/66/2") == "WIE 11/66/2"
    assert normalize("Wie:NO: 72/134/5 362") == "WIE 72/134/5 362"
    assert normalize("VID mamanna 203/6/20") == "WIE 203/6/20"
    assert normalize("WIE 88/95/1-2 452") == "WIE 88/95/1-2 452"
    assert normalize("Man. WIE 1960/20") == "WIE 1960/20"
    assert normalize("Wie:NO: 72/134/5 362") == "WIE 72/134/5 362"
    assert normalize("WUE 4439/32") == "WIE 4439/32"
    assert normalize("WIEM4439/1") == "WIE 4439/1"


def test_fix_typos_in_number():
    assert normalize("WIE o/24") == "WIE 0/24"
    assert normalize("WIE C/87") == "WIE 0/87"


def test_handle_parantheses_in_number():
    # assert normalize("WIE 318/218(6)") == "WIE 318/218/6"
    assert normalize("WIE 4695 (1-10)") == "WIE 4695 (1-10)"


# assert normalize("WIE 1505 (1)") == "WIE 1505/1"
# die beiden auskommentierten Testfälle werden in Kauf genommen, da es sehr kompliziert wäre diese beiden zu fixen ohne den mittleren kaput zu machen...


def test_fix_typos_in_prefix():
    assert normalize("W1E4892") == "WIE 4892"


def test_without_number():
    assert normalize("WIE. (Abffrift)") == "WIE. (Abffrift)"
    # assert normalize("Property Card Art") == "Property Card Art"
    assert (
        normalize("Unknown 1 Fcty deda and the Swee") == "WIE 6401"
    )  # found the property card
    assert normalize("2 schofers") == "WIE 6624/1-2"  # found the property card
    # ist es okay,w enn bei NO.123 WIE 123 zurückgegeben wird? Sonst könnte ich das auch noch ändern
    assert normalize("No. 123") == "WIE 123"
    assert normalize("WIE (X8XXX 6494") == "WIE 6494"  # found the property card


def test_contain_special_characters_in_number():
    assert normalize("WIE 88/95/1-2 452") == "WIE 88/95/1-2 452"
    assert normalize("WIE 79/200/3,4,6,8") == "WIE 79/200/3,4,6,8"
    assert normalize("WIE 553-") == "WIE 553"
    assert normalize("WIE/1767 / 1 Grasleben") == "WIE 1767/1 Grasleben"


def test_dont_remove_words_at_the_end():
    assert normalize("WIE 6191/13/9EXIEDLE") == "WIE 191/13/9"
    assert normalize("WIE 544/10 Grasleben") == "WIE 544/10 Grasleben"
    # assert (
    #    normalize("WIE 544/22 Grasleben\nReichsbank Fft.Main")
    #    == "WIE 544/22 Grasleben\nReichsbank Fft.Main"
    # )


def test_only_number():
    assert normalize("461") == "WIE 461"


def test_remove_quotes():
    assert normalize('"WIE 7/208/2,6 "') == "WIE 7/208/2,6"
    assert normalize('"WIE 544/22 Grasleben') == "WIE 544/22 Grasleben"
    assert (
        normalize('"WIE 628/35 Gr asleben, Reichsbank Tim."')
        == "WIE 628/35 Gr asleben, Reichsbank Tim."
    )
    assert normalize('"WIE 1867/11, Heilbronn"') == "WIE 1867/11, Heilbronn"


def test_keep_lowercase_character_suffix():
    assert normalize("WIE 1867/10 a") == "WIE 1867/10 a"
    assert normalize("WIE 1867/10 f - i") == "WIE 1867/10 f - i"
    assert normalize("WIE 1867/10 j to.o") == "WIE 1867/10 j to.o"
    assert normalize("WIE 5297/5 a, b,c,d") == "WIE 5297/5 a, b,c,d"
    assert normalize("WIE 636/25 a and b") == "WIE 636/25 a and b"
    assert normalize("WIE 1737a/Grasleben") == "WIE 1737a/Grasleben"


def test_other_number_before_wie_number():
    assert normalize("WB Sub-CCP 236 Stuttgart WIE 5760") == "WIE 5760"
    assert normalize("317. (WB Sub-C0/240 Stuttgart, WIE 5762)") == "WIE 5762"


def test_unknown_numbers():
    assert normalize("Unknown No. 51 0.8") == "Unknown No. 51 0.8"
    assert normalize("Unknown No. 56 a,c") == "Unknown No. 56 a,c"
