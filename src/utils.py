import csv
from typing import List
import json

from config import labels
from schemas import LabelStatusSchema, LabelExplanations


def transform_string_to_schema(result: str) -> LabelStatusSchema:
    """
    Transforms a result string into a LabelStatusSchema object.

    Parameters:
        result (str): The label string to be transformed.

    Returns:
        LabelStatusSchema: An object with fields set based on the given result.
    """
    # Create a dictionary with the specified field set to True
    data = {field: True if field == result else False for field in labels}

    # Create a LabelStatusSchema instance from the dictionary
    schema = LabelStatusSchema(**data)

    return schema


def extract_binary_values_from_schemas(schema: LabelExplanations) -> List[int]:
    """
    Extracts the binary values and justifications from the given LabelExplanations schema.

    Parameters:
        schema (LabelExplanations): The schema object containing the label and justification.

    Returns:
        List[int], str: A list of binary values representing the selected labels and the justification string.
    """
    schema_labels = schema.label_explanation[1]
    schema_labels = [
        int(getattr(schema_labels, field_name))
        for field_name in schema_labels.__annotations__.keys()
    ]
    justification = schema.label_explanation[0].justification
    return schema_labels, justification


def write_to_csv(
    descriptions, init_labels, final_labels, explanations, filename="output/output.csv"
):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Labels", "Final Labels", "Explanation"])
        for desc, label, final_label, exp in zip(
            descriptions, init_labels, final_labels, explanations
        ):
            writer.writerow([desc, label, final_label, exp])


def write_to_json(
    descriptions, init_labels, final_labels, explanations, filename="output/output.json"
):
    data = []
    for desc, final_label, exp in zip(descriptions, final_labels, explanations):
        data.append(
            {
                "Description": desc,
                "Labels": init_labels,
                "Final Labels": final_label,
                "Explanation": exp,
            }
        )

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def read_descriptions_from_file(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]
