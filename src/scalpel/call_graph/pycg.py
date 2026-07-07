"""
This file is a wrapper of the pycg, a practical python call graph generator. Please refer to:
1. https://github.com/vitsalis/PyCG
2. https://pypi.org/project/pycg/
3. Vitalis Salis, Thodoris Sotiropoulos, Panos Louridas, Diomidis Spinellis and Dimitris Mitropoulos. PyCG: Practical
Call Graph Generation in Python. In 43rd International Conference on Software Engineering, ICSE '21, 25–28 May 2021.
"""

import sys
import types
from importlib.metadata import version as distribution_version

from packaging.version import Version

try:
    import pkg_resources  # noqa: F401
except ModuleNotFoundError:
    # setuptools >= 81 no longer ships pkg_resources, but pycg still imports
    # it for its fasten output format. A minimal stand-in providing the one
    # name pycg uses keeps it importable on modern environments.
    from packaging.requirements import Requirement as _PackagingRequirement

    class _Requirement(_PackagingRequirement):
        @classmethod
        def parse(cls, line):
            return cls(line)

    _pkg_resources = types.ModuleType("pkg_resources")
    _pkg_resources.Requirement = _Requirement
    sys.modules["pkg_resources"] = _pkg_resources

# PyCG 0.0.7 renamed its import package from "pycg" to "PyCG", so both
# spellings have to be tried to support old and new releases alike.
try:
    import pycg
    from pycg import formats
    from pycg.pycg import CallGraphGenerator as CallGraphGeneratorPyCG
except ModuleNotFoundError:
    import PyCG as pycg
    from PyCG import formats
    from PyCG.pycg import CallGraphGenerator as CallGraphGeneratorPyCG

pycg_version = distribution_version("pycg")
if Version(pycg_version) > Version("0.0.3"):

    class CallGraphGenerator(CallGraphGeneratorPyCG):
        def __init__(self, entry_points, package, max_iter=-1, operation="call-graph"):
            super().__init__(entry_points, package, max_iter, operation)

    pycg.pycg.CallGraphGeneratorPyCG = CallGraphGenerator
