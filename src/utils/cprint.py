import os

from termcolor import colored


def cprint(text, color=None, indent=0, newline=False):
    text = f" {text}"
    if indent:
        text = f" {text}"
        for _ in range(indent):
            text = f"  {text}"
    if newline:
        text = f"\n{text}"
    colored_text = colored(text, color)
    print(colored_text)


def cprint_header():
    terminal_size = os.get_terminal_size()
    terminal_width = terminal_size.columns
    title = "Smoluchowski Coagulation Solver"
    title = f"{title} " if len(title) % 2 != 0 else title
    pad = 2
    a = (terminal_width - 2*pad - 2)
    b = int((a - len(title))/2)
    c = pad * ' '
    d = b * ' '
    e = a * '─'
    f = " " if terminal_width % 2 != 0 else ""
    text = "\n"
    text += f"{c}╭{e}╮{c}\n"
    text += f"{c}│{d}{f}{title}{d}│{c}\n"
    text += f"{c}╰{e}╯{c}"
    colored_text = colored(text, "blue")
    print(colored_text)
