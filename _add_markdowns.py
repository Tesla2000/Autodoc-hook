from __future__ import annotations

from pathlib import Path

additional_documents_header = """Additional Documentation
------------------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:"""


def add_markdowns():
    def _conv2ref(markdown_file_path: Path) -> str:
        return str(markdown_file_path.relative_to(source_path).with_suffix(""))

    source_path = Path("docs/source")
    for file in source_path.glob("*.rst"):
        if file.name in ("index.rst", "modules.rst"):
            continue
        content = file.read_text()
        before, _, after = content.rpartition(additional_documents_header)
        before = (before or after).rstrip()
        documentation_path = "/".join(file.name.split(".")[:-1])
        markdown_files = source_path.joinpath(documentation_path).rglob("*.md")
        indent = 3 * " "
        additional_docs = f"\n{indent}".join(map(_conv2ref, markdown_files))
        file.write_text(
            "{}\n{}\n\n{}{}\n".format(
                before, additional_documents_header, indent, additional_docs
            )
        )


if __name__ == "__main__":
    add_markdowns()
