import argparse
import html

desc="""CSS Encapsulator / Namespace Applier Code
Python 3.5+
Ömer Selçuk"""
version='1.1'

if __name__ != '__main__': exit()

parser = argparse.ArgumentParser(description=desc)
parser.add_argument('-v', '--version', help='Show version', action='store_true')
parser.add_argument('-o', '--output-file', help='Output file name')
parser.add_argument('-d', '--dry-run', action='store_true', help="Don't modifiy anything, just show me what would happen")
parser.add_argument('-n', '--namespace', default="encapsulated", help='Class name to be added to every identifier in CSS file')
parser.add_argument('file', metavar='CSS File', type=str, help='Input CSS file')
args = parser.parse_args()

if args.version:
    print(version)
    exit()


namespace = args.namespace
cname = namespace if namespace.startswith('.') else f'.{namespace}'
filename = args.file
dryrun = bool(args.dry_run)

if args.output_file:
    new_filename = args.output_file
else:
    new_filename = filename.split('.')
    new_filename = ''.join(new_filename[:-1]) + '.encapsulated.' + new_filename[-1]

file = open(filename, 'rt')
if not dryrun:
    mod = open(new_filename, 'wt')


def variations(tag):
    """returns (tag, {rules}, {fixes})"""
    return [
        (f' {tag} ', {}, {'pre': ' ', 'suf': ' '}),
        (f'{tag} ', {'position': 0}, {'pre': '', 'suf': ' '}),
        (f', {tag}, ', {}, {'pre': ', ', 'suf': ', '}),
        (f', {tag} ', {}, {'pre': ', ', 'suf': ' '}),
        (f'{tag},', {'position': 0}, {'pre': '', 'suf': ','}),
        (f' {tag}, ', {}, {'pre': ' ', 'suf': ', '}),

        (f'{tag}:', {'position': 0}, {'pre': '', 'suf': ':'}),
        (f' {tag}:', {}, {'pre': ' ', 'suf': ':'}), 
        (f', {tag}:', {}, {'pre': ', ', 'suf': ':'}), 
    ]


lines = file.readlines()
modified_lines = 0

for index, line in enumerate(lines):
    modified = False
    line = line.replace('\n', '')
    newline = line

    for tag in html.tags:
        vars = variations(tag)
        
        for var, rules, fix in vars:
            if not var in line: continue
            broken = False
            if len(rules):
                for key, value in rules.items():
                    if not (key == 'position' and line.find(var) == value): 
                        broken = True
                        break                    
            if broken: continue

            replacement = fix['pre'] + tag + cname + fix['suf']
            newline = newline.replace(var, replacement)
            modified = True

    if dryrun and modified:
        print(f'[{index}] {line} ---> {newline}')
    if not dryrun:
        mod.write(f'{newline}\n')
    if modified: modified_lines += 1


if not dryrun:
    print(f'Namespacing for {filename} ---> {new_filename} completed.')
    print(f'Total {modified_lines} lines affected.')
else:
    print(f'Namespacing for {filename} [dry-run] completed.')
    print(f'Total {modified_lines} lines would have affected.')
print('Have a great day.')
