from pathlib import Path
import ast
import xml.etree.ElementTree as ET

# Analisa a pasta atual (onde o script está sendo executado)
ROOT = Path.cwd()

IGNORE = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    ".pytest_cache"
}

project = ET.Element("project")
project.set("root", str(ROOT))

def parse_python(file_element, text):
    try:
        tree = ast.parse(text)

        imports = ET.SubElement(file_element, "imports")
        classes = ET.SubElement(file_element, "classes")
        functions = ET.SubElement(file_element, "functions")

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):
                for n in node.names:
                    ET.SubElement(imports, "import", name=n.name)

            elif isinstance(node, ast.ImportFrom):
                ET.SubElement(
                    imports,
                    "import",
                    module=node.module if node.module else ""
                )

            elif isinstance(node, ast.ClassDef):
                ET.SubElement(
                    classes,
                    "class",
                    name=node.name,
                    line=str(node.lineno)
                )

            elif isinstance(node, ast.FunctionDef):
                ET.SubElement(
                    functions,
                    "function",
                    name=node.name,
                    line=str(node.lineno)
                )

    except Exception as e:
        file_element.set("python_error", str(e))


def scan_directory(parent_xml, directory):

    for item in sorted(directory.iterdir()):

        if item.name in IGNORE:
            continue

        if item.is_dir():

            dir_xml = ET.SubElement(
                parent_xml,
                "directory",
                name=item.name,
                path=str(item.relative_to(ROOT))
            )

            scan_directory(dir_xml, item)

        else:

            file_xml = ET.SubElement(
                parent_xml,
                "file",
                name=item.name,
                path=str(item.relative_to(ROOT)),
                extension=item.suffix
            )

            try:
                file_xml.set("size", str(item.stat().st_size))
            except:
                pass

            try:
                text = item.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                file_xml.set(
                    "lines",
                    str(len(text.splitlines()))
                )

                if item.suffix == ".py":
                    parse_python(file_xml, text)

            except Exception as e:
                file_xml.set("error", str(e))


scan_directory(project, ROOT)

tree = ET.ElementTree(project)
ET.indent(tree, space="    ")

tree.write(
    "project.xml",
    encoding="utf-8",
    xml_declaration=True
)

print("=" * 50)
print("Projeto :", ROOT)
print("XML     : project.xml")
print("=" * 50)