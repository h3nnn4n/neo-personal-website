from markdown import markdown


def load_markdown(filename: str) -> str:
    with open(filename, "rt") as f:
        return f.read()


def render_markdown(markdown_str: str):
    return markdown(markdown_str)
