"""
This is mostly compatible with pkginfo's metadata classes.
"""

import json
import logging
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Sequence, Tuple

import libcst as cst
import pkginfo.distribution
from libcst.metadata import ParentNodeProvider, QualifiedNameProvider, ScopeProvider

LOG = logging.getLogger(__name__)


# TODO: pkginfo isn't typed
class Distribution(pkginfo.distribution.Distribution):  # type: ignore
    # These are not actually part of the metadata, see PEP 566
    setup_requires: Sequence[str] = ()
    tests_require: Sequence[str] = ()
    extras_require: Dict[str, Sequence[str]] = {}
    use_scm_version: Optional[bool] = None
    zip_safe: Optional[bool] = None
    include_package_data: Optional[bool] = None
    test_suite: str = ""
    namespace_packages: Sequence[str] = ()

    def _getHeaderAttrs(self) -> Sequence[Tuple[str, str, bool]]:
        # Until I invent a metadata version to include this, do so
        # unconditionally.
        return tuple(super()._getHeaderAttrs()) + (
            ("Setup-Requires", "setup_requires", True),
            ("Tests-Require", "tests_require", True),
            ("???", "extras_require", False),
            ("Use-SCM-Version", "use_scm_version", False),
            ("Zip-Safe", "zip_safe", False),
            ("Test-Suite", "test_suite", False),
            ("Include-Package-Data", "include_package_data", False),
            ("Namespace-Package", "namespace_packages", True),
        )


# setup(kwarg=) -> Distribution key
MAPPING = {
    "name": "name",
    "version": "version",
    "author": "author",
    "author_email": "author_email",
    "maintainer": "maintainer",
    "maintainer_email": "maintainer_email",
    "license": "license",
    "description": "summary",
    "long_description": "description",
    "long_description_content_type": "description_content_type",
    "install_requires": "requires_dist",
    "requires": "requires",
    "python_requires": "requires_python",
    "url": "home_page",
    "download_url": "download_url",
    "project_urls": "project_urls",
    "keywords": "keywords",
    "license": "license",
    "platforms": "platforms",
    "use_scm_version": "use_scm_version",
    "setup_requires": "setup_requires",
    "tests_require": "tests_require",
    "extras_require": "extras_require",
    "classifiers": "classifiers",
    "zip_safe": "zip_safe",
    "test_suite": "test_suite",
    "include_package_data": "include_package_data",
    "namespace_packages": "namespace_packages",
}


def from_setup_py(path: Path, markers: Dict[str, Any]) -> Distribution:
    """
    Reads setup.py (and possibly some imports).

    Will not actually "run" the code but will evaluate some conditions based on
    the markers you provide, since much real-world setup.py checks things like
    version, platform, or even `sys.argv` to come up with what it passes to
    `setup()`.

    There should be some other class to read pyproject.toml.

    This needs a path because one day it may need to read other files alongside
    it.
    """

    # TODO: This does not take care of encodings or py2 syntax.
    module = cst.parse_module((path / "setup.py").read_text())

    # TODO: This is not a good example of LibCST integration.  The right way to
    # do this is with a scope provider and transformer, and perhaps multiple
    # passes.

    d = Distribution()
    d.metadata_version = "2.1"

    analyzer = SetupCallAnalyzer()
    wrapper = cst.MetadataWrapper(module)
    wrapper.visit(analyzer)
    if not analyzer.found_setup:
        raise SyntaxError("No simple setup call found")

    for k, v in analyzer.saved_args.items():
        if k in MAPPING:
            if isinstance(v, Literal):
                setattr(d, MAPPING[k], v.value)
            else:
                LOG.warning(f"Want to save {k} but is {type(v)}")
        else:
            LOG.warning(f"Specified {k} but we don't store it")

    return d


@dataclass
class TooComplicated:
    reason: str


@dataclass
class Sometimes:
    # TODO list of 'when' and 'else'
    pass


@dataclass
class Literal:
    value: Any
    cst_node: Optional[cst.CSTNode]


class FileReference:
    def __init__(self, filename: str) -> None:
        self.filename = filename


class SetupCallTransformer(cst.CSTTransformer):
    METADATA_DEPENDENCIES = (ScopeProvider, ParentNodeProvider, QualifiedNameProvider)  # type: ignore

    def __init__(
        self,
        call_node: cst.CSTNode,
        keywords_to_change: Dict[str, Optional[cst.CSTNode]],
    ) -> None:
        self.call_node = call_node
        self.keywords_to_change = keywords_to_change

    def leave_Call(
        self, original_node: cst.Call, updated_node: cst.Call
    ) -> cst.BaseExpression:
        if original_node == self.call_node:
            new_args = []
            for arg in updated_node.args:
                if isinstance(arg.keyword, cst.Name):
                    if arg.keyword.value in self.keywords_to_change:
                        value = self.keywords_to_change[arg.keyword.value]
                        if value is not None:
                            new_args.append(arg.with_changes(value=value))
                        # else don't append
                    else:
                        new_args.append(arg)
                else:
                    new_args.append(arg)
            return updated_node.with_changes(args=new_args)

        return updated_node


class SetupCallAnalyzer(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (ScopeProvider, ParentNodeProvider, QualifiedNameProvider)  # type: ignore

    # TODO names resulting from other than 'from setuptools import setup'
    # TODO wrapper funcs that modify args
    # TODO **args
    def __init__(self) -> None:
        super().__init__()
        # TODO Union[TooComplicated, Sometimes, Literal, FileReference]
        self.saved_args: Dict[str, Any] = {}
        self.found_setup = False
        self.setup_node: Optional[cst.CSTNode] = None

    def visit_Call(self, node: cst.Call) -> Optional[bool]:
        names = self.get_metadata(QualifiedNameProvider, node)
        # TODO sometimes there is more than one setup call, we might
        # prioritize/merge...
        if any(
            q.name in ("setuptools.setup", "distutils.core.setup", "setup3lib")
            for q in names
        ):
            self.found_setup = True
            self.setup_node = node
            scope = self.get_metadata(ScopeProvider, node)
            for arg in node.args:
                # TODO **kwargs
                if isinstance(arg.keyword, cst.Name):
                    key = arg.keyword.value
                    value = self.evaluate_in_scope(arg.value, scope)
                    self.saved_args[key] = Literal(value, arg)
                elif arg.star == "**":
                    # kwargs
                    d = self.evaluate_in_scope(arg.value, scope)
                    if isinstance(d, dict):
                        for k, v in d.items():
                            self.saved_args[k] = Literal(v, None)
                    else:
                        # GRR
                        pass
                else:
                    raise ValueError(repr(arg))

            return False

        return None

    BOOL_NAMES = {"True": True, "False": False, "None": None}
    PRETEND_ARGV = ["setup.py", "bdist_wheel"]

    def evaluate_in_scope(self, item: cst.CSTNode, scope: Any) -> Any:
        if isinstance(item, cst.SimpleString):
            return item.evaluated_value
        # TODO int/float/etc
        elif isinstance(item, cst.Name) and item.value in self.BOOL_NAMES:
            return self.BOOL_NAMES[item.value]
        elif isinstance(item, cst.Name):
            name = item.value
            assignments = scope[name]
            for a in assignments:
                # TODO: Only assignments "before" this node matter if in the
                # same scope; really if we had a call graph and walked the other
                # way, we could have a better idea of what has already happened.

                # Assign(
                #   targets=[AssignTarget(target=Name(value="v"))],
                #   value=SimpleString(value="'x'"),
                # )
                # TODO or an import...
                # TODO builtins have BuiltinAssignment
                try:
                    node = a.node
                    if node:
                        parent = self.get_metadata(ParentNodeProvider, node)
                        if parent:
                            gp = self.get_metadata(ParentNodeProvider, parent)
                        else:
                            raise KeyError
                    else:
                        raise KeyError
                except (KeyError, AttributeError):
                    return "??"

                # This presumes a single assignment
                if not isinstance(gp, cst.Assign) or len(gp.targets) != 1:
                    return "??"  # TooComplicated(repr(gp))

                try:
                    scope = self.get_metadata(ScopeProvider, gp)
                except KeyError:
                    # module scope isn't in the dict
                    return "??"

                return self.evaluate_in_scope(gp.value, scope)
        elif isinstance(item, (cst.Tuple, cst.List)):
            lst = []
            for el in item.elements:
                lst.append(
                    self.evaluate_in_scope(
                        el.value, self.get_metadata(ScopeProvider, el)
                    )
                )
            if isinstance(item, cst.Tuple):
                return tuple(lst)
            else:
                return lst
        elif (
            isinstance(item, cst.Call)
            and isinstance(item.func, cst.Name)
            and item.func.value == "dict"
        ):
            d = {}
            for arg in item.args:
                if isinstance(arg.keyword, cst.Name):
                    d[arg.keyword.value] = self.evaluate_in_scope(arg.value, scope)
                # TODO something with **kwargs
            return d
        elif isinstance(item, cst.Dict):
            d = {}
            for el2 in item.elements:
                if isinstance(el2, cst.DictElement):
                    d[self.evaluate_in_scope(el2.key, scope)] = self.evaluate_in_scope(
                        el2.value, scope
                    )
            return d
        elif isinstance(item, cst.Subscript):
            lhs = self.evaluate_in_scope(item.value, scope)
            if isinstance(lhs, str):
                # A "??" entry, propagate
                return "??"

            # TODO: Figure out why this is Sequence
            if isinstance(item.slice[0].slice, cst.Index):
                rhs = self.evaluate_in_scope(item.slice[0].slice.value, scope)
                return lhs.get(rhs, "??")
            else:
                LOG.warning(f"Omit2 {type(item.slice[0].slice)!r}")
                return "??"
        else:
            LOG.warning(f"Omit1 {type(item)!r}")
            return "??"


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    for path in sys.argv[1:]:
        try:
            dist = from_setup_py(Path(path), {})
            value = {
                "path": path,
            }

            for k in list(dist):
                if getattr(dist, k):
                    value[k] = getattr(dist, k)

            print(json.dumps(value, indent=2,))
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            print(f"Fail: {path}\n{e!r}", file=sys.stderr)


if __name__ == "__main__":
    main()
