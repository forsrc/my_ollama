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
