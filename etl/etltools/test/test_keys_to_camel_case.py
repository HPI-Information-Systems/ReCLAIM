from etl.etltools.helpers import keys_to_camel_case


def test_words_with_spaces():
    assert keys_to_camel_case({"collection number": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"Arrival Date": 1}) == {"arrivalDate": 1}


def test_words_with_underscores():
    assert keys_to_camel_case({"collection_number": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"Arrival_Date": 1}) == {"arrivalDate": 1}


def test_words_with_dots():
    assert keys_to_camel_case({"collection.number": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"Arrival.Date": 1}) == {"arrivalDate": 1}


def test_words_with_slashes():
    assert keys_to_camel_case({"collection/number": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"Arrival/Date": 1}) == {"arrivalDate": 1}


def test_words_with_hyphens():
    assert keys_to_camel_case({"collection-number": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"Arrival-Date": 1}) == {"arrivalDate": 1}


def test_uppercase_woards():
    assert keys_to_camel_case({"COLLECTION NUMBER": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"BAND": 1}) == {"band": 1}


def test_pascal_case_words():
    assert keys_to_camel_case({"CollectionNumber": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"ArrivalDate": 1}) == {"arrivalDate": 1}


def test_camel_case_words():
    assert keys_to_camel_case({"collectionNumber": 1}) == {"collectionNumber": 1}
    assert keys_to_camel_case({"arrivalDate": 1}) == {"arrivalDate": 1}
