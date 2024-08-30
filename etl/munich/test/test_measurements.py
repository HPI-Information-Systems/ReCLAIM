from munich.preparation.measurements import merge_measurements


def test_multiple_measurements():
    assert merge_measurements("10", "20", "30") == "10 x 20 x 30"
    assert merge_measurements("10", None, "30.5") == "10 x 30.5"


def test_single_measurement():
    assert merge_measurements("10", None, None) == "10"
    assert merge_measurements(None, "20", None) == "20"
    assert merge_measurements(None, None, "30") == "30"


def test_no_measurement():
    assert merge_measurements(None, None, None) == None
