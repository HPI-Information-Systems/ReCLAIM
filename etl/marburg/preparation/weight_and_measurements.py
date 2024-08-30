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
    # in the marburburg data there are no occurences of weights in the measurements column

    regex = re.compile(r"\(\d+([.|,]\d+)? ?[x|X|&] ?\d+([.|,]\d+)?\)")

    if ("cm" in weight) or regex.search(weight) is not None:
        if weight in measurements:
            weight = ""
        if measurements in weight:
            measurements = weight
            weight = ""
        else:
            measurements = measurements + " " + weight
            weight = ""

    # convert measures to uppercase

    measurements = measurements.replace(" h", " H")
    measurements = measurements.replace(" w", " W")
    measurements = measurements.replace(" b", " B")
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
