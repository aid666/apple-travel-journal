#!/usr/bin/env python3
"""
Assemble a travel journal HTML file from template and content.

Usage:
    python3 assemble_html.py --title "TITLE" --content content.html --template template.html --output journal.html
    python3 assemble_html.py --title "TITLE" --content content.html --template template.html --output journal.html --embed-images

If --embed-images is specified, local image paths in <img src="..."> tags
will be converted to base64 data URIs for single-file portability.
"""

import argparse
import base64
import mimetypes
import os
import re
import sys


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def embed_images(html: str, base_dir: str) -> str:
    """Replace local image src with base64 data URIs."""

    def replace_src(match):
        src = match.group(1)
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        img_path = os.path.join(base_dir, src) if not os.path.isabs(src) else src
        if not os.path.exists(img_path):
            print(f"Warning: image not found: {img_path}", file=sys.stderr)
            return match.group(0)
        mime, _ = mimetypes.guess_type(img_path)
        if mime is None:
            mime = "image/jpeg"
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("ascii")
        return f'src="data:{mime};base64,{b64}"'

    return re.sub(r'src="([^"]+)"', replace_src, html)


def main():
    parser = argparse.ArgumentParser(description="Assemble travel journal HTML")
    parser.add_argument("--title", required=True, help="Journal title")
    parser.add_argument("--content", required=True, help="Path to content HTML fragment")
    parser.add_argument("--template", required=True, help="Path to HTML template")
    parser.add_argument("--output", required=True, help="Output HTML file path")
    parser.add_argument(
        "--embed-images",
        action="store_true",
        help="Embed local images as base64 data URIs",
    )
    args = parser.parse_args()

    template = read_file(args.template)
    content = read_file(args.content)

    html = template.replace("{{TITLE}}", args.title).replace("{{CONTENT}}", content)

    if args.embed_images:
        base_dir = os.path.dirname(os.path.abspath(args.content))
        html = embed_images(html, base_dir)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated: {args.output}")
    print(f"Size: {os.path.getsize(args.output):,} bytes")


if __name__ == "__main__":
    main()
