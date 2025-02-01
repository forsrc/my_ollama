import ollama
import re
import json


def calculate_average(numbers):
    if not isinstance(numbers, list) or not numbers:
        return json.dumps({"error": "Invalid input, expected a non-empty list of numbers"})

    try:
        avg = sum(numbers) / len(numbers)
        return json.dumps({"average": avg})
    except Exception as e:
        return json.dumps({"error": str(e)})
    
def calculate_sum(numbers):
    if not isinstance(numbers, list):
        return json.dumps({"error": "Invalid input, expected a list of numbers"})
    
    if not all(isinstance(x, (int, float)) for x in numbers):
        return json.dumps({"error": "List must contain only numbers"})

    try:
        return json.dumps({"sum": sum(numbers)})
    except Exception as e:
        return json.dumps({"error": str(e)})

calculate_average_tools = {
        "type": "function",
        "function": {
            "name": "calculate_average",
            "description": "Calculate the average of a list of numbers",
            "parameters": {
                "numbers": {
                "type": "array",
                "description": "A list of numbers"
                }
            },
        },
    }

calculate_sum_tools = {
        "type": "function",
        "function": {
            "name": "calculate_sum",
            "description": "Calculate the sum of a list of numbers",
            "parameters": {
                "numbers": {
                "type": "array",
                "description": "A list of numbers"
                }
            },
        },
    }


TOOLS = {
    'calculate_average': calculate_average,
    'calculate_sum': calculate_sum
}

question_to_tool_args = {
    "calculate_average": {"numbers"},
    "calculate_sum": {"numbers"}
}

questions = [
    "What is the average and sum of [1, 2, 3, 4, 5]?",
    "What is the average and sum of [6, 7, 8, 9, 10]?"
]

def extract_numbers(question):
    numbers = re.findall(r'\d+', question)
    return [int(num) for num in numbers]

results = []

for question in questions:
    numbers = extract_numbers(question)
    print(f"\nInput numbers: {numbers}")
    
    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': question}],
        tools = [calculate_average_tools, calculate_sum_tools],
    )
    
    tool_calls = response.get('message', {}).get('tool_calls', [])

    result_entry = {"numbers": numbers}
    
    print(f"[I] tool_calls: {tool_calls}")

    for tool_call in tool_calls:
        tool_name = tool_call.get("function").get("name")
        args = tool_call.get("function").get("arguments", {})
        
        print(f"[I] tool_name: {tool_name}, args: {args}")

        
        if tool_name not in question_to_tool_args:
            continue
            
        required_args = question_to_tool_args[tool_name]
        missing_args = [arg for arg in required_args if arg not in args]
        #print(f"required_args: {required_args}, missing_args: {missing_args}")

        if missing_args:
            print(f"[E] Missing arguments: {missing_args} for tool {tool_name}")
            continue
        
        param_value = args.get('numbers', '')
        if isinstance(param_value, str):
            try:
                param_numbers = json.loads(param_value)
            except json.JSONDecodeError:
                param_numbers = []
        else:
            param_numbers = param_value
        
        if not param_numbers:
            print(f"[E] No numbers found in tool arguments for {tool_name}")
            continue
        
        func = TOOLS.get(tool_name, None)
        if not func:
            print(f"[E] Tool {tool_name} not recognized")
            continue
        
        try:
            result = func(param_numbers)
            result_entry[tool_name] = json.loads(result)
        except Exception as e:
            print(f"[E] Error processing tool {tool_name}: {e}")
    
    results.append(result_entry)

print(results)
#print(json.dumps(results, indent=2))
