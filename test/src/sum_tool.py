# src/sum_tool.py

import json

def calculate_sum(numbers):
    if not isinstance(numbers, list):
        return json.dumps({"error": "Invalid input, expected a list of numbers"})
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        return json.dumps({"error": "List must contain only numbers"})

    try:
        return json.dumps({"sum": sum(numbers)})
    except Exception as e:
        return json.dumps({"error": str(e)})


calculate_sum_tools = {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Calculate the sum of a list of numbers, The args must named 'numbers'",
            "parameters": {
                "numbers": {
                "type": "array",
                "description": "A list of numbers, must named 'numbers'"
                }
            },
        },
    }