#!/usr/bin/env python3

import argparse
import csv
import os
import sys
import yaml

try:
    import ssg.controls
    import ssg.environment
except (ModuleNotFoundError, ImportError):
    sys.stderr.write("Unable to load ssg python modules.\n")
    sys.stderr.write("Hint: run source ./.pyenv.sh\n")
    exit(3)

SSG_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRG_PATH = os.path.join(SSG_ROOT, 'shared', 'references', 'disa-os-srg-v2r3.xml')
RULES_JSON = os.path.join(SSG_ROOT, "build", "rule_dirs.json")
BUILD_CONFIG = os.path.join(SSG_ROOT, "build", "build_config.yml")

SRG_ID_IDX = 2

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=str, action="store", required=True,
                        help="SRG ID to process. Useful for debugging")
    parser.add_argument("-j", "--json", type=str, action="store", default=RULES_JSON,
                        help=f"Path to the rules_dir.json (defaults to {RULES_JSON})")
    parser.add_argument('-c', '--control', type=str, action="store", required=True,
                        help="The control file to parse")
    parser.add_argument('-s', '--csv', type=str, action="store", required=True,
                        help="The CSV export of the DISA STIG spreadsheet")
    parser.add_argument('-d', '--dry-run', action="store_true", required=False,
                        help="Print the result to stdout")
    parser.add_argument("-r", "--root", type=str, action="store", default=SSG_ROOT,
                        help=f"Path to SSG root directory (defaults to {SSG_ROOT})")
    parser.add_argument("-p", "--product", type=str, action="store", required=True,
                        help="What product to get STIGs for")
    parser.add_argument("-b", "--build-config-yaml", default=BUILD_CONFIG,
                        help="YAML file with information about the build configuration.")
    parser.add_argument("-m", "--manual", type=str, action="store",
                        help="Path to XML XCCDF manual file to use as the source of the SRGs",
                        default=SRG_PATH)
    parser.add_argument("-u", "--rule-mode", action="store_true",
                        help="Print attributes expected to create a policy inside a rule dir",
                        default=False)
    return parser.parse_args()

def get_policy(args, env_yaml) -> ssg.controls.Policy:
    policy = ssg.controls.Policy(args.control, env_yaml=env_yaml)
    policy.load()
    return policy


def new_csv_dict(reader) -> dict():
    csv_dict = dict()

    header = next(reader)
    for i, k in enumerate(header):
        csv_dict[i] = k
    return csv_dict


def parse_csv_line(csv_dict: dict, line: list) -> dict():
    ctrl_dict = dict()
    for i, k in enumerate(line):
        ctrl_dict[csv_dict[i]] = k
    return ctrl_dict


def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)


def main() -> None:
    args = parse_args()

    product_dir = os.path.join(args.root, "products", args.product)
    product_yaml_path = os.path.join(product_dir, "product.yml")
    env_yaml = ssg.environment.open_environment(args.build_config_yaml, str(product_yaml_path))
    policy = get_policy(args, env_yaml)

    controls = [ ctr for ctr in policy.controls if ctr.id == args.id ]
    if len(controls) != 1:
        print("Expected to find 1 control, found %d" % len(controls))
        exit(1)

    control = controls[0]

    # augment the data from the CSV
    with open(args.csv) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(4096))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        csv_dict = new_csv_dict(reader)
        line = []
        for l in reader:
            if len(l) < SRG_ID_IDX+1:
                continue
            if l[SRG_ID_IDX] == args.id:
                line = l
                break
        ctrl_dict = parse_csv_line(csv_dict, line)


    update_dict = dict()
    if args.rule_mode:
        update_dict['checktext'] = ctrl_dict.get("Check", "FIXME")
        update_dict['fixtext'] = ctrl_dict.get("Fix", "FIXME")
        update_dict['srg_requirement'] = ctrl_dict.get("SRG Requirement", "FIXME")
    else:
        if control.artifact_description == None and ctrl_dict.get("Artifact Description","") != "":
            update_dict["artifact_description"] = ctrl_dict.get("Artifact Description")
        if control.status_justification == None and ctrl_dict.get("Status Justification","") != "":
            update_dict["status_justification"] = ctrl_dict.get("Status Justification")

    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str
    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)
    yaml.safe_dump(update_dict, sys.stdout)

if __name__ == "__main__":
    main()
