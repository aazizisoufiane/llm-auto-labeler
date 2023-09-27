import argparse

from langchain.chat_models import ChatOpenAI
from langchain.llms import Replicate

from config import labels
from llm_handler import LLMChainHandler
from logger import logger
from utils import write_to_csv, read_descriptions_from_file, write_to_json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Auto-label descriptions using LLMs.")
    parser.add_argument(
        "--description_file",
        type=str,
        help="Path to the file containing descriptions to label",
        default="input/descriptions",
    )

    args = parser.parse_args()

    # Initialize the individual LLMs for the initial labeling
    llms = [
        ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0.9),
        Replicate(
            model="meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
            model_kwargs={"temperature": 0.9, "max_length": 500, "top_p": 1},
        ),
    ]

    # Initialize the mediator LLM
    llm_mediator = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature=0.9)

    handler = LLMChainHandler(
        llm_mediator=llm_mediator,
        llms=llms,
        labels=labels,
    )
    if args.description_file:
        descriptions = read_descriptions_from_file(args.description_file)
        all_final_labels = []
        all_explanations = []

        for description in descriptions:
            try:
                final_labels, explanation = handler.run(description)

                all_final_labels.append(final_labels)
                all_explanations.append(explanation)
                logger.info(f"Successfully processed description: {description[:100]}")

            except Exception as e:
                logger.error(
                    f"An error occurred while processing the description '{description[:100]}': {e}"
                )

                # Write the results to a CSV file
        try:
            write_to_json(descriptions, labels, all_final_labels, all_explanations)
            logger.info("Successfully wrote the results to a CSV file.")
        except Exception as e:
            logger.error(f"Failed to write to CSV: {e}")

    else:
        logger.warning("Please provide the path to the description file.")
