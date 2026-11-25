import ast


def validate(file_path, tree):

    violations = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id == "display":

                    violations.append(
                        (
                            file_path,
                            node.lineno,
                            "display() is not allowed."
                        )
                    )

    return violations