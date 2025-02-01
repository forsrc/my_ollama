from loguru import logger
from ollama import Client
from ollama import ChatResponse
import sys
from typing import Dict, Any, Callable


def add(a: int, b: int) -> int:
    result = a + b
    return result


def subtract(a: int, b: int) -> int:
    result = a - b
    return result


def multiply(a: int, b: int) -> int:
    return a * b


def divide(a: int, b: int) -> int:
    return a / b


def main(query: str):
    add_tool = {
        "type": "function",
        "function": {
            "name": "add",
            "description": "add 2 numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer", "description": "first integer"},
                    "b": {"type": "integer", "description": "second integer"},
                },
            },
        },
    }

    subtract_tool = {
        "type": "function",
        "function": {
            "name": "subtract",
            "description": "subtract 2 numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer", "description": "first integer"},
                    "b": {"type": "integer", "description": "second integer"},
                },
            },
        },
    }

    multiply_tool = {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "multiply 2 numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer", "description": "first integer"},
                    "b": {"type": "integer", "description": "second integer"},
                },
            },
        },
    }

    divide_tool = {
        "type": "function",
        "function": {
            "name": "divide",
            "description": "divide 2 numbers",
            "parameters": {
                "type": "object",
                "required": ["a", "b"],
                "properties": {
                    "a": {"type": "integer", "description": "first integer"},
                    "b": {"type": "integer", "description": "second integer"},
                },
            },
        },
    }

    messages = [{"role": "user", "content": query}]
    logger.info(f'\tquery: {messages[0]["content"]}')

    available_functions: Dict[str, Callable] = {
        "add": add,
        "subtract": subtract,
        "multiply": multiply,
        "divide": divide,
    }

    try:
        client = Client(host = "http://localhost:11434")

        response: ChatResponse = client.chat(
            "qwen2.5:1.5b",
            messages = messages,
            tools = [add_tool, subtract_tool, multiply_tool, divide_tool],
        )

        if response.message.tool_calls:
            for tool in response.message.tool_calls:
                if function_to_call := available_functions.get(tool.function.name):
                    output = function_to_call(**tool.function.arguments)
                else:
                    logger.warning(f"\tfuntion {tool.function.name} not found")

            messages.append(response.message)
            messages.append(
                {"role": "tool", "content": str(output), "name": tool.function.name}
            )

            final_response = client.chat("qwen2.5:1.5b", messages=messages)
            logger.success(f"\t{final_response.message.content}")

        else:
            logger.warning("no tool_calls")

    except Exception as e:
        logger.error(f"\tError: {str(e)}")
        raise


if __name__ == "__main__":
    main("11111111加77777777等于？")
    main("10000减去1等于？")
    main("9乘以9等于？")
    main("9除以3等于？")
