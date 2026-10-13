import re, subprocess, sys, tempfile, pathlib
import markdown

root = pathlib.Path(__file__).parent
css = re.search(r"<style>(.*?)</style>", (root / "_layouts/default.html").read_text(), re.S).group(1)
jobs = [("index.md", "Benoit-Clennett-Sirois-CV-fr.pdf", "fr"), ("english/index.md", "Benoit-Clennett-Sirois-CV-en.pdf", "en")]

for src, out, lang in jobs:
    text = (root / src).read_text()
    text = re.sub(r"^\[[^\]]*\]\([^)]*\)\s*$", "", text, count=1, flags=re.M)  # language switch link
    text = re.sub(r"(?m)^(?!\s*[*-] )(.+)\n(\s*[*-] )", r"\1\n\n\2", text)  # python-markdown needs a blank line before lists
    body = markdown.markdown(text, extensions=["extra"])
    html = f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="main-content">{body}</div></body></html>'
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
    subprocess.run(["google-chrome", "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={root / out}", f"file://{f.name}"], check=True)
