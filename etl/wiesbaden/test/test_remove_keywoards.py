"""
    Test
"""

import etl


def test_keep_value_without_keywords():
    assert (
        etl.common.ccp_keywords.remove_ccp_keywords("oil on canvas") == "oil on canvas"
    )
    assert (
        etl.common.ccp_keywords.remove_ccp_keywords(
            "Stillife with fruits Strange colours, sometimes done in flat planes of light. The technique seems to be lack- ing as far as the drappery FOR goes. Top and bottom background browns."
        )
        == "Stillife with fruits Strange colours, sometimes done in flat planes of light. The technique seems to be lack- ing as far as the drappery FOR goes. Top and bottom background browns."
    )


def test_remove_uppercase_keywords():
    assert (
        etl.common.ccp_keywords.remove_ccp_keywords("DATE 12.12.2020") == " 12.12.2020"
    )
    assert (
        etl.common.ccp_keywords.remove_ccp_keywords("MATERIAL oil on canvas")
        == " oil on canvas"
    )
    assert etl.common.ccp_keywords.remove_ccp_keywords("PROPERTY CARD ART") == ""


def test_remove_keyword_with_colon():
    assert etl.common.ccp_keywords.remove_ccp_keywords("PROPERTY CARD-ART:") == ""
    assert etl.common.ccp_keywords.remove_ccp_keywords("DEPOT NO: 35") == " 35"
    assert (
        etl.common.ccp_keywords.remove_ccp_keywords(
            "ARRIVAL CONDITION: good, undamaged"
        )
        == " good, undamaged"
    )


def test_remove_lowercase_keyword():
    assert etl.common.ccp_keywords.remove_ccp_keywords("property card") == ""
    assert etl.common.ccp_keywords.remove_ccp_keywords("Weight: 1650 gr") == " 1650 gr"


def test_mixed_case_keywords():
    assert etl.common.ccp_keywords.remove_ccp_keywords("oTHER PHOTOS:") == ""
