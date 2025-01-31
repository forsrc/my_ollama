import json
import ollama
from src.average_tool import calculate_average
from src.sum_tool import calculate_sum
import re

# 定义工具
TOOLS = {
    'calculate_average': calculate_average,
    'calculate_sum': calculate_sum
}

# 定义问题
questions = [
    "What is the average and sum of [1, 2, 3, 4, 5]?",
    "What is the average and sum of [6, 7, 8, 9, 10]?",
]

def extract_numbers(question):
    """从问题中提取数值列表"""
    numbers = re.findall(r'\d+', question)
    return [int(num) for num in numbers]

results = []

for question in questions:
    numbers = extract_numbers(question)
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': question}]
    )
    
    tool_call = response.get('message', {}).get('tool_calls', [])
    
    if tool_call:
        result_entry = {"number": numbers}
        for tool in tool_call:
            tool_name = tool.get('name')
            tool_args = tool.get('args', {})
            if tool_name in TOOLS:
                tool_result = json.loads(TOOLS[tool_name](**tool_args))
                result_entry[tool_name] = tool_result
            else:
                result_entry[tool_name] = {"error": "Unknown tool"}
        results.append(result_entry)
    else:
        print(response['message']['content'])

print(json.dumps(results, indent=2))
