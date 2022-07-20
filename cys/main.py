import glob
import os
import subprocess
import sys
from typing import Optional
from pathlib import Path

import typer
from rich.console import Console

from cys.reader import line_grater
from cys.alt import AbstractLineTreeManager
from cys.states import LineContext, Begin
from cys.generator import generate

basic_template_header = """#include <stdio.h>
#include <stdlib.h>
"""

template_main = """

int main(void):

    return 0
"""

path = Path.cwd()

app = typer.Typer()

err_console = Console(stderr=True)


@app.callback()
def callback():
    """
    C Y Semicolon - C without {;}
    """


def abstract_line_tree_build(codeline_dict: dict) -> LineContext:
    line_tree = AbstractLineTreeManager()
    line_context = LineContext(Begin(), line_tree)
    for line_num in range(1, int(len(codeline_dict)) + 1):
        line_context.insert_line(codeline_dict[line_num], line_num)
    return line_context


@app.command()
def new(project_name: str, math: bool = False, string: bool = False):
    """
    Create  CYS project directory.
    """
    global path
    path = path / project_name
    try:
        path.mkdir()
    except:
        err_console.print(f"{project_name} already exists!\nPlease check!")
        raise typer.Exit()
    try:
        path = path / "main.cy"
        template_f = path.open("w+t", encoding="utf-8")
    except:
        raise typer.Exit()
    template_f.write(basic_template_header)
    if string:
        template_f.write("#include <string.h>\n")
    if math:
        template_f.write("#include <math.h>\n")
    template_f.write(template_main)
    template_f.close()

@app.command()
def translate(filename: str):
    """
    Translate .cy files only.
    """
    try:
        code_dict = line_grater(filename)
    except FileNotFoundError:
        err_console.print(".cy file does not exist!\nPlease check your path!")
        raise typer.Exit(code=2)
    line_context = abstract_line_tree_build(code_dict)
    result = generate("c", line_context, code_dict)
    result.close(path, filename[:-1])


@app.command()
def build(filename: str, math: bool = False):
    """
    Translate .cy files and compile output(*.out) using gcc.
    """
    translate(filename)
    source_name: str = filename[:-1]
    gcc_command: str = f"gcc {source_name} -o {source_name[:-2]}.out"
    if math:
        gcc_command += " -lm"
    build_process = subprocess.Popen(
        gcc_command, shell=True, stdout=subprocess.PIPE, encoding="utf-8"
    )
    while True:
        output = build_process.stdout.readline()
        if output == "" and build_process.poll() is not None:
            break
        if output:
            print(output.strip())


@app.command()
def run(filename: str, math: bool = False):
    """
    Build .cy files and run result(.out file)
    """
    out_name: str = filename[:-2] + "out"
    build(filename, math)
    run_process = subprocess.Popen(
        f"./{out_name}", shell=True, stdout=subprocess.PIPE, encoding="utf-8"
    )
    while True:
        output = run_process.stdout.readline()
        if output == "" and run_process.poll() is not None:
            break
        if output:
            print(output.strip())


if __name__ == "__main__":
    app()
