# main.py

import ollama
import json
import re
from src.average_tool import calculate_average
from src.average_tool import calculate_average_tools
from src.sum_tool import calculate_sum
from src.sum_tool import calculate_sum_tools


TOOLS = {"calculate_average": calculate_average, "calculate_sum": calculate_sum}


def main(questions: any):
    results = []

    for question in questions:
        response = ollama.chat(
            model="llama3.2", messages=[{"role": "user", "content": question}]
        )
        result_entry = {}

        response = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": question}],
            tools=[calculate_average_tools, calculate_sum_tools],
        )

        tool_calls = response.get("message", {}).get("tool_calls", [])
        for tool_call in tool_calls:
            tool_name = tool_call.get("function").get("name")
            args = tool_call.get("function").get("arguments", {})
            func = TOOLS.get(tool_name, None)
            if not func:
                print(f"[E] Tool {tool_name} not recognized")
                continue
            param_value = args.get("numbers", "")
            result_entry["numbers"] = param_value
            param_numbers = json.loads(param_value)
            try:
                result = func(param_numbers)
                result_entry[tool_name] = json.loads(result)
            except Exception as e:
                print(f"[E] Error processing tool {tool_name}: {e}")

        results.append(result_entry)

    print(results)


if __name__ == "__main__":
    questions = [
        "What is the average and sum of [1, 2, 3, 4, 5]?",
        "What is the average and sum of [6, 7, 8, 9, 10]?",
    ]
    main(questions)
