import json
import os
from pydantic import BaseModel
from crewai.tools import tool
from typing import Dict, Any

DATA_FRUIT = "knowledge/fruits.json"
DATA_FRUIT_DETAILS = "knowledge/fruits_details.json"

class EditJSONInput(BaseModel):
    """Schema for editing JSON"""
    new_content: Dict[str, Any]  # Expecting a full JSON dictionary as input

@tool
def read_fruits_json() -> Dict[str, Any]:
    """
    Reads and returns the raw JSON content from fruits.json.
    This file contains the different types of fruits.
    If the file does not exist or is invalid, an empty dictionary is returned.
    """
    if not os.path.exists(DATA_FRUIT):
        return {}  # Return empty dictionary if file doesn't exist
    
    try:
        with open(DATA_FRUIT, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data  # Return as a raw JSON dictionary
    except json.JSONDecodeError:
        return {}  # Return empty dictionary if JSON is invalid

@tool
def read_fruits_details_json() -> Dict[str, Any]:
    """
    Reads and returns the raw JSON content from fruits_details.json.
    This file contains fruit names and their description.
    If the file does not exist or is invalid, an empty dictionary is returned.
    """
    if not os.path.exists(DATA_FRUIT_DETAILS):
        return {}  # Return empty dictionary if file doesn't exist
    
    try:
        with open(DATA_FRUIT_DETAILS, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data  # Return as a raw JSON dictionary
    except json.JSONDecodeError:
        return {}  # Return empty dictionary if JSON is invalid

@tool
def edit_fruits_json(new_content: Dict[str, Any]) -> str:
    """
    Overwrites fruits.json with new content provided by the agent.
    The new content must be valid JSON.
    """
    try:
        # Ensure content is valid JSON
        json.dumps(new_content)  # This checks if it's serializable
    except (TypeError, ValueError):
        return "Error: The provided content is not valid JSON."

    with open(DATA_FRUIT, "w", encoding="utf-8") as file:
        json.dump(new_content, file, ensure_ascii=False, indent=4)

    return "Successfully updated fruits.json with new content."

@tool
def edit_fruits_details_json(new_content: Dict[str, Any]) -> str:
    """
    Overwrites fruits_details.json with new content provided by the agent.
    The new content must be valid JSON.
    """
    try:
        # Ensure content is valid JSON
        json.dumps(new_content)  # This checks if it's serializable
    except (TypeError, ValueError):
        return "Error: The provided content is not valid JSON."

    with open(DATA_FRUIT_DETAILS, "w", encoding="utf-8") as file:
        json.dump(new_content, file, ensure_ascii=False, indent=4)

    return "Successfully updated fruits_details.json with new content."

@tool
def read_json(file_path: str) -> Dict[str, Any]:
    """
    Reads and returns the raw JSON content from the specified file.
    
    Args:
        file_path (str): The path of the JSON file to read.
        
    Returns:
        Dict[str, Any]: The JSON content as a dictionary, or an empty dict if the file does not exist or is invalid.
    """
    if not os.path.exists(file_path):
        return {}  # Return empty dictionary if file doesn't exist
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data  # Return as a raw JSON dictionary
    except json.JSONDecodeError:
        return {}  # Return empty dictionary if JSON is invalid
    
    
@tool
def edit_json(file_path: str, new_content: Dict[str, Any]) -> str:
    """
    Overwrites the specified JSON file with new content provided by the agent.
    
    Args:
        file_path (str): The path of the JSON file to overwrite.
        new_content (Dict[str, Any]): The new JSON content to write.
        
    Returns:
        str: Success or error message.
    """
    try:
        # Ensure content is valid JSON
        json.dumps(new_content)  # This checks if it's serializable
    except (TypeError, ValueError):
        return "Error: The provided content is not valid JSON."

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(new_content, file, ensure_ascii=False, indent=4)
        return f"Successfully updated {file_path} with new content."
    except Exception as e:
        return f"Error writing to file: {str(e)}"