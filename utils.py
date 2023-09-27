import csv
from typing import List

from config import labels
from schemas import LabelStatusSchema, LabelExplanations


def transform_string_to_schema(result: str) -> LabelStatusSchema:
    # Create a dictionary with the specified field set to True
    data = {field: True if field == result else False for field in labels}

    # Create a LabelStatusSchema instance from the dictionary
    schema = LabelStatusSchema(**data)

    return schema


def extract_binary_values_from_schemas(schema: LabelExplanations) -> List[int]:
    schema_labels = schema.label_explanation[1]
    schema_labels = [int(getattr(schema_labels, field_name)) for field_name in schema_labels.__annotations__.keys()]
    justification = schema.label_explanation[0].justification
    return schema_labels, justification


def write_to_csv(descriptions, final_labels, explanations, filename="output.csv"):
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Description", "Final Labels", "Explanation"])
        for desc, label, exp in zip(descriptions, final_labels, explanations):
            writer.writerow([desc, label, exp])


def read_descriptions_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]
