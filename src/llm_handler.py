from typing import List

from langchain.chains import LLMChain

# ... other imports ...
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from src.schemas import parser_labels, format_instructions
from src.utils import extract_binary_values_from_schemas, transform_string_to_schema


class LLMChainHandler:
    """
    Handles the complete lifecycle of obtaining, mediating, and finalizing labels
    for a given text description using multiple Language Learning Models (LLMs).
    """

    def __init__(self, llm_mediator, llms, labels, verbose=False):
        """
        Initializes the LLMChainHandler with a mediator LLM, a list of LLMs for
        initial labeling, and a list of possible labels.

        Parameters:
            llm_mediator: The mediator LLM used to make the final label decision.
            llms: A list of LLMs used for initial labeling.
            labels: A list of possible labels.
            verbose: A flag to control verbosity (optional).
        """
        self.labels = labels
        self.description = None
        self.llms = llms
        self.llm_mediator = llm_mediator
        self.verbose = verbose
        self.llm_label_responses = []
        self.mediated_labels = None

    def collect_multiple_llm_labels(self):
        """
        Collects label suggestions from multiple LLMs for a given description.
        """

        template = """As a human specialist in data labeling, your mission is to carefully assess the provided description and select the most suitable label from the 
        list below. If none of the labels apply, you can leave it blank: 

        {description}

        This is the list of available labels: {labels}


        your response with explanation why?: """

        # Define the human message prompt template.
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=template,
                input_variables=["description", "labels"],
                format_instructions={"labels": self.labels},
            )
        )

        # Create the chat prompt template.
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])

        # Create the extraction chain.
        if not isinstance(self.llms, list):
            self.llms = [self.llms]
        for llm in self.llms:
            extractions = LLMChain(
                llm=llm, prompt=chat_prompt_template, verbose=self.verbose
            )
            self.llm_label_responses.append(
                extractions.run(
                    {"description": self.description, "labels": self.labels}
                )
            )

    def mediate_label_choices(self):
        """
        Uses a mediator LLM to evaluate and make the final label choice
        based on the labels suggested by the other LLMs.
        """

        template = """As an expert in data labeling, your task is to carefully evaluate a set of provided answers to determine if they are correct. You will be given a 
        description, a list of possible labels, and a set of answers from other language models (LLMs). Your job is to choose whether one or all of these answers are correct. 
        The responses you provide should consist solely of labels without additional information. If none of the labels apply, you can leave the response blank.

                Description: {description}

                Available labels: {labels}

                Answers from other LLMs: {llm_answers}

                Please provide your response and explain your choice based on the information provided, taking into account the answers from other LLMs:


                {format_instructions}    
                """

        # Define the human message prompt template.
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(
                template=template,
                input_variables=["description", "labels", "llm_answers"],
                format_instructions={
                    "labels": self.labels,
                    "llm_answers": self.llm_label_responses,
                },
                partial_variables={"format_instructions": format_instructions},
            )
        )

        # Create the chat prompt template.
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])

        # Create the extraction chain.

        extractions = LLMChain(
            llm=self.llm_mediator, prompt=chat_prompt_template, verbose=self.verbose
        )
        self.mediated_labels = extractions.run(
            {
                "description": self.description,
                "labels": self.labels,
                "llm_answers": self.llm_label_responses,
            }
        )

    def extract_labels_and_transform_schema(self):
        """
        Attempts to parse the mediated labels into the desired schema. If parsing
        fails, it transforms the string into the required schema. Finally, it
        transforms the labels into binary values.

        Returns:
            A list of lists containing binary values representing the final label selections.
        """
        try:
            self.mediated_labels = parser_labels.parse(self.mediated_labels)
        except:
            self.mediated_labels = transform_string_to_schema(self.mediated_labels)
        return extract_binary_values_from_schemas(self.mediated_labels)

    def label_extraction_and_binary_values(self) -> List[List[int]]:
        """
        Transforms the final labels into binary values.

        Returns:
            A list of lists containing binary values representing label selections.
        """

    # return binary_values

    def run(self, description):
        """
        Runs the complete label generation process for a given description.

        Parameters:
            description: The text description to be labeled.

        Returns:
            final_labels: The final set of labels chosen for the description.
            justifications: Justifications for each label chosen.
        """

        self.description = description
        self.collect_multiple_llm_labels()
        self.mediate_label_choices()
        final_labels, justifications = self.extract_labels_and_transform_schema()
        return final_labels, justifications
