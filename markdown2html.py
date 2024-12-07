#!/usr/bin/python3

import sys
import os

if len(sys.argv) < 3:
    print("Usage: ./markdown2html.py README.md README.html")
    sys.exit(1)

    mark_down_file = sys.argv[1]
    html_file = sys.argv[2]

    if not os.path.exists(mark_down_file):
        print(f"Missing {mark_down_file}")
        sys.exit(1)