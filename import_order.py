import os


def get_import_order(module_name, visited=None):
    if visited is None:
        visited = set()

    if module_name not in visited:
        visited.add(module_name)
        module_path = module_name + ".py"

        # Check if the module file exists
        if os.path.isfile(module_path):
            with open(module_path, "r") as f:
                lines = f.readlines()

                # Extract import statements and process them
                for line in lines:
                    if line.startswith("from ") or line.startswith("import "):
                        parts = line.split()
                        imported_module_name = parts[1]
                        if imported_module_name != "__future__":
                            # Ignore __future__ imports
                            get_import_order(imported_module_name, visited)

    return list(visited)


# Start with the top-level module you are interested in (a.py in this case)
start_module = r"pybattle\screen\frames\frame"
import_order = get_import_order(start_module)

for i, module in enumerate(import_order):
    print(f"{i + 1}: {module}")
