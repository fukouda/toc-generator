from itertools import chain
import sys
import re

def combine_toc_newlayout(toc_lines, old_lines):
    it = chain(toc_lines, old_lines)

    for x in it:
        yield x

def create_toc(filename):

    new_filename = filename.replace('.md', '_with_toc.md')

    with open(filename, 'r') as input_file, open(new_filename, 'w') as output_file:

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

            if re.match(r'^#+\s[\w]+.*$', line):

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
        output_file.write('\n'.join(combine_toc_newlayout(toc_lines, lines_to_write)))



create_toc(sys.argv[1])
