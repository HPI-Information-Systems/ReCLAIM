from etl.err.preparation.html_links import remove


# this pattern is used 131 of 136 times in the data when there is "href" in the string
def test_remove_target_blank_pattern():
    assert (
        remove(
            "<a target='_blank' href='http://www.imj.org.il/imagine/irso/itemirso.asp?table=comb&itemNum=246839'>Francke</a>"
        )
        == "Francke (http://www.imj.org.il/imagine/irso/itemirso.asp?table=comb&itemNum=246839)"
    )
    assert (
        remove(
            "<a target='_blank' href='http://www.gallery.ca/en/about/382.php'>Li 47</a>"
        )
        == "Li 47 (http://www.gallery.ca/en/about/382.php)"
    )
    assert (
        remove(
            "<a target='_blank' href='http://www.culture.gouv.fr/public/mistral/mnrbis_fr?ACTION=RETROUVER&FIELD_1=TOUT&VALUE_1=&FIELD_2=Caut&VALUE_2=&FIELD_3=Cdate&VALUE_3=&FIELD_4=Ctitre&VALUE_4=commode&FIELD_5=LOCA&VALUE_5=&FIELD_6=Ctexte&VALUE_6=&FIELD_7=Domaine&VALUE_7=&NUMBER=4&GRP=0&REQ=%28%28commode%29%20%3aTITR%2cATIT%2cAUTI%2cPTIT%2cDENO%2cDESC%2cSUITE%20%29&USRNAME=nobody&USRPWD=4%24%2534P&SPEC=9&SYN=1&IMLY=&MAX1=1&MAX2=1&MAX3=50&DOM=All'>commode</a>"
        )
        == "commode (http://www.culture.gouv.fr/public/mistral/mnrbis_fr?ACTION=RETROUVER&FIELD_1=TOUT&VALUE_1=&FIELD_2=Caut&VALUE_2=&FIELD_3=Cdate&VALUE_3=&FIELD_4=Ctitre&VALUE_4=commode&FIELD_5=LOCA&VALUE_5=&FIELD_6=Ctexte&VALUE_6=&FIELD_7=Domaine&VALUE_7=&NUMBER=4&GRP=0&REQ=%28%28commode%29%20%3aTITR%2cATIT%2cAUTI%2cPTIT%2cDENO%2cDESC%2cSUITE%20%29&USRNAME=nobody&USRPWD=4%24%2534P&SPEC=9&SYN=1&IMLY=&MAX1=1&MAX2=1&MAX3=50&DOM=All)"
    )


def test_extra_space():
    assert (
        remove(
            "<a target='_blank'  href='http://www.mfa.org/collections/object/marguerite-de-gas-the-artists-sister-4905'>DW 1582</a>"
        )
        == "DW 1582 (http://www.mfa.org/collections/object/marguerite-de-gas-the-artists-sister-4905)"
    )


def test_dont_change_other_strings():
    assert (
        remove(
            '<a href=""http://www.diplomatie.gouv.fr/fr/sites/archives_diplo/schloss/tableauxO/tableaux126.html?provenance=collection target=""_blank"">'
        )
        == '<a href=""http://www.diplomatie.gouv.fr/fr/sites/archives_diplo/schloss/tableauxO/tableaux126.html?provenance=collection target=""_blank"">'
    )
    assert remove("This is a test string") == "This is a test string"


def test_two_links():
    assert (
        remove(
            "This is some example text. <a target='_blank' href='http://www.gallery.ca/en/about/382.php'>Li 47</a> And after the link there is even more text and another link. <a target='_blank' href='http://www.google.de'>das ist google</a>"
        )
        == "This is some example text. Li 47 (http://www.gallery.ca/en/about/382.php) And after the link there is even more text and another link. das ist google (http://www.google.de)"
    )
