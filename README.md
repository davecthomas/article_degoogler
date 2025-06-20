# Article De-Googler

`article-degoogler` cleans up exported HTML files by removing Google-injected
redirect links. It walks a directory tree, rewriting links in any `.html` or
`.htm` file so that they point directly at their targets. Links that lead away
from the current page are updated so they open in a new browser tab. The
distribution provides a standard `article_degoogler` Python package exposing a
`__version__` attribute.

## Installation

The project uses a standard `pyproject.toml` and can be installed with either
`pip` or `poetry`.

### Using pip

Create a virtual environment and install the package:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
```

### Using Poetry

```bash
poetry install
```

## Command-line usage

After installation the `fix-links` command will be available. Provide a
directory containing exported HTML files and each file will be processed in
place. While running, the command prints the path of each file being fixed and
how many links were rewritten. Once all files are processed it prints
``complete``.

```bash
fix-links path/to/exported-html
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for
more information.
