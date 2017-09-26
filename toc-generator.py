#!/usr/bin/env python3

import sys, argparse, re

def compiled_markdown(table_of_contents, old_lines, inline_tag, index):
    """
    Generator function which yields lines from the list of lines to be written
    and also replaces the inline tag with the table of contents
    """

    if inline_tag:
        old_lines[index] = re.sub(inline_tag, table_of_contents, old_lines[index])

    it = iter(old_lines)
    for x in it:
        yield x

def generate_toc(**kwargs):
    """
    This function builds a symbol table for the different headings
    to avoid duplicate heading ids, creates the table of contents,
    and finds where the inline tag is located within the given
    Markdown file
    """

    infile = kwargs['infile']
    outfile = kwargs['outfile'] if 'outfile' in kwargs else None
    bullets = kwargs['bullets']
    inline = kwargs['inline'] if 'inline' in kwargs else False
    no_title = kwargs['no_title']


    with open(infile, 'r') as input_file:

        inline_index = 0
        toc_symbol_table = {}
        table_of_contents = ''
        lines_to_write = []

        linked_headings = True
        toc_title = '## Table of Contents\n'
        heading_id_struct = '<a name="{0}"></a>'
        toc_struct = bullets + ' [{0}](#{1})'
        inline_tag = r"{inline-toc}"

        counter = 0
        line_iter = iter(input_file)
        for line in line_iter:

            counter += 1

            line_stripped = line.rstrip(' \n')

            if re.match(r'^```[\w]+\s*$', line):
                lines_to_write.append(line_stripped)
                line = next(line_iter,'')
                while line != '```\n':
                    lines_to_write.append(line.rstrip(' \n'))
                    counter += 1
                    line = next(line_iter,'')
                lines_to_write.append(line.rstrip(' \n'))
                counter += 1
                continue

            elif re.match(r'[^`]*{0}'.format(inline_tag), line):
                inline_index = counter + 1
                pos = line_stripped.find(inline_tag)
                lines_to_write.append(line_stripped[:pos])
                lines_to_write.append(line_stripped[pos + len(inline_tag) + 1:])


            elif re.match(r'^#+\s[\w]+.*$', line):

                full_heading = line_stripped
                last_hash_char = full_heading.rfind('#')

                heading_name = full_heading[last_hash_char + 2:]

                heading_id = '-'.join(heading_name.lower().replace(',', '').split(' '))
                heading_offset = '\t' * (last_hash_char - 1)

                if heading_name in toc_symbol_table:
                    toc_symbol_table[heading_name] += 1
                    heading_id += str(toc_symbol_table[heading_name])
                else:
                    toc_symbol_table[heading_name] = 0

                toc_entry = heading_offset + toc_struct.format(heading_name, heading_id) + '\n'
                table_of_contents += toc_entry

                if linked_headings:
                    linked_heading = full_heading + ' ' + heading_id_struct.format(heading_id)
                    lines_to_write.append(linked_heading)

                continue

            lines_to_write.append(line_stripped)

        table_of_contents += '\n'

        if not no_title:
            table_of_contents = toc_title + table_of_contents

        if not outfile:
            if inline:
                print('\n'.join(compiled_markdown(table_of_contents, lines_to_write, inline_tag, inline_index)))
            else:
                print(table_of_contents)
            sys.exit()

        with open(outfile, 'w') as output_file:
            if inline:
                output_file.write('\n'.join(compiled_markdown(table_of_contents, lines_to_write, inline_tag, inline_index)))
            else:
                output_file.write(table_of_contents)

        sys.exit()

def main():
    """
    Parses the arguments from the command line and passes them into the
    generate_toc function for processing
    """
    input_file = ''
    parser = argparse.ArgumentParser(add_help=False, description="Autogenerates the table of contents for a markdown file and links to each heading based on the heading titles.")
    parser.add_argument('inputfile',
                        help="The Markdown file that needs the table of contents",
                        type=str)
    parser.add_argument('-h',
                        '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-i',
                        '--inline',
                        action='store_true',
                        help="Edit the inputfile inline and place the TOC within {inline-toc} * can also be combined with -o to output to named file")
    parser.add_argument('-b',
                        '--bullets',
                        default='-',
                        help="Enable custom bullets for items in the generated TOC (default is '-')",
                        type=str)
    parser.add_argument('-nt',
                        '--no_title',
                        action='store_true',
                        help="This option will disable the title for table of contents")
    parser.add_argument('-o', '--output',
                        nargs='?',
                        const=' ',
                        help="Output the table of contents to specified file [OUTPUT] instead of printing to screen (default OUTPUT: [inputfile]_with_toc.md)",
                        type=str)
    args = parser.parse_args()

    input_file = args.inputfile
    output_file = args.output if (args.output != ' ') else input_file.replace('.md', '_with_toc.md')
    inline_on = args.inline
    bullets = args.bullets
    no_title = args.no_title

    if not args.output:
         generate_toc(infile=input_file, bullets=bullets, inline=inline_on, no_title=no_title)

    generate_toc(infile=input_file, outfile=output_file, bullets=bullets, inline=inline_on, no_title=no_title)

if __name__ == "__main__":
    main()
