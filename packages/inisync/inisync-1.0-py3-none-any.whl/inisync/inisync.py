import argparse
import configparser
from configobj import ConfigObj

# CLI options
parser = argparse.ArgumentParser(description='Sync values from a source INI file to one or more target INI files.')
parser.add_argument('source', metavar='src', type=str,
                   help='Source filename')
parser.add_argument('target', metavar='dst', type=str, nargs='+',
                   help='Target filename')
parser.add_argument('--section', '-s', metavar='section', type=str, required=True,
                   help='Sectionname in INI file')
parser.add_argument('--option', '-o', metavar='option', type=str, required=True,
                   help='Optionname in INI file')
parser.add_argument('--create', '-c', action="store_true",
                    help='Add Key in destination file if it does not exist.')
args = parser.parse_args()


def main():
  print(args)

  target = configparser.ConfigParser()
  target.read(args.target)
  source = configparser.ConfigParser()
  source.read(args.source)

  if not source.has_option(args.section, args.option):
    print(f'Provided option "{args.option}" in section "{args.section}" not existant in SOURCE file!')
    exit(1)
  if not (args.create or target.has_option(args.section, args.option)):
    print(f'Provided option "{args.option}" in section "{args.section}" not existant in TARGET file!')
    exit(1)

  value = source.get(args.section, args.option)
  
  for target_file in args.target:
    config = ConfigObj(target_file)
    config[args.section][args.option] = value
    config.write()
