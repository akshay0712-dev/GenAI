
# Cursore AI Assistant

Cursore AI Assistant is a command-line intelligent assistant that helps you generate production-ready web applications step-by-step using OpenAI's chat model. It interacts with the file system using predefined tools and follows a structured workflow: **plan → action → observe → output**.

## Features

- Built-in tools for managing files, directories, and system commands.
- Follows a structured format for AI responses using JSON.
- Handles tool execution, error reporting, and feedback collection.
- Defaults to Python/HTML/CSS/JS if no stack is provided.
- Supports clearing terminal, managing sessions, and handling user queries continuously.

## Requirements

- Python 3.8+
- `openai`
- `python-dotenv`

## Installation

```bash
pip install openai python-dotenv
```

## Environment Variables

Create a `.env` file in the root directory and add:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

## Usage

Run the assistant:

```bash
python your_script.py
```

Interact via the terminal:

- Type your query (e.g., "Create a tic tac toe game using HTML, CSS, and JS").
- Type `exit` to quit.
- Type `clear` to clear the terminal.

## Example Interaction

```
Enter your query >> : Create a calculator app using HTML, CSS, JavaScript
🧠 plan : user is interested in creating a calculator app using html, css and javascript
🧠 action : create_directory calculator
🧠 observe : calculator directory created successfully
...
✅ output : calculator app created successfully
```

## Available Tools

The assistant uses these tools internally:

- `create_file`, `remove_file`, `create_directory`, `remove_directory_tree`, etc.
- `move`, `copy_file`, `copy_directory`, `rename`
- `run_system_command`, `clear_terminal_unix`, `clear_terminal_windows`
- `get_current_directory`, `change_directory`, `get_file_stats`, `path_exists`
- ...and more.

Each tool has proper error handling and description-based mapping for clarity.

---

Developed as a part of a smart assistant framework that automates web development with interactive user input and real-time file system operations.
