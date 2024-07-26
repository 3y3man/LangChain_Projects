# LangChain Project

This repository showcases a project built using LangChain, a powerful framework for building applications with language models. The project demonstrates various features and capabilities of LangChain, integrated with OpenAI's API.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- You have Python installed on your local machine.
- You have an OpenAI API key. If you don't have one, you can get it [here](https://platform.openai.com/signup).

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/3y3man/LangChains/langchain-project.git
    cd langchain-project
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API key:
    Create a `.env` file in the root directory of your project and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

To run the project, execute the following command:
```bash
streamlit run main.py
```

This will start a local server and open the application in your default web browser.

## Project Structure

- `main.py`: The main script to run the application.
- `requirements.txt`: The list of dependencies required to run the project.

## Contributing

If you want to contribute to this project, please fork the repository and create a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [OpenAI](https://openai.com)

