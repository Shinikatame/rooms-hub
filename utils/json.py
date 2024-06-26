from json import load, dump

def json_load(json_path: str) -> dict | list:
    with open(json_path, 'r') as file:
        return load(file)


def json_dump(json_path: str, data: dict | list) -> None:
    with open(json_path, 'w') as file:
        dump(data, file, indent = 4)