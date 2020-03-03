#!/usr/bin/env python3

import errno
import os
import os.path
import sys
import urllib.parse
from string import Template

mc_template = \
"""# platform = $platform
apiVersion: machineconfiguration.openshift.io/v1
kind: MachineConfig
spec:
  config:
    ignition:
      version: 2.2.0
    storage:
      files:
      - contents:
          source: data:,$content
        filesystem: root
        mode: $mode
        path: $path
"""

def urlencoded_file(filename):
    with open(filename) as f:
        return urllib.parse.quote(''.join(f.readlines()))

def resolve_rule_dir(rule_name, content_root):
    # If the rulename is not given, we can't find the rule path
    if rule_name is None:
        return None

    # Otherwise we try to guess it based on the rule name
    for root, dirs, files in os.walk(content_root):
        # FIXME: split the path properly?
        if root.endswith(rule_name):
            return root

    return None


def get_ign_dir(rule_dir):
    return os.path.join(rule_dir, "ignition")


def get_ign_file(rule_dir):
    return os.path.join(get_ign_dir(rule_dir), "shared.yml")


class IgnEncoder(object):
    # too many options? Convert to flags?
    def __init__(self, content_root=None, force=False, dry_run=False, debug=False):
        self._content_root = content_root
        self._force = force
        self._dry_run = dry_run
        self._debug = debug

        if self._content_root == None:
            self._content_root = os.path.join(os.getcwd(), "linux_os")

        self._ign_wrappers = []

    def add_wrapper(self, wrapper):
        self._ign_wrappers.append(wrapper)

    def write_ign_remediations(self, force=False):
        for ign in self._ign_wrappers:
            content = ign.encode()
            rule_path = self._resolve_rule_dir(ign.rule)
            self._write_ign_file(rule_path, content)

    def _resolve_rule_dir(self, rule_name):
        return resolve_rule_dir(rule_name, self._content_root)

    def _write_ign_file(self, rule_dir, content):
        ign_dir = get_ign_dir(rule_dir)
        ign_path = get_ign_file(rule_dir)

        with self._ign_file_handle(ign_dir, ign_path) as ign_fhandle:
            if self._debug:
                print(ign_path)
                print(content)
            ign_fhandle.write(content)

    def _ign_file_handle(self, ign_dir, ign_path):
        if self._dry_run:
            return open("/dev/stdout", "w")

        if os.path.exists(ign_path) and self._force is False:
            return open("/dev/null", "w")

        try:
            ign_file = open(ign_path, "w")
        except OSError as e:
            if e.errno == errno.ENOENT:
                os.mkdir(ign_dir)
                ign_file = open(ign_path, "w")
            else:
                raise
        return ign_file


# Should we have encoder accept an array of IgnSource objects so we can
# generate a remediation out of multiple files?
class IgnFileWrapper(object):
    def __init__(self, rule, infile_path, target_path, mode="0644", platform="multi_platform_ocp"):
        self.rule = rule
        self.infile_path = infile_path
        self.target_path = target_path
        self.mode = mode
        self.platform = platform

    def __repr__(self):
        return "%s: [%s, %s]" % (self.rule, self.infile_path, self.target_path)

    def encode(self):
        content = urlencoded_file(self.infile_path)
        tmpl = Template(mc_template)
        mc = tmpl.substitute(path=self.target_path, mode=self.mode,
                             platform=self.platform, content=content)
        return mc
