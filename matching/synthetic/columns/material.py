import random
from .augment import *

EQUIV_MATERIALS = [
    ["oil on canvas", "oil", "oil paint", "Öl auf Leinwand", "Ölgemälde", "canvas"],
    ["Keramik", "ceramic"],
    ["Keramikstatue", "ceramic statue", "Statue"],
    ["Bronzestatue", "bronze statue", "Statue"],
    ["Marmorstatue", "Marmor", "marble", "marble statue", "Statue", "white marble", "weißer Marmor", "Marmor weiß", "weiße Marmorstatue"],
    ["enamel on bronze", "enamel"],
    ["gold", "metal", "Metall", "gold and silver", "Gold", "gold over silber", "Gold auf Silber", "Gold und Silber", "Silber und Gold"],
    ["silver", "metal", "Metall", "gold and silver", "Silber", "gold over silber", "Gold auf Silber", "Gold und Silber", "Silber und Gold"],
    ["wood", "Holzschnitt", "Holzarbeit", "Holzplatte", "Holz", "mahogany", "Holz / Stein"],
    ["metal", "Metall", "bronze", "Kupferlegierung"],
    ["metal", "Metall", "tin", "Zinn"],
    ["Sepiazeichnung, laviert", "Zeichnung", "Handzeichnung"],
    ["Federzeichnung, laviert", "Zeichnung", "Handzeichnung"],
    ["Stich", "Farbstich"],
    ["Stich", "Kupferstich"],
    ["Kohle auf Leinwand", "Kohle", "Kohlez.", "Kohlezeichnung"]
]


def get_random_equal_materials():
    equiv_list = random.choice(EQUIV_MATERIALS)
    return random.choice(equiv_list), random.choice(equiv_list)


def get_random_nonequal_materials():
    equiv_list1 = random.choice(EQUIV_MATERIALS)
    equiv_list2 = random.choice(EQUIV_MATERIALS)
    while equiv_list1 == equiv_list2:
        equiv_list2 = random.choice(EQUIV_MATERIALS)
    return random.choice(equiv_list1), random.choice(equiv_list2)

