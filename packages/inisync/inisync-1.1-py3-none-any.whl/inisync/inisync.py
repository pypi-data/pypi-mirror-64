import argparse
import configparser
from shutil import copyfile
from configobj import ConfigObj

# CLI options
parser = argparse.ArgumentParser(description='Sync values from a source INI file to one or more target INI files.')
parser.add_argument('source', metavar='src', type=str,
                   help='Source filename')
parser.add_argument('target', metavar='dst', type=str, nargs='+',
                   help='Target filename')
parser.add_argument('--section', '-s', metavar='sec', type=str, required=True,
                   help='Sectionname in INI file')
parser.add_argument('--key', '-k', metavar='key', type=str, required=True,
                   help='Keyname in INI file')
parser.add_argument('--create', '-c', action="store_true",
                    help='Add Key in destination file if it does not exist.')
parser.add_argument('--skip-backup', action="store_true",
                    help='Skip creation of target file backups.')
args = parser.parse_args()


def main():
  source = configparser.ConfigParser()
  source.read(args.source)
  target = configparser.ConfigParser()
  target.read(args.target)

  # check source and read source value
  if not source.has_option(args.section, args.key):
    print(f'Provided option "{args.key}" in section "{args.section}" not existant in SOURCE file!')
    exit(1)
  value = source.get(args.section, args.key)
  
  # check if each target has key or create option is set
  for target_file in args.target:
    target.read(target_file)
    if not (args.create or target.has_option(args.section, args.key)):
      print(f'Provided key "{args.key}" in section "{args.section}" not existant in TARGET file!')
      exit(1)

  # update each target file
  for target_file in args.target:
    if not args.skip_backup:
      backup(target_file)
      
    print(f'Setting value "{value}" to key "[{args.section}]{args.key}" in file "{target_file}"...')
    config = ConfigObj(target_file)
    config[args.section][args.key] = value
    config.write()

  print("done.")

def backup(target_file: str):
  copyfile(target_file, target_file + '.bak')
  print("Backup file created: " + target_file + ".bak")
