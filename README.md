# toc-generator
---
A table of contents generator for Markdown files built in Python.

## Getting Started

All you need to do is clone the repo and call `toc-generator.py` along with the Markdown file you want to generate the table of contents for.

```BASH
git clone https://github.com/fukouda/toc-generator.git
cd toc-generator
python toc-generator.py your_markdown_file.md
```

## Usage:

```BASH
usage: toc-generator.py [-h] [-i] [-b BULLETS] [-nt] [-o [OUTPUT]] inputfile

Autogenerates the table of contents for a markdown file and links to each
heading based on the heading titles.

positional arguments:
  inputfile             The Markdown file that needs the table of contents

optional arguments:
  -h, --help            Show this help message and exit.

  -i, --inline          Edit the inputfile inline and place the TOC within
                        {inline-toc} . It can also be combined with '-o' to output
                        to a specific file.

  -b BULLETS, --bullets BULLETS
                        Enable custom bullets for items in the generated TOC
                        (default is '-')

  -nt, --no_title       This option will disable the title for the table of contents

  -o [OUTPUT], --output [OUTPUT]
                        Output the table of contents to specified file
                        [OUTPUT] instead of printing to screen (default
                        OUTPUT: [inputfile]_with_toc.md)
```

## Examples

You can run the example Markdown files from the examples folder like this:

```BASH
python toc-generator.py examples/test.md
```
