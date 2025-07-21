# Majo

Meet **Majo**, the command-line agent that's about changing how you work. **Majo** provides interactive capabilities to supercharge your terminal productivity, making your command line truly smart to manage your email!

This agent is designed to help you manage your email, allowing you to easily perform queries, generate reports, and manage your service.

`CURRENT STATUS:` ***Majo is in its early stages of development. Community contributions are welcome!***

## TECH STACK

- [Typer](https://typer.tiangolo.com/): Fast, typed CLI library for Python.
- [Langgraph](https://langchain-ai.github.io/langgraphjs/) and [Langchain](https://python.langchain.com/): A frameworks for building LLM-powered agents.
- [Pydantic](https://docs.pydantic.dev/): A library for data validation and settings management.

## DEVELOPMENT
To run **Majo** locally in development mode, follow these recommendations:

#### Set env variables:
Create a `.env` file at workspace folder to store the required environment variables. Take a look at [.env.example](.env.example) file for reference. If you do not want to use an `.env` file, you can set the environment variables in the code in execution time.

#### Install UV:
This project uses [UV](https://docs.astral.sh/uv/) to manage the dependencies and run the project. To install UV, follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) according to your operating system.

#### Configure virtual environment:
- Create a virtual environment:
```bash
uv venv
```
- Activate the virtual environment:
```bash
source .venv/bin/activate
```

#### Install dependencies:
```bash
uv sync
```

#### Run the project:
Use the following command to get the help of the CLI:
```bash
uv run src/majo/cli.py --help
```

Currently, you can run the following commands to get the help of the CLI:
```bash
uv run src/majo/cli.py ask --help
```
```bash
uv run src/majo/cli.py graph --help
```


## CONTRIBUTIONS
**Majo** project is open source and therefore any interested software developer can contribute to its improvement. To contribute, take a look at the following recommendations:

- **Bug Reports**: If you find a bug, please create an issue detailing the problem, the steps to reproduce it, and the expected behavior.
- **Feature Requests**: If you have an idea for a new feature or an enhancement to an existing one, please create an issue describing your idea.
- **Pull Requests**: If you've fixed a bug or implemented a new feature, we'd love to see your work! Please submit a pull request. Make sure your code follows the existing style and all tests pass.