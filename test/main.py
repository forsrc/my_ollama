# main.py

import ollama
import json
import re
from src.average_tool import calculate_average
from src.sum_tool import calculate_sum


tools = {
    'calculate_average': calculate_average,
    'calculate_sum': calculate_sum
}

questions = [
    "What is the average and sum of [1, 2, 3, 4, 5]?",
    "What is the average and sum of [6, 7, 8, 9, 10]? max is ?",

]

def extract_numbers(text):
    match = re.search(r'\[(.*?)\]', text)
    if match:
        try:
            numbers = list(map(int, match.group(1).split(',')))
            return numbers
        except ValueError:
            return []
    return []


for question in questions:
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': question}]
    )

    response_content = response.get('message', {}).get('content', '')
    numbers = extract_numbers(question)

    result_dict = {
        "number": numbers,
        "calculate_average": json.loads(calculate_average(numbers)),
        "calculate_sum": json.loads(calculate_sum(numbers))
    }

    print(json.dumps(result_dict, indent=2))

"""
{
  "number": [
    1,
    2,
    3,
    4,
    5
  ],
  "calculate_average": {
    "average": 3.0
  },
  "calculate_sum": {
    "sum": 15
  }
}
"""