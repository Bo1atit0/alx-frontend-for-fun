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


def parse_markdown_to_html(md_content):

    """
    Parses Markdown content to HTML manually for headings.
    Only supports strict heading syntax (# to ######).
    """
    html_lines = []
    in_list = False  # Tracks whether we are inside a list

    for line in md_content.splitlines():
        # Handle headings
        if line.startswith("#"):
            parts = line.split(" ", 1)  # Split into the # part and the text
            hashes = parts[0]          # The # part
            if len(hashes) <= 6 and len(parts) == 2:  # Valid heading
                heading_level = len(hashes)
                heading_text = parts[1].strip()
                html_lines.append(
                    f"<h{heading_level}>{heading_text}</h{heading_level}>")
            continue

        # Handle unordered lists
        if line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")  # Start a new unordered list
                in_list = True
            list_item = line[2:].strip()  # Remove the "- " prefix
            html_lines.append(f"    <li>{list_item}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")  # Close the unordered list
                in_list = False

    # Close any open list at the end of the document
    if in_list:
        html_lines.append("</ul>")

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
