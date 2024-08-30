"""
    Test
"""

from etl.wiesbaden.preparation.weights_and_measurements import prepare


def test_keep_right_format():
    assert prepare("", "78 x 36 cm") == ("", "78 x 36 cm")
    assert prepare("", "0,17 x 0,14 m") == ("", "0,17 x 0,14 m")
    assert prepare("520 gr", "Ø 23 cm") == ("520 gr", "Ø 23 cm")
    assert prepare("", "20 1/2 x 17 cm") == (
        "",
        "20 1/2 x 17 cm",
    )


def test_convert_by_to_x():
    assert prepare("", "0.24 by 0.145 cm") == (
        "",
        "0.24 x 0.145 cm",
    )
    assert prepare("", "0,185 by 0,243 cm") == (
        "",
        "0,185 x 0,243 cm",
    )
    assert prepare("", "29,2 cm by 1940 cm") == (
        "",
        "29,2 x 1940 cm",
    )
    assert prepare("", "0,29 cm by 0,20") == (
        "",
        "0,29 cm x 0,20",
    )
    assert prepare("", "0,29 by 0,20 m") == (
        "",
        "0,29 x 0,20 m",
    )
    assert prepare("", "0,185 by 0,243 m") == (
        "",
        "0,185 x 0,243 m",
    )
    assert prepare("", "5 by 5 m") == ("", "5 x 5 m")


def test_add_whitespace():
    assert prepare("", "12,5 x 15,50m") == (
        "",
        "12,5 x 15,50 m",
    )


def test_h_and_w_given_in_measurements():
    assert prepare("", "h 60 cm W 33 cm") == (
        "",
        "H 60 cm W 33 cm",
    )
    assert prepare("", "H. 153 cm") == ("", "H. 153 cm")
    assert prepare("1200 gr", "h 29 cm") == (
        "1200 gr",
        "H 29 cm",
    )
    assert prepare("1890 gr", "h 17 cm w 21 cm") == (
        "1890 gr",
        "H 17 cm W 21 cm",
    )
    assert prepare("10 gr together", "h 9,2 cm and 7,9 cm") == (
        "10 gr together",
        "H 9,2 cm and 7,9 cm",
    )
    assert prepare("", "L 49 cm") == ("", "L 49 cm")
    assert prepare("", "H 14,4 cm, B 17,8 cm") == (
        "",
        "H 14,4 cm, B 17,8 cm",
    )
    # or do we want to add x in the middle as well?


def test_o_to_0():
    assert prepare("", "0,185 by o,243 m") == (
        "",
        "0,185 x 0,243 m",
    )


def test_trim():
    assert prepare(" 80 gr", "1 20,5 cm") == (
        "80 gr",
        "1 20,5 cm",
    )


def test_remove_keywords():
    assert prepare("WEIGHT", "78 x 36 cm") == ("", "78 x 36 cm")
    assert prepare("DEPOT POSSESSOR,", "78 x 36 cm") == (
        ",",
        "78 x 36 cm",
    )
    assert prepare("Weight:", "Measurements: L W H") == (
        "",
        "L W H",
    )
    assert prepare("MEASUREMENTS", "78 x 36 cm") == (
        "",
        "78 x 36 cm",
    )


def test_remove_double_unit():
    assert prepare("", "0,42 cm x 0,28 cm") == (
        "",
        "0,42 x 0,28 cm",
    )
    assert prepare("", "5m x 6,7 m") == ("", "5 x 6,7 m")
    assert prepare("", "0,42 cm x 0,28cm") == (
        "",
        "0,42 x 0,28 cm",
    )


def test_wrong_column():
    assert prepare("0,42 by 0,28 m", "0,42 by 0,28 m") == (
        "",
        "0,42 x 0,28 m",
    )
    assert prepare("0,59 m", "") == ("", "0,59 m")
    assert prepare("B. 30 cm", "H. 53 cm, B. 30 cm") == (
        "",
        "H. 53 cm, B. 30 cm",
    )
    # assert prepare("","h 27 cm, 530 gr") == ("530 gr","h 27 cm")
    assert prepare("-", "430 gr.") == ("- 430 gr.", "")
    assert prepare("", "65,167 kg (total)") == (
        "65,167 kg (total)",
        "",
    )
    assert prepare("", "1, 727 (total) kg") == (
        "1, 727 (total) kg",
        "",
    )
    assert prepare("2.354 kg", "2.354 kg") == ("2.354 kg", "")
    assert prepare("D. 0.51 m", "Br. 1,64 m") == (
        "",
        "Br. 1,64 m D. 0.51 m",
    )
    assert prepare("1.415.22 rough grams", "WEIGHT: 1.415.22 rough grams") == (
        "1.415.22 rough grams",
        "",
    )


# alle Daten sind in der Form Weight, Measurements

# weitere Testfälle
# nan,1.39 by-0.93 m,"('nan', '1.39 by-0.93 m')"
# nan,"1,54 byt 1,10 m","('nan', '1,54 byt 1,10 m')"
# "MEASUREMENTS: 0,34 x 0,25 m","0,34 x 0,25 m","('', '0,34 x 0,25 : 0,34 x 0,25 m')"
# nan,"1, 727 (total) hg","('nan', '1, 727 (total) Hg')"

# komplexe Felder
# nan,"0,15 by 0,15 (each small pic- ture 0,82 by 1,11 m the whole"
# nan,"0,56 m (with frame)"
# nan,"2,02 by 1,08 m (each)"#
# MEASUREMENTS: Frankfux,L. 27 cm
# nan,"box 43x34.5 cm, book 37.5x28 cm, seal 16 cm"
# nan,"a) Br. 16 cm bl. Br. 13,5 cm C) Br. 14 cm"
# nan,Maße Mappe 99 x 70
# 859 gr.,"H. 32 cm (Chalice), 16.5 cm (Patene)"
# MEASUREMENTS,"H. 74,2, Br. 72, D. 47,5 cm"
# taly 18th cent.,29 x 29 x 23 cm
# nan,"1) 276 x 164 cm, 2) 305 x 164, 3) 176 x 164, 4) 272 x 164"
# nan,"H. 8,3 cm (cup), 12,5 cm (saucer)"
# %.,..)
# 17 16 11,10 Inch
# Weight:,Measurements: 4 Brussels about 1700 W H 377 x 275 on
# 30 x 35 cm,"L: Unknown, W: Unknown, H: Unknown"
# "L: Unknown late 17th cent, W: Unknown late 17th cent, H: 33,8cm","L: Unknown late 17th cent. 1 large plate, W: 33,8cm"
# 24:00,L W
