from typing import List

from langchain.chains import LLMChain
# ... other imports ...
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (ChatPromptTemplate, HumanMessagePromptTemplate, )

from schemas import parser_labels, format_instructions
from utils import extract_binary_values_from_schemas, transform_string_to_schema


class LLMChainHandler:
    def __init__(self, llm_mediator, llms, labels, verbose=False):
        self.labels = labels
        self.description = None
        self.llms = llms
        self.llm_mediator = llm_mediator
        self.verbose = verbose
        self.llm_label_responses = []
        self.mediated_labels = None

    def collect_multiple_llm_labels(self):

        template = '''As a human specialist in data labeling, your mission is to carefully assess the provided description and select the most suitable label from the 
        list below. If none of the labels apply, you can leave it blank: 

        {description}

        This is the list of available labels: {labels}


        your response with explanation why?: '''

        # Define the human message prompt template.
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(template=template, input_variables=["description", "labels"],
                format_instructions={"labels": self.labels},

            ))

        # Create the chat prompt template.
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])

        # Create the extraction chain.
        if not isinstance(self.llms, list):
            self.llms = [self.llms]
        for llm in self.llms:
            extractions = LLMChain(llm=llm, prompt=chat_prompt_template, verbose=self.verbose)
            self.llm_label_responses.append(extractions.run({"description": self.description, "labels": self.labels}))

    def mediate_label_choices(self):

        template = '''As an expert in data labeling, your task is to carefully evaluate a set of provided answers to determine if they are correct. You will be given a 
        description, a list of possible labels, and a set of answers from other language models (LLMs). Your job is to choose whether one or all of these answers are correct. 
        The responses you provide should consist solely of labels without additional information. If none of the labels apply, you can leave the response blank.

                Description: {description}

                Available labels: {labels}

                Answers from other LLMs: {llm_answers}

                Please provide your response and explain your choice based on the information provided, taking into account the answers from other LLMs:


                {format_instructions}    
                '''

        # Define the human message prompt template.
        human_message_prompt = HumanMessagePromptTemplate(
            prompt=PromptTemplate(template=template, input_variables=["description", "labels", "llm_answers"],
                format_instructions={"labels": self.labels, "llm_answers": self.llm_label_responses},
                partial_variables={"format_instructions": format_instructions},

            ))

        # Create the chat prompt template.
        chat_prompt_template = ChatPromptTemplate.from_messages([human_message_prompt])

        # Create the extraction chain.

        extractions = LLMChain(llm=self.llm_mediator, prompt=chat_prompt_template, verbose=self.verbose)
        self.mediated_labels = extractions.run(
            {"description": self.description, "labels": self.labels, "llm_answers": self.llm_label_responses})

    def extract_labels_and_transform_schema(self):

        try:
            self.mediated_labels = parser_labels.parse(self.mediated_labels)
        except:
            self.mediated_labels = transform_string_to_schema(self.mediated_labels)

    def label_extraction_and_binary_values(self) -> List[List[int]]:

        # resulting_schemas = extract_labels_and_transform_schema(llm, labels, description,llm_answers, verbose=verbose)
        return extract_binary_values_from_schemas(self.mediated_labels)

    # return binary_values

    def run(self, description):
        self.description = description
        self.collect_multiple_llm_labels()
        self.mediate_label_choices()
        self.extract_labels_and_transform_schema()
        self.label_extraction_and_binary_values()
        final_labels, justifications = self.label_extraction_and_binary_values()
        return final_labels, justifications
