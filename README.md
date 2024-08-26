# GOV.UK agent

A quick [Streamlit](https://streamlit.io) integration for [GOV.UK](https://www.gov.uk/). Uses [LangGraph](https://www.langchain.com/langgraph) and some simple tools to grab relevant information.

Literally the quickest, nastiest exploration of agents for GOV.UK.

# Setup

The project uses [poetry](https://python-poetry.org) for dependency management and [Poe the Poet](https://poethepoet.natn.io) for task running.

Create a `.env` with an `OPENAI_API_KEY` set.

Run with `poe run`.

Lint and format with `poe ruff`.
