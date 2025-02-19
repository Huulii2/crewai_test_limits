# Contents:
- [Tool](#tool)
    - [Custom Caching](#custom-caching)
    - [StructuredTool](#structuredtool)
    - [Forcing Tool Output as Result](#forcing-tool-output-as-result)

---
---

# Tool

## Custom Caching
 - Caching is on by default
 - Determines when to cache results based on specific conditions
    - optimizes performance
    - reduce redundant operations

```python
from crewai.tools import tool

@tool
def multiplication_tool(first_number: int, second_number: int) -> int:
    """Useful for when you need to multiply two numbers together."""
    result = first_number * second_number
    print(f"Multiplication Result: {result} (Checking Cache)")
    return result

def cache_func(args, result):
    cache = result % 2 == 0  # Cache only even results
    print(f"Cache Status: {'Cached ✅' if cache else 'Not Cached ❌'} (Result: {result})")
    return cache

multiplication_tool.cache_function = cache_func
```
- This tool will only cache data if the result is even

## StructuredTool
Using StructuredTool.from_function, you can wrap a function that interacts with an external API or system, providing a structured interface. This enables robust  
validation and consistent execution, making it easier to integrate complex functionalities into your applications as demonstrated in the following example:  

```python
from crewai.tools.structured_tool import CrewStructuredTool
from pydantic import BaseModel

# Define the schema for the tool's input using Pydantic
class APICallInput(BaseModel):
    endpoint: str
    parameters: dict

# Wrapper function to execute the API call
def tool_wrapper(*args, **kwargs):
    # Here, you would typically call the API using the parameters
    # For demonstration, we'll return a placeholder string
    return f"Call the API at {kwargs['endpoint']} with parameters {kwargs['parameters']}"

# Create and return the structured tool
def create_structured_tool():
    return CrewStructuredTool.from_function(
        name='Wrapper API',
        description="A tool to wrap API calls with structured input.",
        args_schema=APICallInput,
        func=tool_wrapper,
    )

# Example usage
structured_tool = create_structured_tool()

# Execute the tool with structured input
result = structured_tool._run(**{
    "endpoint": "https://example.com/api",
    "parameters": {"key1": "value1", "key2": "value2"}
})
print(result)  # Output: Call the API at https://example.com/api with parameters {'key1': 'value1', 'key2': 'value2'}
```

## Forcing Tool Output as Result
```python
@agent
def blog_writer(self) -> Agent:
    return Agent(
        ...
        tools=[MyCustomTool(result_as_answer=True)]
        ...
    )
```