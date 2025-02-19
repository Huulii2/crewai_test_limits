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