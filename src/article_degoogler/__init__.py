"""Article De-Googler package."""

__all__ = ["clean_href", "process_html", "process_file", "main", "__version__"]

from .fix_links import clean_href, process_html, process_file, main

__version__ = "0.1.1"
