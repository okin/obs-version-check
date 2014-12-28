#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from flask import Flask
# app = Flask(__name__)
app = Flask("obsversioncheck")

PROJECTS_TO_CHECK = (
    'home:uibmz:opsi:opsi40',
)

@app.route("/")
def show_overview():
    if not PROJECTS_TO_CHECK:
        return "No projects configured."

    projects = {}
    for project in PROJECTS_TO_CHECK:
        projects[project] = get_versions(project)

    return str(projects)


def get_versions(project):
    repo = get_link_to_project_repository(project)

    software = {}
    for operating_system in get_operating_systems(repo):
        print("Found OS: {name}".format(name=operating_system))
        software[operating_system] = parse_repository('{repo}{os}'.format(repo=repo, os=operating_system))

    print("Software is: {0}".format(software))
    return software


def get_link_to_project_repository(project):
    return 'http://download.opensuse.org/repositories/{project}/'.format(project=project.replace(':', r':/'))


def get_operating_systems(link_to_repository):
    request = requests.get(link_to_repository)

    # Links will look like: <a href="Univention_3.2/">Univention_3.2/</a>
    for finding in re.findall('<a href="(?P<os>[\w.-]+)/">(?P=os)/</a>', request.text):
        yield finding


def parse_repository(link_to_repository):
    print("Parsing repo: {0}".format(link_to_repository))

    try:
        return {split_name_and_version(sw)[0]: split_name_and_version(sw)[1] for sw in get_software_from_repository(link_to_repository)}
    except Exception as err:
        print("Fuck: {0}".format(err))
        return {}


def get_software_from_repository(link_to_repository):
    print("Parsing {0}".format(link_to_repository))
    request = requests.get(link_to_repository)

    for folder in re.findall('<a href="(?P<folder>[\w_]+/)">(?P=folder)</a>', request.text):
        yield from get_software_from_repository('/'.join((link_to_repository, folder)))

    for finding in re.findall('<a href="(?P<file>[\w\d._-]+(\.rpm|\.deb))">(?P=file)</a>', request.text):
        yield finding[0]  # we have a tuple, only want first item


def split_name_and_version(filename):
    if filename.endswith('.rpm'):
        match = re.search('(?P<name>[\w_-]+)-(?P<version>.+)\.(i\d86|ia64|x86_64|noarch|src)\.rpm', filename)
    elif filename.endswith('.deb'):
        match = re.search('(?P<name>[\w_-]+)_(?P<version>.+)_(i\d86|amd64|all)\.deb', filename)
    else:
        match = None

    if match:
        return (match.group('name'), match.group('version'))

    raise ValueError("Unable to split software name and version from {0}".format(filename))


if __name__ == "__main__":
    app.run()
