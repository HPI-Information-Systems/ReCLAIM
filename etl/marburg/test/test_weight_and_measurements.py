from etl.marburg.preparation.weight_and_measurements import prepare


def test_keep_right_format():
    assert prepare("", "78 x 36 cm") == ("", "78 x 36 cm")
    assert prepare("", "0,17 x 0,14 m") == ("", "0,17 x 0,14 m")
    assert prepare("520 gr", "Ø 23 cm") == ("520 gr", "Ø 23 cm")
    assert prepare("", "20 1/2 x 17 cm") == (
        "",
        "20 1/2 x 17 cm",
    )


def test_wrong_column():
    assert prepare("(97.5x124)", "H.:84 B.:102") == (
        "",
        "H.:84 B.:102 (97.5x124)",
    )
    assert prepare("(253 X 60)", "H.122 b.:96") == (
        "",
        "H.122 B.:96 (253 X 60)",
    )
