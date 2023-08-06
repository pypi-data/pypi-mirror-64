from functools import partial

import astroid
from pylint.checkers.variables import VariablesChecker
from pylint_plugin_utils import get_checker


orig_check_unused_args = VariablesChecker._check_unused_arguments


def patched_check_unused_args(self, name, node, stmt, argnames):
    if node.is_method():
        klass = node.parent.frame()
        if is_mutation_arg(node, klass, name) or is_resolver_arg(node, name):
            return

    return orig_check_unused_args(self, name, node, stmt, argnames)


def is_mutation_arg(node, klass, arg_name):
    return (
        "graphene.Mutation" in klass.basenames
        and node.name == "mutate"
        and arg_name in ("root", "info", "kwargs")
    )


def is_resolver_arg(node, arg_name):
    return node.name.startswith("resolve_") and arg_name in ("info", "kwargs")


def register(linter):
    var_checker = get_checker(linter, VariablesChecker)
    var_checker._check_unused_arguments = partial(
        patched_check_unused_args, var_checker
    )


def transform(_):
    pass


astroid.MANAGER.register_transform(astroid.FunctionDef, transform)
