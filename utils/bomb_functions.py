def hi_bomb():
    """Bomb that prints "hi\""""
    print("hi")


def raise_bomb():
    """Bomb that raises error"""
    raise ValueError("Sorry But you were hacked")


def open_link():
    import webbrowser
    webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley')  # Go to example.com


def if_bomb():
    exec("if 3 > 2:\n    print(\"Hi\")\nelse:\n    print(\"ABA\")")


def normal_if_bomb():
    if 3 > 2:
        print("Hi")
    else:
        print("ABA")


def if_bomb_2():
    exec("""
    from random import randint\nrand = randint(0, 1)\nif rand:\n    print(\"Generated 1\")\nelse:\n    print(\"Generated 1\")\n\nfor i in range(1, 10):\n    print(i)\n    try:\n        a = 10 / i\n    except ZeroDivisionError:\n        a = 2\n
    """)


def example_not_more_256():
    print(
        "AAADDDDDDDDDDDDDDDDDDDDDDDDDDAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


def if_bomb_2_normal():
    from random import randint
    rand = randint(0, 1)
    if rand:
        print("Generated 1")
    else:
        print("Generated 0")
    for i in range(1, 10):
        print(f"Current i:{i}")
        try:
            b = 3
            print(b)
            a = 10 / (i - 5)
        except ZeroDivisionError:
            print("ZERO")
            a = 2


def self_report_bomb():
    """Bomb that prints self pickle opcodes"""
    import inspect
    import re
    import pickletools
    caller = inspect.stack()[1]
    var_names = re.findall("loads\((\w+)\)", "".join(caller.code_context))
    var_name = var_names[0] if var_names else None
    payload = caller.frame.f_locals.get(var_name)
    pickletools.dis(pickletools.optimize(payload)) if payload else None


def pic_bomb():
    """Bomb that opens an image with default image viewer"""
    import subprocess
    import urllib.request
    import os
    urllib.request.urlretrieve("https://i.ytimg.com/vi/XH0LEgrTvhY/hqdefault.jpg", "pic.jpg")
    cmd = "if xdg-open pic.jpg 2> /dev/null ; then \n\techo \"\" \nelse \n\topen pic.jpg \nfi"
    cmd = "pic.jpg" if os.name == "nt" else cmd
    subprocess.check_output(cmd, shell=True)


def swap_integers():
    import ctypes
    import sys

    def mutate(obj, new_obj):
        import ctypes
        import sys
        if sys.getsizeof(obj) != sys.getsizeof(new_obj):
            raise ValueError('objects must have same size')

        mem = (ctypes.c_byte * sys.getsizeof(obj)).from_address(id(obj))
        new_mem = (ctypes.c_byte * sys.getsizeof(new_obj)).from_address(id(new_obj))

        for i in range(len(mem)):
            mem[i] = new_mem[i]

    mutate(50, 100)
    mutate(40, 10)

