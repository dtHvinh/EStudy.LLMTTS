import os
from typing import List, Dict, Any


def read_prompt(file_path: str) -> str:
    """
    Read prompt content from a file.

    Args:
        file_path (str): Path to the prompt file

    Returns:
        str: Content of the prompt file

    Raises:
        FileNotFoundError: If the file doesn't exist
        IOError: If there's an error reading the file
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Prompt file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as file:
            prompt_content = file.read().strip()

        if not prompt_content:
            raise ValueError(f"Prompt file is empty: {file_path}")

        return prompt_content

    except FileNotFoundError:
        raise
    except Exception as e:
        raise IOError(f"Error reading prompt file {file_path}: {str(e)}")


def load_prompt_to_messages(
    messages: List[Dict[str, Any]], prompt_name: str
) -> List[Dict[str, Any]]:
    """
    Load a prompt file and add it as a system message to the messages list.

    Args:
        messages (List[Dict[str, Any]]): List of existing messages
        prompt_name (str): Name of the prompt file (without .md extension)

    Returns:
        List[Dict[str, Any]]: Updated messages list with system prompt

    Raises:
        FileNotFoundError: If the prompt file doesn't exist
        ValueError: If prompt_name is empty or invalid
    """
    if not prompt_name or not prompt_name.strip():
        raise ValueError("Prompt name cannot be empty")

    # Sanitize prompt name to prevent path traversal
    prompt_name = (
        prompt_name.strip().replace("..", "").replace("/", "").replace("\\", "")
    )

    prompt_file_path = f"prompts/{prompt_name}.md"
    prompt_content = read_prompt(prompt_file_path)

    system_message = {"role": "system", "content": prompt_content}

    # Insert system message at the beginning if no system message exists,
    # or replace existing system message
    if messages and messages[0].get("role") == "system":
        messages[0] = system_message
    else:
        messages.insert(0, system_message)

    return messages


def set_prompt_to_messages(
    messages: List[Dict[str, Any]], prompt: str, defaultPrompt: str = "Lexa"
) -> List[Dict[str, Any]]:
    """
    Set a prompt file and add it as a system message to the messages list.

    Args:
        messages (List[Dict[str, Any]]): List of existing messages
        prompt (str): Content of the prompt

    Returns:
        List[Dict[str, Any]]: Updated messages list with system prompt
    """
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    defaultPromptContent = read_prompt(f"prompts/{defaultPrompt}.md")

    system_message = {"role": "system", "content": prompt + defaultPromptContent}

    # Insert system message at the beginning if no system message exists,
    # or replace existing system message
    if messages and messages[0].get("role") == "system":
        messages[0] = system_message
    else:
        messages.insert(0, system_message)

    return messages
