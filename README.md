# LLM-Auto-Labeler

![Author](https://img.shields.io/badge/Author-Soufiane%20AAZIZI-brightgreen)
[![Medium](https://img.shields.io/badge/Medium-Follow%20Me-blue)](https://medium.com/@aazizi.soufiane)
[![GitHub](https://img.shields.io/badge/GitHub-Follow%20Me-lightgrey)](https://github.com/aazizisoufiane)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect%20with%20Me-informational)](https://www.linkedin.com/in/soufiane-aazizi-phd-a502829/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [API Configuration and Environmental Variables](#api-configuration-and-environmental-variables)
- [Project Structure](#project-structure)
- [License](#license)

## Overview

LLM-Auto-Labeler is an automated text labeling tool designed to reduce the need for time-consuming human intervention.
It leverages multiple Language Model Mediators (LLMs) to assess, label, and provide justifications for text data.

## Features

- **Multi-Model Consensus**: Ensures robust labeling by employing multiple LLMs for the initial assessment.
- **Explanations**: Increases transparency by having each LLM provide justifications for its chosen label.
- **Mediation**: Utilizes a mediator LLM to make the final labeling decision, thereby reconciling any discrepancies
  between different LLMs.

## Getting Started

### Prerequisites

To run this project, you'll need:

- Python 3.7 or higher
- Langchain library
- Pydantic library
- Your preferred LLM libraries (e.g., OpenAI's GPT, etc.)

### Installation

Clone the repository and install the necessary packages:

```bash
git clone https://github.com/yourusername/llm-auto-labeler.git
cd llm-auto-labeler
pip install -r requirements.txt
python src/main.py --description_file "input/descriptions"
```

### API Configuration and Environmental Variables

To run LLM-Auto-Labeler, you'll need access to specific Language Model Mediators (LLMs) APIs. For example, if you are
using OpenAI's GPT-based models and Replicate models, you'll need to set up the following API keys:

OPENAI_API_KEY for OpenAI's GPT-based models.
REPLICATE_API_TOKEN for Replicate models.
Place these API keys in a .env file located at the root directory of the project. The .env file should look like this:

```textmate
OPENAI_API_KEY=your_openai_api_key_here
REPLICATE_API_TOKEN=your_replicate_api_token_here
````

However, the modular architecture of LLM-Auto-Labeler allows you to use LLMs of your choice. If you want to integrate
other LLMs, make sure to read their respective documentation to obtain and configure additional API keys or access
tokens.

## Project Structure

```textmate
├── README.md
├── input
│   └── descriptions
├── logs
├── output
│   └── output.json
├── requirements.txt
└── src
    ├── __init__.py
    ├── autolabel.py
    ├── config.py
    ├── llm_handler.py
    ├── logger.py
    ├── main.py
    ├── schemas.py
    └── utils.py
```

## License

Feel free to edit the placeholders like the documentation link, contributor's guide, or other specific details to fit
your project's needs.
