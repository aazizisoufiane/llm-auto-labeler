from typing import Tuple, List

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from pydantic import create_model

from config import labels


def generate_label_status_schema(field_names: List[str]) -> type:
    field_definitions = {}
    for field_name in field_names:
        field_definitions[field_name] = (bool, False)

    schema = create_model("LabelStatusSchema", **field_definitions)

    return schema


LabelStatusSchema = generate_label_status_schema(field_names=labels)


class JustificationModel(BaseModel):
    justification: str


class LabelExplanations(BaseModel):
    label_explanation: Tuple[JustificationModel, LabelStatusSchema]


parser_labels = PydanticOutputParser(pydantic_object=LabelExplanations)
format_instructions = parser_labels.get_format_instructions()
