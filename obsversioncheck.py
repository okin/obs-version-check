#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from flask import Flask, render_template
app = Flask(__name__)

PROJECTS_TO_CHECK = (
    'home:uibmz:opsi:opsi40',
    'home:uibmz:opsi:opsi40-testing',
    'home:uibmz:opsi:opsi40-experimental',
)
IMPORTANT_SOFTWARE = ('python-opsi', 'opsiconfd')


@app.route('/<project>/<os>/')
@app.route('/<project>/')
def show_project(project, os=None):
    if project not in PROJECTS_TO_CHECK:
        return "Unconfigured project: {0}".format(project)

    operating_systems = list(get_operating_systems(project))
    repo_url = get_link_to_project_repository(project, os)

    if os is None:
        if IMPORTANT_SOFTWARE:
            important_software = {}
            for (software, version) in parse_repository(repo_url).items():
                if software not in IMPORTANT_SOFTWARE:
                    continue

                if software in important_software:
                    if version > important_software[software]:
                        important_software[software] = version
                else:
                    important_software[software] = version
        else:
            important_software = {}

        return render_template('project.html',
                               project=project,
                               systems=operating_systems,
                               important_software=important_software)
    elif os not in operating_systems:
        return "Invalid OS. Valid OS: {0}".format(', '.join(operating_systems))

    software = parse_repository(repo_url)

    return render_template('os.html',
                           project=project,
                           os=os,
                           software=software,
                           important_software=IMPORTANT_SOFTWARE)

@app.route("/")
def show_overview():
    if not PROJECTS_TO_CHECK:
        return "No projects configured."

    projects = {project: get_operating_systems(project) for project in PROJECTS_TO_CHECK}

    return render_template('overview.html', projects=projects)


def get_versions(project):
    repo = get_link_to_project_repository(project)

    software = {}
    for operating_system in get_operating_systems(project):
        print("Found OS: {name}".format(name=operating_system))
        repo_url = get_link_to_project_repository(project, operating_system)
        software[operating_system] = parse_repository(repo_url)

    print("Software in {project} is: {0}".format(software, project=project))
    return software


def get_link_to_project_repository(project, os=None):
    if os is None:
        return 'http://download.opensuse.org/repositories/{project}/'.format(project=project.replace(':', r':/'))
    else:
        return 'http://download.opensuse.org/repositories/{project}/{os}'.format(project=project.replace(':', r':/'), os=os)


def get_operating_systems(project):
    request = requests.get(get_link_to_project_repository(project))

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
