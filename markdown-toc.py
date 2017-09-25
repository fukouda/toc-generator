#!/usr/bin/python

from itertools import chain
import sys, argparse, re

def combine_toc_newlayout(toc_lines, old_lines):
    it = chain(toc_lines, old_lines)

    for x in it:
        yield x

def generate_toc(filename, new_filename = None):

    with open(filename, 'r') as input_file:

        toc_lines = ['# Table of Contents']
        lines_to_write = []
        heading_id_struct = '<a name="{0}"></a>'
        toc_struct = '- [{0}](#{1})'

        line_iter = iter(input_file)
        for line in line_iter:

            line_stripped = line.rstrip(' \n')

            if re.match(r'^```[\w]+$', line_stripped):
                lines_to_write.append(line.rstrip(' \n'))
                line = next(line_iter,'')
                while line != '```\n':
                    lines_to_write.append(line.rstrip(' \n'))
                    line = next(line_iter,'')
                lines_to_write.append(line.rstrip(' \n'))
                continue

            elif re.match(r'^#+\s[\w]+.*$', line):

                full_heading = line_stripped
                last_hash_char = full_heading.rfind('#')

                heading_name = full_heading[last_hash_char + 2:]
                heading_id = '-'.join(heading_name.lower().replace(',', '').split(' '))
                heading_offset = '\t' * (last_hash_char - 1)

                toc_entry = heading_offset + toc_struct.format(heading_name.title(), heading_id)
                toc_lines.append(toc_entry)

                linked_heading = full_heading.title() + ' ' + heading_id_struct.format(heading_id)
                lines_to_write.append(linked_heading)

                continue

            lines_to_write.append(line_stripped)

        toc_lines.append('\n')

        if not new_filename:
            for i in toc_lines:
                print(i)
            sys.exit()

        with open(new_filename, 'w') as output_file:
            output_file.write('\n'.join(combine_toc_newlayout(toc_lines, lines_to_write)))

        sys.exit()


if __name__ == "__main__":
    input_file = ''
    parser = argparse.ArgumentParser(description="Autogenerates the table of contents for a markdown file based on the heading titles.")
    parser.add_argument('inputfile',
                        help="the file to generate the table of contents for",
                        type=str)
    parser.add_argument('-o', '--output',
                        nargs='?',
                        const=' ',
                        help="append table of contents to the beginning of the source file and output to specified file (default: print table of contents markdown directly onto terminal)",
                        type=str)
    args = parser.parse_args()
    input_file = args.inputfile
    if args.output:
        output_file = args.output if (args.output != ' ') else input_file.replace('.md', '_with_toc.md')
        generate_toc(input_file, output_file)

    generate_toc(input_file)
