# src/average_tool.py


import json

def calculate_average(numbers):
    if not isinstance(numbers, list) or not numbers:
        return json.dumps({"error": "Invalid input, expected a non-empty list of numbers"})

    try:
        avg = sum(numbers) / len(numbers)
        return json.dumps({"average": avg})
    except Exception as e:
        return json.dumps({"error": str(e)})

calculate_average_tools = {
        "type": "function",
        "function": {
            "name": "calculate_average",
            "description": "Calculate the average of a list of numbers, The args must named 'numbers'",
            "parameters": {
                "numbers": {
                "type": "array",
                "description": "A list of numbers, must named 'numbers'"
                }
            },
        },
    }