import ast


def validate(file_path, tree):

    violations = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Attribute):

                if node.func.attr == "toPandas":

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "toPandas() is not allowed."
                        )
                    )

    return violations