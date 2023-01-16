#!/usr/bin/env python3

import argparse
import json
import os
import pathlib
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
RULES_JSON = os.path.join(SSG_ROOT, "build", "rule_dirs.json")
BUILD_CONFIG = os.path.join(SSG_ROOT, "build", "build_config.yml")
SRG_PATH = os.path.join(SSG_ROOT, 'shared', 'references', 'disa-os-srg-v2r3.xml')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--id', type=str, action="store",
                        help="SRG ID to process. Useful for debugging")
    parser.add_argument("-j", "--json", type=str, action="store", default=RULES_JSON,
                        help=f"Path to the rules_dir.json (defaults to {RULES_JSON})")
    parser.add_argument('-c', '--control', type=str, action="store", required=True,
                        help="The control file to parse")
    parser.add_argument("-r", "--root", type=str, action="store", default=SSG_ROOT,
                        help=f"Path to SSG root directory (defaults to {SSG_ROOT})")
    parser.add_argument("-p", "--product", type=str, action="store", required=True,
                        help="What product to get STIGs for")
    parser.add_argument("-b", "--build-config-yaml", default=BUILD_CONFIG,
                        help="YAML file with information about the build configuration.")
    parser.add_argument("-m", "--manual", type=str, action="store",
                        help="Path to XML XCCDF manual file to use as the source of the SRGs",
                        default=SRG_PATH)
    return parser.parse_args()


def get_policy(args, env_yaml) -> ssg.controls.Policy:
    policy = ssg.controls.Policy(args.control, env_yaml=env_yaml)
    policy.load()
    return policy


def get_rule_json(json_path: str) -> dict:
    with open(json_path, 'r') as json_file:
        rule_json = json.load(json_file)
    return rule_json


def html_plain_text(source: str) -> str:
    if source is None:
        return ""
    # Quick and dirty way to clean up HTML fields.
    # Add line breaks
    result = source.replace("<br />", "\n")
    result = result.replace("<br/>", "\n")
    result = result.replace("<tt>", '"')
    result = result.replace("</tt>", '"')
    # Remove all other tags
    result = re.sub(r"(?s)<.*?>", " ", result)

    # only replace this after replacing other tags as < and >
    # would be caught by the generic substitution
    result = result.replace("&gt;", ">")
    result = result.replace("&lt;", "<")
    return result

def repr_str(dumper, data):
    if '\n' in data:
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data, style='|')
    return dumper.org_represent_str(data)

def main() -> None:
    args = parse_args()

    # open the controls
    product_dir = os.path.join(args.root, "products", args.product)
    product_yaml_path = os.path.join(product_dir, "product.yml")
    env_yaml = ssg.environment.open_environment(args.build_config_yaml, str(product_yaml_path))
    policy = get_policy(args, env_yaml)
    rule_json = get_rule_json(args.json)

    # instantiate the control
    all_controls = policy.controls
    if args.id != "":
        all_controls = [ ctr for ctr in policy.controls if ctr.id == args.id ]

    for control in all_controls:
        print(control)

    # create the policy file contents
    policy_dict = dict()
    policy_dict['fixtext'] = control.fixtext
    policy_dict['checktext'] = control.check
    #policy_dict['vuldiscussion'] = html_plain_text(control.rationale)
    policy_dict['srg_requirement'] = control.title

    yaml.SafeDumper.org_represent_str = yaml.SafeDumper.represent_str

    yaml.add_representer(str, repr_str, Dumper=yaml.SafeDumper)

    # find the rule(s) that implement this control
    rules = [ rule_json[rule] for rule in control.selected ]

    # for each rule, create a policy file based on the control contents
    for r in rules:
        pdir = os.path.join(r['dir'], "policy", "stig")
        if os.path.exists(pdir):
            print("Refusing to modify existing policy")
            continue
        pathlib.Path(pdir).mkdir(parents=True)
        pfile = os.path.join(pdir, "shared.yml")
        with open(pfile, "w") as pfh:
            yaml.safe_dump(policy_dict, pfh)

if __name__ == '__main__':
    main()