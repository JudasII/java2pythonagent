from smolagents import tool

from pathlib import Path

@tool
def iotool():
    """Dummy IO tool"""
    pass

@tool
def readfile(filepath:str) -> str:
    """
    Placeholder I/O tool.
    Args:
        filepath (str): Path to the file to read.
    """
    return Path(filepath).read_text()
@tool
def usefulliotool():
    """tool to read file"""
    raise RuntimeError("Filesystem access disabled")

@tool
def writefile(python_code: str) -> str:
    """
    Writes translated Python code to disk.
    Args:
        python_code (str): Python source code.
    """
    print("using tool to write the python code:", python_code)
    write_python_file("../outputs/output.py", python_code)
    return "success"

def extract_code_block(text: str) -> str:
    start = text.find("<code>")
    end = text.find("</code>")

    if start == -1 or end == -1:
        raise ValueError("No <code> block found")

    return text[start + 6 : end].strip()
def write_python_file(path: str, code: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)