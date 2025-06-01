from dotenv import load_dotenv
import json
import shutil
from openai import OpenAI
import os

load_dotenv() 
ai = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"), 
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

client = OpenAI(
    api_key="GEMINI_API_KEY",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Tools | Agents

# Returns the current working directory
def get_current_directory():
    try:
        return os.getcwd()
    except Exception as E:
        return f"Error: {str(E)}"

# Changes the current working directory to the specified path
def change_directory(path):
    try:
        os.chdir(path)
        return f"Changed directory to {os.getcwd()}"
    except Exception as E:
        return f"Error: {str(E)}"

# Lists all files and folders in the given path (defaults to current directory)
def list_directory(path="."):
    try:
        return os.listdir(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Creates a single directory
def create_directory(directory_name):
    try:
        os.mkdir(directory_name)
        return f"{directory_name} created successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Creates nested directories (intermediate folders as needed)
def create_nested_directories(path):
    try:
        os.makedirs(path)
        return f"{path} created successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Removes a directory (only if it is empty)
def remove_empty_directory(path):
    try:
        os.rmdir(path)
        return f"{path} removed successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Removes a directory and its empty parent directories
def remove_nested_directories(path):
    try:
        os.removedirs(path)
        return f"{path} and its empty parents removed successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Creates an empty file
def create_file(filename, content=""):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"File '{filename}' created successfully with content."
    except Exception as E:
        return f"Error: {str(E)}"

# Removes/deletes a file
def remove_file(filename):
    try:
        os.remove(filename)
        return f"File '{filename}' removed successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Renames a file or directory from old name to new name
def rename(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return f"Renamed '{old_name}' to '{new_name}' successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Returns metadata/statistics about a file or directory
def get_file_stats(path):
    try:
        stats = os.stat(path)
        return stats
    except Exception as E:
        return f"Error: {str(E)}"

# Checks if a path exists (file or directory)
def path_exists(path):
    try:
        return os.path.exists(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Checks if the path is a file
def is_file(path):
    try:
        return os.path.isfile(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Checks if the path is a directory
def is_directory(path):
    try:
        return os.path.isdir(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Copies a file from source to destination
def copy_file(src, dst):
    try:
        shutil.copy(src, dst)
        return f"File copied from '{src}' to '{dst}' successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Recursively copies an entire directory from source to destination
def copy_directory(src, dst):
    try:
        shutil.copytree(src, dst)
        return f"Directory copied from '{src}' to '{dst}' successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Moves a file or directory from source to destination
def move(src, dst):
    try:
        shutil.move(src, dst)
        return f"Moved '{src}' to '{dst}' successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Deletes a directory and all its contents (files and subfolders)
def remove_directory_tree(path):
    try:
        shutil.rmtree(path)
        return f"Directory tree '{path}' deleted successfully"
    except Exception as E:
        return f"Error: {str(E)}"

# Runs any system command like 'ls', 'mkdir', 'clear', etc.
def run_system_command(command):
    try:
        exit_code = os.system(command)
        return f"Command '{command}' executed with exit code {exit_code}"
    except Exception as E:
        return f"Error: {str(E)}"

# Clears the terminal (Linux/macOS)
def clear_terminal_unix():
    try:
        os.system("clear")
        return "Terminal cleared (Unix/Linux/macOS)"
    except Exception as E:
        return f"Error: {str(E)}"

# Clears the terminal (Windows)
def clear_terminal_windows():
    try:
        os.system("cls")
        return "Terminal cleared (Windows)"
    except Exception as E:
        return f"Error: {str(E)}"

# Returns absolute path of the given path
def get_absolute_path(path):
    try:
        return os.path.abspath(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Splits a path into (head, tail)
def split_path(path):
    try:
        return os.path.split(path)
    except Exception as E:
        return f"Error: {str(E)}"

# Joins multiple path parts into one
def join_paths(*paths):
    try:
        return os.path.join(*paths)
    except Exception as E:
        return f"Error: {str(E)}"




# Dictionary mapping tool names to their function and descriptions
available_tools = {
    "get_current_directory": {
        "fn": get_current_directory,
        "description": "Returns the current working directory.",
    },
    "change_directory": {
        "fn": change_directory,
        "description": "Changes the current working directory to the given path.",
    },
    "list_directory": {
        "fn": list_directory,
        "description": "Lists files and directories in the given path. Defaults to current directory.",
    },
    "create_directory": {
        "fn": create_directory,
        "description": "Creates a single directory at the given path.",
    },
    "create_nested_directories": {
        "fn": create_nested_directories,
        "description": "Creates nested directories recursively.",
    },
    "remove_empty_directory": {
        "fn": remove_empty_directory,
        "description": "Removes an empty directory.",
    },
    "remove_nested_directories": {
        "fn": remove_nested_directories,
        "description": "Removes a directory and its empty parent directories recursively.",
    },
    "create_file": {
        "fn": create_file,
        "description": "Creates a file with the specified filename and optional content.",
    },
    "remove_file": {
        "fn": remove_file,
        "description": "Removes/deletes the specified file.",
    },
    "rename": {
        "fn": rename,
        "description": "Renames a file or directory from old name to new name.",
    },
    "get_file_stats": {
        "fn": get_file_stats,
        "description": "Returns metadata about a file or directory.",
    },
    "path_exists": {
        "fn": path_exists,
        "description": "Checks if the given path exists (file or directory).",
    },
    "is_file": {
        "fn": is_file,
        "description": "Checks if the given path is a file.",
    },
    "is_directory": {
        "fn": is_directory,
        "description": "Checks if the given path is a directory.",
    },
    "copy_file": {
        "fn": copy_file,
        "description": "Copies a file from source path to destination path.",
    },
    "copy_directory": {
        "fn": copy_directory,
        "description": "Recursively copies a directory from source path to destination path.",
    },
    "move": {
        "fn": move,
        "description": "Moves a file or directory from source to destination.",
    },
    "remove_directory_tree": {
        "fn": remove_directory_tree,
        "description": "Deletes a directory and all its contents (files and subfolders).",
    },
    "run_system_command": {
        "fn": run_system_command,
        "description": "Executes a system command using the OS shell (e.g., 'ls', 'mkdir'). ⚠️ Use with caution: executing arbitrary commands may be unsafe or harmful.",
    },
    "clear_terminal_unix": {
        "fn": clear_terminal_unix,
        "description": "Clears the terminal screen (Linux/macOS).",
    },
    "clear_terminal_windows": {
        "fn": clear_terminal_windows,
        "description": "Clears the terminal screen (Windows).",
    },
    "get_absolute_path": {
        "fn": get_absolute_path,
        "description": "Returns the absolute path of the given relative or absolute path.",
    },
    "split_path": {
        "fn": split_path,
        "description": "Splits the given path into (head, tail).",
    },
    "join_paths": {
        "fn": join_paths,
        "description": "Joins multiple path components into a single valid path.",
    },
}


# Generate system prompt with available tools
tool_descriptions = "\n".join(
    [f"- {name}: {info['description']}" for name, info in available_tools.items()]
)


system_prompt = f"""
    You are a very helpfull assistant, who is specialized in creating basic level to full stack website applications. Your task is to create a fully structured production ready web application based on user query and use available tools as require.
    You work on follwoing steps: plan -> action -> observe -> output
    
    Rules:
    - Follow the Output JSON Format.
    - Always perform one step at a time and wait for next input
    - Carefully analyse the user query
    - Use the available tools as per requirement
    - Always observe after action step
    - Maintain error handling
    - If the directory already exits, then use delete_directory from available tools, delete it and create new one
    - If user has not provided tech stack, use python by default and if its a website then use html, css and js as default 
    - On step output, provide the final output
    
    Output JSON Format:
    {{
        "step": "plan" | "action" | "observe" | "output"
        "content": "string",
        "function": "name of the function",
        "input": "input parameter for the function",
        "parameter": "number of parameter, function takes(if there is function name and type will be number)" 
    }}
    
    Available Tools:
    {tool_descriptions}
    Example : 
    User Query : Create a tic tac toe game using html, css and javascript
    Output: {{ "step": "plan", "content": "user is interested in creating a tic tac game by using tech stack html, css and javascript" }}
    Output: {{ "step": "action", "function": "create_directory", "input": "tic-tac-toe", "parameter": 1 }}
    Output: {{ "step": "observe", "content": "tic-tac-toe directory created successfully" }}
    Output: {{ "step": "action", "function": "change_directory", "input": "tic-tac-toe", "parameter": 1 }}
    Output: {{ "step": "observe", "content": "Working directory changed successfully" }}
    Output: {{ "step": "action", "function": "create_file", "input": "index.html", "file_content": "code for index.html", "parameter": 2 }}
    Output: {{ "step": "observe", "content": "index.html, style.css and script.js created successfully, everythings looks and project is ready to serve" }}
    Output: {{ "step": "output", "output": "tic tac toe game created successfully" }}
"""

messages = [{"role": "system", "content": system_prompt}]

print("Welcome to Cursore AI Assistant (type 'exit' to quit or 'clear' to clear terminal)")

while True: 
    user_input = input("Enter your query >> : ")
    messages.append({"role": "user", "content": user_input})
    
    if user_input.strip().lower() == "exit":
        print("Exiting Cursore AI Assistant. Goodbye!")
        break
    elif user_input.strip().lower() == "clear":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Terminal cleared.")
        continue
    print("Generating response...", os.getcwd())
    while True:
        response = ai.chat.completions.create(
            model="gemini-2.0-flash",
            messages=messages,
            response_format={"type": "json_object"}
        )
        parsed_output = json.loads(response.choices[0].message.content)
        messages.append({ "role": "assistant", "content": json.dumps(parsed_output) })

        step = parsed_output.get("step")
        if step == "plan" or step == "observe":
            print(f"🧠 {step} : {parsed_output.get("content")}")
            continue
        elif (step == "action"):
            func_name = parsed_output.get("function")
            tool_entry = available_tools.get(func_name)

            if not tool_entry:
                messages.append({"role": "assistant", "content": json.dumps(f"Tool '{func_name}' not found")})
                continue

            tool_func = tool_entry["fn"]

            # Try to get all inputs from parsed_output, preferring a list
            tool_args = parsed_output.get("input")
            
            # If `input` is not a list, treat as single parameter
            try:
                if tool_args is None:
                    # No arguments (like clear_terminal)
                    tool_output = tool_func()
                elif isinstance(tool_args, list):
                    kwargs = parsed_output.get("kwargs", {})
                    tool_output = tool_func(*tool_args, **kwargs)
                else:
                    second_arg = parsed_output.get("file_content")
                    if second_arg is not None:
                        tool_output = tool_func(tool_args, second_arg)
                    else:
                        tool_output = tool_func(tool_args)
            except Exception as e:
                tool_output = f"Error during tool execution: {e}"


            messages.append({"role": "assistant", "content": json.dumps(tool_output)})
            
            continue
                
        
        elif step == "output":
            print(f"✅ {step} : {parsed_output.get('content')}")
            break
        else: 
            print("Invalid input, please try again")
            break


