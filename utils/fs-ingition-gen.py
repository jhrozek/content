#!/usr/bin/env python3

import argparse
import os
import os.path
import re

from ignition_encoder import IgnEncoder,IgnFileWrapper

description = \
"""
To be filled later
"""

def parse_runlevel_like_name(filename):
    m = re.match('^(\d\d-)(.*$)', filename)
    if m == None or len(m.groups()) < 2:
        return ""
    return m.groups()[1]

def guess_rule_name(file_path):
    file_dir, file_name = os.path.split(file_path)
    last_dir = file_dir.split(os.sep)[-1]

    rule_name = file_name
    # TODO: We should always be able to read the rule name from some comment
    # or such, then remove the comment (maybe later in the encoder?)

    # First heuristics, if the last directory of the rule path ends with a .d
    # and the rule itself starts with two digits and a dash, strip the two
    # digits and use the remainder as the rule name
    if last_dir.endswith(".d"):
        rule_name = parse_runlevel_like_name(file_name)

    # Fall back to just using the filename without the extension 
    # as the rulename
    return os.path.splitext(rule_name)[0]

def main():
    parser = argparse.ArgumentParser(
                            description=description,
                            formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--dry-run', action='store_true',
                        help='If set, the rules would be just printed to stdout')
    parser.add_argument('--force', action='store_true',
                        help='If set, existing rules would be overwritten')
    parser.add_argument('--debug', action='store_true',
                        help='If set, the rules and the rule names would be printed out')
    parser.add_argument('ROOT', action='store', type=str,
                        help='The base of the chroot')
    args = parser.parse_args()

    abs_root = os.path.abspath(args.ROOT)

    encoder = IgnEncoder(dry_run=args.dry_run,
                         force=args.force,
                         debug=args.debug)

    for root, dirs, files in os.walk(args.ROOT):
        if len(files) == 0:
            continue
        for f in files:
            infile_path = os.path.join(root, f)
            rule = guess_rule_name(infile_path)
            chroot_rel_path = os.path.relpath(infile_path, abs_root)

            wrapper = IgnFileWrapper(rule,
                                     infile_path,
                                     target_path=os.path.join("/",chroot_rel_path))
            print(wrapper)
            encoder.add_wrapper(wrapper)

    encoder.write_ign_remediations()

if __name__ == "__main__":
    main()
