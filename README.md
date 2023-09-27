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
- [Project Structure](#project-structure)
- [License](#license)

## Overview

LLM-Auto-Labeler is an automated text labeling tool designed to reduce the need for time-consuming human intervention. It leverages multiple Language Model Mediators (LLMs) to assess, label, and provide justifications for text data.

## Features

- **Multi-Model Consensus**: Ensures robust labeling by employing multiple LLMs for the initial assessment.
- **Explanations**: Increases transparency by having each LLM provide justifications for its chosen label.
- **Mediation**: Utilizes a mediator LLM to make the final labeling decision, thereby reconciling any discrepancies between different LLMs.

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

Feel free to edit the placeholders like the documentation link, contributor's guide, or other specific details to fit your project's needs.
