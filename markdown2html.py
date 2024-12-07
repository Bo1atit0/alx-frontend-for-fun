#!/usr/bin/python3

"""
This script converts a Markdown file to an HTML file.

It takes two command-line arguments:
1. The name of the Markdown file (input file).
2. The name of the output HTML file (output file).

Usage:
    ./markdown2html.py input.md output.html

The script uses the `markdown` library to parse the Markdown content
and generate the corresponding HTML.
"""

import sys
import os
import re


def parse_markdown_to_html(md_content):
    """
    Parses Markdown content to HTML manually for:
        - Headings (# to ######)
        - Unordered lists (- Item)
        - Ordered lists (* Item)
        - Paragraphs
        - Bold (**Text** → <b>Text</b>)
        - Emphasis (__Text__ → <em>Text</em>)
    """
    html_lines = []
    in_unordered_list = False
    in_ordered_list = False
    in_paragraph = False

    for line in md_content.splitlines():
        line = line.strip()

        # Handle headings
        if line.startswith("#"):
            parts = line.split(" ", 1)
            hashes = parts[0]
            if len(hashes) <= 6 and len(parts) == 2:
                heading_level = len(hashes)
                heading_text = parts[1].strip()
                heading_text = re.sub(
                    r"\*\*(.+?)\*\*", r"<b>\1</b>", heading_text)
                heading_text = re.sub(
                    r"__(.+?)__", r"<em>\1</em>", heading_text)
                html_lines.append(
                    f"<h{heading_level}>{heading_text}</h{heading_level}>"
                )
            continue

        # Handle unordered lists
        if line.startswith("- "):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False
            if not in_unordered_list:
                html_lines.append("<ul>")
                in_unordered_list = True
            item_text = line[2:].strip()
            item_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", item_text)
            item_text = re.sub(r"__(.+?)__", r"<em>\1</em>", item_text)
            html_lines.append(f"    <li>{item_text}</li>")
            continue

        # Handle ordered lists
        if line.startswith("* "):
            if in_paragraph:
                html_lines.append("</p>")
                in_paragraph = False
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if not in_ordered_list:
                html_lines.append("<ol>")
                in_ordered_list = True
            item_text = line[2:].strip()
            item_text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", item_text)
            item_text = re.sub(r"__(.+?)__", r"<em>\1</em>", item_text)
            html_lines.append(f"    <li>{item_text}</li>")
            continue

        # Handle paragraphs
        if line:  # Non-empty line
            if in_unordered_list:
                html_lines.append("</ul>")
                in_unordered_list = False
            if in_ordered_list:
                html_lines.append("</ol>")
                in_ordered_list = False

            if not in_paragraph:
                html_lines.append("<p>")
                in_paragraph = True
            else:
                html_lines.append("        <br />")
            line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
            line = re.sub(r"__(.+?)__", r"<em>\1</em>", line)
            html_lines.append(f"    {line}")
            continue

        # Empty line (indicates the end of a paragraph or list)
        if in_paragraph:
            html_lines.append("</p>")
            in_paragraph = False
        if in_unordered_list:
            html_lines.append("</ul>")
            in_unordered_list = False
        if in_ordered_list:
            html_lines.append("</ol>")
            in_ordered_list = False

    # Close any open list or paragraph at the end of the document
    if in_paragraph:
        html_lines.append("</p>")
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")

    return "\n".join(html_lines)


if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    # Assign arguments to variables
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Check if the specified Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    try:
        # Read the content of the Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Convert the Markdown content to HTML using the `markdown` library
        html_content = parse_markdown_to_html(md_content)

        # Write the generated HTML content to the output file
        with open(html_file, 'w', encoding='utf-8') as html_output:
            html_output.write(html_content)

    except Exception as e:
        # Handle any exceptions that occur during file operations or conversion
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)  # Exit with status 1 to indicate an error
