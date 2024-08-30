# What is a taxonomy?

The `classification.ttl` and `material.ttl` files define taxonomies. Taxonomies describe networks of specializations, meaning that if A is a specialization of B, A has all the characteristics that B has.

## Examples
The following excerpt from the material taxonomy shows that `paint` has all the characteristics that `unknown` has, and `watercolor` has all the characteristics that `paint` has:

```turtle
Material:paint
    a                 jdcrp:Material ;
    jdcrp:name        "paint" ;
    jdcrp:wikidataUri wd:Q174219 ;
    jdcrp:subMaterialOf Material:unknown .

Material:watercolor
    a                   jdcrp:Material ;
    jdcrp:name          "watercolor" ;
    jdcrp:wikidataUri   wd:Q22915256 ;
    jdcrp:subMaterialOf Material:paint .
```

It is also possible to have multiple generalizations, as shown in this example:

```turtle
Material:paintedWood
    a                   jdcrp:Material ;
    jdcrp:name          "painted wood" ;
    jdcrp:subMaterialOf Material:wood, Material:paint .
```

## Considerations
One can argue that 'strange terms' like `unknown` should not be added to the taxonomies. However, `unknown` is one of the official classification options in the ERR data and also occurs in similar forms (e.g., k.a. (keine Angabe)) in other data sources. Therefore, our taxonomies aim to include all semantically unique terms that occur frequently (more than about 30 times) in the data.

If all semantically unique terms were to be added to the taxonomies, they would become too large to be beneficial for creating a shared vocabulary for developers and users.

## 'Made up' categories
Although most categories in the taxonomies often occur in the data, some terms were 'made up' as connectors. They structure the other categories more precisely than they were missing because they form a common generalization for multiple categories. One example is `drawing instrument`, which has `pen` and `pencil` as specializations. `skeletonPart`is also 'made up' and connects `ivory`, `bone`and `tortoise shell`.
