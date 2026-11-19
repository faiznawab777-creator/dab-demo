import ast

def validate(file_path, tree):

    violations = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            if isinstance(node.func, ast.Attribute):

                if node.func.attr == "collect":

                    violations.append(

                        (
                            file_path,
                            node.lineno,
                            "collect() is not allowed."

                        )

                    )

    return violations