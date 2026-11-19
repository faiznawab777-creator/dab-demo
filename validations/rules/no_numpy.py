import ast


def _is_numpy(name):
    return name == "numpy" or name.startswith("numpy.")


def _get_full_attr_chain(node):

    parts = []

    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value

    if isinstance(node, ast.Name):
        parts.append(node.id)

    return ".".join(reversed(parts))


def validate(file_path, tree):

    violations = []

    for node in ast.walk(tree):

        # ---------------------------------------------
        # import numpy
        # ---------------------------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                if _is_numpy(alias.name):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Numpy import is not allowed."
                        )
                    )

        # ---------------------------------------------
        # from numpy import ...
        # ---------------------------------------------

        elif isinstance(node, ast.ImportFrom):

            if node.module and _is_numpy(node.module):

                violations.append(
                    (
                        file_path,
                        node.lineno,
                        "Numpy import is not allowed."
                    )
                )

        # ---------------------------------------------
        # Function Calls
        # ---------------------------------------------

        elif isinstance(node, ast.Call):

            call_name = None

            if isinstance(node.func, ast.Name):

                call_name = node.func.id

            elif isinstance(node.func, ast.Attribute):

                call_name = _get_full_attr_chain(node.func)

                # np.*
                # numpy.*

                if (
                    call_name.startswith("np.")
                    or call_name.startswith("numpy.")
                ):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            f"NumPy API '{call_name}' is not allowed."
                        )
                    )

            # Dynamic imports

            if call_name in ("importlib.import_module", "import_module"):

                if (
                    node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and _is_numpy(node.args[0].value)
                ):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Dynamic import of numpy is not allowed."
                        )
                    )

            elif call_name == "__import__":

                if (
                    node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and _is_numpy(node.args[0].value)
                ):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Dynamic import of numpy is not allowed."
                        )
                    )

    return violations