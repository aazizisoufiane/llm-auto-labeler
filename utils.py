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
