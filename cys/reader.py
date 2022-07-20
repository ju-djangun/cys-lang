from dataclasses import dataclass


def read_source_file(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        source: str = f.read()
    return source

def split_line(source: str):
    line_dict: dict = {} # is dataclass better?
    codelines: list = str(source).splitlines()
    for line_no, line in enumerate(codelines):
        line_dict[line_no+1] = line.rstrip()
    return line_dict

def line_grater(filename: str) -> dict:
    source = read_source_file(filename)
    codeline_dict = split_line(source)
    return codeline_dict
