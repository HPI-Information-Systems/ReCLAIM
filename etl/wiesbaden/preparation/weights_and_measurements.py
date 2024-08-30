import csv
from etl import etltools
from etl import common
import re


def add_space(match):
    return f"{match.group(1)} {match.group(2)}"


def prepare(weight: str, measurements: str) -> tuple:
    '''This function resolves the OCR errors that cause weight and measurements to be in the wrong columns and formats the weight and measurements columns'''
    if weight is None:
        weight = ""
    if measurements is None:
        measurements = ""

    # remove keywords
    weight = common.ccp_keywords.remove_ccp_keywords(weight)
    measurements = common.ccp_keywords.remove_ccp_keywords(measurements)

    # When we find a measure in the weight column, we move it to the measurements column
    #   - When both columns contain measures and one is part of the other, we store the longer one in the measurements column
    #       for example: weight: 0,42 by 0,28 m, measurements: 0,28 m -> weight: "", measurements: 0,42 by 0,28 m
    #   - Otherwise we concatenate the two columns with a whitespace in between
    if ("cm" in weight) or ("mm" in weight) or ("m" in weight):
        if weight in measurements:
            weight = ""
        if measurements in weight:
            measurements = weight
            weight = ""
        else:
            measurements = measurements + " " + weight
            weight = ""

    if ("gr" in measurements) or ("kg" in measurements) or (" g" in measurements):
        if measurements in weight:
            measurements = ""
        if weight in measurements:
            weight = measurements
            measurements = ""
        else:
            weight = weight + " " + measurements
            measurements = ""

    # convert o to 0
    measurements = measurements.replace("o,", "0,")
    measurements = measurements.replace(" o.", " 0.")

    # add whitespace before unit
    pattern = r"(\d+)([a-zA-Z]+)"

    measurements = re.sub(pattern, add_space, measurements)

    # convert by to x
    # by_pattern matches for example "0,32 by 0,29 cm"
    unit_regex = re.compile(r"(cm|m|mm)")
    by_pattern = re.compile(
        r"(\d+?(?:,\d+|.\d+)? ?(?:cm|m|mm)? ?by \d+(?:,\d+|.\d+)? ?(?:cm|m|mm)?)"
    )

    result = by_pattern.findall(measurements)

    if len(result) != 0:
        measurements = measurements.replace("by", "x")

        unit = unit_regex.findall(measurements)
        if len(unit) > 1:
            if unit[0] == unit[1]:
                unit_with_whitespace = unit[0] + " "
                measurements = measurements.replace(unit_with_whitespace, "", 1)

    # remove double unit
    x_pattern = re.compile(
        r"(\d+?(?:,\d+|.\d+)? ?(?:cm|m|mm)? ?x \d+(?:,\d+|.\d+)? ?(?:cm|m|mm)?)"
    )

    result = x_pattern.findall(measurements)

    if len(result) != 0:
        measurements = measurements.replace("by", "x")

        unit = unit_regex.findall(measurements)
        if len(unit) > 1:
            if unit[0] == unit[1]:
                unit_with_whitespace = unit[0] + " "
                measurements = measurements.replace(unit_with_whitespace, "", 1)

    # convert measures to uppercase

    measurements = measurements.replace(" h", " H")
    measurements = measurements.replace(" w", " W")
    measurements = measurements.replace(" l", " L")
    measurements = measurements.replace("h ", "H ")
    measurements = measurements.replace("w ", "W ")
    measurements = measurements.replace("l ", "L ")

    # trim
    measurements = measurements.strip()
    weight = weight.strip()

    return (weight, measurements)


def import_weight_and_measurements():
    data = etltools.data.csv_as_lines(
        source_id="wccp",
        file_path="wiesbaden-ccp-property-cards-ocr-export-postprocessed-16-11-23.csv",
    )

    with open("weight_and_measurements.csv", "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        for line in data:
            weight = format(line["weight"])
            measurements = format(line["measurements"])
            writer.writerow(
                [
                    weight,
                    measurements,
                    prepare(weight, measurements),
                ]
            )


def main():
    import_weight_and_measurements()
    print("done")


if __name__ == "__main__":
    main()
