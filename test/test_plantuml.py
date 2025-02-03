import re
import requests



PLANTUML_URL = "http://localhost:9999/plantuml"

def getPlantumlText(text: str):
    code = []
    pattern = r'@startuml(.*?)@enduml'
    results = re.findall(pattern, text, flags=re.DOTALL)


    for i, result in enumerate(results):
        print(f"第 {i+1} 个匹配项:")
        print(result.strip())
        print("\n")
        code.append(f'@startuml\n{result.strip()}\n@enduml')
    return code

def getPlantumlCoder(src: str):
    url = f'{PLANTUML_URL}/coder'
    headers = {
        'Content-Type': 'text/plain',
    }

    response = requests.post(url, headers=headers, data=src)
    if(response.status_code == 200):
        return response.text
    print(response)
    return None
    
def getPlantumlPng(data: str):
    url = f'{PLANTUML_URL}/png/{data}'
    headers = {
    }

    response = requests.get(url, headers=headers)
    if(response.status_code == 200):
        return response.text
    print(response)
    return None

def getPlantumlPngUrl(src: str):
    return f'http://localhost:9999/plantuml/png/{getPlantumlCoder(src)}'


def getPlantumlMd(src: str):
    return f'![plantuml](http://localhost:9999/plantuml/png/{getPlantumlCoder(src)})'


if __name__ == "__main__":
    text = """
    xxxxxx
    ...
    @startuml
    Bob -> Alice : hello
    @enduml
    xxxxx
    xxxxx
    @startuml
    Alice -> Bob : hello
    Alice -> joker : world
    @enduml
    xxxxx
    """
    for src in getPlantumlText(text):
        print(src)
        print(getPlantumlMd(src))
