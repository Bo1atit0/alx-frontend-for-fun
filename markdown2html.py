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

import sys  # For accessing command-line arguments and error handling
import os   # For checking file existence and interacting with the file system
import markdown  # For converting Markdown content to HTML

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)  # Exit with status 1 to indicate incorrect usage

    # Assign arguments to variables
    markdown_file = sys.argv[1]  # First argument: input Markdown file
    html_file = sys.argv[2]      # Second argument: output HTML file

    # Check if the specified Markdown file exists
    if not os.path.exists(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)  # Exit with status 1 to indicate a missing file

    try:
        # Read the content of the Markdown file
        with open(markdown_file, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()

        # Convert the Markdown content to HTML using the `markdown` library
        html_content = markdown.markdown(md_content)

        # Write the generated HTML content to the output file
        with open(html_file, 'w', encoding='utf-8') as html_output:
            html_output.write(html_content)

        # Indicate successful conversion
        print(f"Converted {markdown_file} to {html_file} successfully.")

    except Exception as e:
        # Handle any exceptions that occur during file operations or conversion
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)  # Exit with status 1 to indicate an error
