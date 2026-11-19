import ast


DATAFRAME_APIS = {
    "groupby",
    "merge",
    "join",
    "sort_values",
    "sort_index",
    "fillna",
    "dropna",
    "rename",
    "assign",
    "apply",
    "applymap",
    "transform",
    "rolling",
    "expanding",
    "resample",
    "describe",
    "info",
    "to_csv",
    "to_excel",
    "pivot",
    "pivot_table"
}


def _is_pandas(name):
    return name == "pandas" or name.startswith("pandas.")


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

        # --------------------------------------------------
        # import pandas
        # --------------------------------------------------

        if isinstance(node, ast.Import):

            for alias in node.names:

                if _is_pandas(alias.name):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Pandas import is not allowed."
                        )
                    )

        # --------------------------------------------------
        # from pandas import ...
        # --------------------------------------------------

        elif isinstance(node, ast.ImportFrom):

            if node.module and _is_pandas(node.module):

                violations.append(
                    (
                        file_path,
                        node.lineno,
                        "Pandas import is not allowed."
                    )
                )

        # --------------------------------------------------
        # Function Calls
        # --------------------------------------------------

        elif isinstance(node, ast.Call):

            call_name = None

            if isinstance(node.func, ast.Name):

                call_name = node.func.id

            elif isinstance(node.func, ast.Attribute):

                call_name = _get_full_attr_chain(node.func)

                # pd.read_csv()
                # pd.DataFrame()
                # pd.merge()

                if call_name.startswith("pd."):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            f"Pandas API '{call_name}' is not allowed."
                        )
                    )

                # df.groupby()
                # df.fillna()

                if node.func.attr in DATAFRAME_APIS:

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            f"DataFrame API '{node.func.attr}()' is not allowed."
                        )
                    )

            # Dynamic imports

            if call_name in ("importlib.import_module", "import_module"):

                if (
                    node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and _is_pandas(node.args[0].value)
                ):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Dynamic import of pandas is not allowed."
                        )
                    )

            elif call_name == "__import__":

                if (
                    node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                    and _is_pandas(node.args[0].value)
                ):

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "Dynamic import of pandas is not allowed."
                        )
                    )

    return violations