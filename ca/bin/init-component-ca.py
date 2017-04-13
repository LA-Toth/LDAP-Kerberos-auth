#!/usr/bin/env python3
import os
import shlex

import subprocess

import sys

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
os.chdir(BASEDIR)


def create_file(path: str, content: str = ''):
    full_path = os.path.join(BASEDIR, path)

    if os.path.exists(full_path):
        return

    with open(full_path, 'w') as f:
        f.write(content)


def split_and_run(command: str):
    if subprocess.call(shlex.split(command, posix=True)):
        sys.exit(1)


def init_ca_files(ca_name: str):
    root_ca_dirs = [
        'ca/{}/db'.format(ca_name),
        'crl',
        'certs',
    ]

    for d in root_ca_dirs:
        os.makedirs(os.path.join(BASEDIR, d), 0o755, exist_ok=True)
    private_dir = os.path.join(BASEDIR, 'ca/{ca_name}/private'.format(ca_name=ca_name))
    os.makedirs(private_dir, 0o700, exist_ok=True)

    os.chmod(private_dir, 0o700)

    create_file('ca/{ca_name}/db/{ca_name}.db'.format(ca_name=ca_name))
    create_file('ca/{ca_name}/db/{ca_name}.db.attr'.format(ca_name=ca_name))
    create_file('ca/{ca_name}/db/{ca_name}.crt.srl'.format(ca_name=ca_name), '01')
    create_file('ca/{ca_name}/db/{ca_name}.crl.srl'.format(ca_name=ca_name), '01')

    if not os.path.exists('{root}/ca/{ca_name}/private/{ca_name}.key'.format(root=BASEDIR, ca_name=ca_name)):
        split_and_run('''openssl req -new \
                            -config {root}/etc/{ca_name}.conf \
                            -out {root}/ca/{ca_name}.csr \
                            -keyout {root}/ca/{ca_name}/private/{ca_name}.key'''.format(root=BASEDIR, ca_name=ca_name))


def sign_and_create_crl(ca_name: str, parent_ca_name: str, extension_prefix: str, *, selfsign: bool = False):
    if not os.path.exists('{root}/ca/{ca_name}.crt'.format(root=BASEDIR, ca_name=ca_name)):
        selfsign_param = '-selfsign' if selfsign else ''
        split_and_run('''openssl ca {selfsign}\
                            -config {root}/etc/{parent_ca_name}.conf \
                            -in {root}/ca/{ca_name}.csr \
                            -out {root}/ca/{ca_name}.crt \
                            -extensions {extension}_ext \
                            -enddate 20361231235959Z'''.format(root=BASEDIR, ca_name=ca_name, parent_ca_name=parent_ca_name,
                                                               extension=extension_prefix, selfsign=selfsign_param))

    if not os.path.exists('{root}/crl/{ca_name}.crl'.format(root=BASEDIR, ca_name=ca_name)):
        split_and_run('''openssl ca -gencrl \
                -config {root}/etc/{ca_name}.conf \
                -out {root}/crl/{ca_name}.crl'''.format(root=BASEDIR, ca_name=ca_name))


init_ca_files('component-ca')
sign_and_create_crl('component-ca', 'network-ca', 'signing_ca')
