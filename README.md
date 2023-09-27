# LLM-Auto-Labeler

## Overview

LLM-Auto-Labeler is an automated text labeling tool that employs multiple Language Model Mediators (LLMs) to assess, label, and justify text data. This reduces the need for time-consuming human intervention.

## Features

- **Multi-Model Consensus**: Utilizes multiple LLMs to ensure robust labeling.
- **Explanations**: Each LLM provides justifications for its label, increasing transparency.
- **Mediation**: A final LLM acts as a mediator, making the ultimate labeling decision based on the outputs of other LLMs.

## Getting Started

### Prerequisites

- Python 3.7+
- Langchain
- Pydantic
- Your preferred LLM libraries

### Installation

```bash
git clone https://github.com/yourusername/llm-auto-labeler.git
cd llm-auto-labeler
pip install -r requirements.txt
python main.py --description_file "descriptions"
```

