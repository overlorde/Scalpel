""" The module provides utility functions such as finding all the files with specified flag (i.e., py files) and checking python extensions. """

import ast
import builtins
import operator
import sys 
import os


# scan a folder recurisively and return all files ending with the flag
def get_path_by_ext(root_dir, flag=".py"):
    paths = []
    for root, dirs, files in os.walk(root_dir):
        files = [
            f for f in files if not f[0] == "."
        ]  # skip hidden files such as git files
        dirs[:] = [d for d in dirs if not d[0] == "."]
        for f in files:
            if f.endswith(flag):
                paths.append(os.path.join(root, f))
    return paths

def check_python_version():
    """check Python version"""
    # Check for known bad Python versions.
    if sys.version_info[:2] < (3, 9):
        sys.exit("Running Scalpel with Python 3.8 or lower is not supported; ")


# Since Python 3.8 the parser folds every literal into ast.Constant. The old
# specialised nodes (ast.Num, ast.Str, ast.Bytes, ast.NameConstant) only lived
# on as deprecated aliases and were removed in Python 3.14, so the predicates
# below replace isinstance checks against those classes. type() is compared
# instead of isinstance so that booleans do not count as numbers, matching the
# behaviour of the removed aliases.

def is_num_node(node):
    """Old ast.Num: an int, float or complex literal."""
    return isinstance(node, ast.Constant) and type(node.value) in (int, float, complex)


def is_str_node(node):
    """Old ast.Str: a string literal."""
    return isinstance(node, ast.Constant) and type(node.value) is str


def is_bytes_node(node):
    """Old ast.Bytes: a bytes literal."""
    return isinstance(node, ast.Constant) and type(node.value) is bytes


def is_singleton_node(node):
    """Old ast.NameConstant: True, False or None."""
    return isinstance(node, ast.Constant) and type(node.value) in (bool, type(None))

