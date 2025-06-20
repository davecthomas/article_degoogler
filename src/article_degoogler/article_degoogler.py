import os
import re
import sys


def clean_href(url: str) -> str:
    """Remove Google redirect prefix and trailing ``&sa=`` parameters."""
    prefix = "https://www.google.com/url?q="
    if url.startswith(prefix):
        url = url[len(prefix):]

    # Strip ``&sa=`` query parameters which Google adds for tracking.  These
    # may appear with either a literal ampersand or the HTML encoded
    # ``&amp;`` variant.  Everything from the ``&`` through the end of the
    # string should be discarded when found.
    url = re.sub(r"&(amp;)?sa=.*", "", url, flags=re.IGNORECASE)
    return url


def process_html(content: str) -> tuple[str, int]:
    pattern = re.compile(
        r'href=(["\'])https://www\.google\.com/url\?q=([^"\']+)\1',
        re.IGNORECASE,
    )
    def replacer(match: re.Match) -> str:
        quote = match.group(1)
        url = match.group(2)
        cleaned = clean_href(url)
        return f"href={quote}{cleaned}{quote}"

    result, count = pattern.subn(replacer, content)

    # Add ``target="_blank"`` to all links that navigate away from the current
    # page.  Internal fragment links (``href"="#...")`` are left untouched.
    target_pattern = re.compile(r"<a([^>]*)>", re.IGNORECASE)

    def add_target(match: re.Match) -> str:
        attrs = match.group(1)
        href_match = re.search(r"href=([\"'])([^\"']*)\1", attrs, re.IGNORECASE)
        if not href_match:
            return match.group(0)
        href = href_match.group(2)
        if href.startswith('#'):
            return match.group(0)
        target_match = re.search(r"target=([\"'])([^\"']*)\1", attrs, re.IGNORECASE)
        if target_match:
            if target_match.group(2) == "_blank":
                return match.group(0)
            def repl(m: re.Match) -> str:
                q = m.group(1)
                return f"target={q}_blank{q}"

            attrs_new = re.sub(r"target=([\"'])([^\"']*)\1", repl, attrs, flags=re.IGNORECASE)
            add_target.edits += 1
            return f"<a{attrs_new}>"
        else:
            add_target.edits += 1
            return f"<a{attrs} target=\"_blank\">"

    add_target.edits = 0
    result = target_pattern.sub(add_target, result)
    return result, count + add_target.edits


def process_file(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, edits = process_html(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    return edits


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} DIRECTORY")
        sys.exit(1)
    directory = sys.argv[1]
    for root, dirs, files in os.walk(directory):
        for name in files:
            if name.lower().endswith((".html", ".htm")):
                path = os.path.join(root, name)
                print(f"Fixing {path}")
                edits = process_file(path)
                print(f"{edits} edits")
    print("complete")


if __name__ == "__main__":
    main()
