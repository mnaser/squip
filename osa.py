#!/usr/bin/env python3

import os
import sys

import git
import requests
import yaml

# Get the list of projects
url = 'https://opendev.org/openstack/governance/raw/branch/master/reference/projects.yaml'
r = requests.get(url)
deliverables = yaml.load(r.text).get('OpenStackAnsible').get('deliverables')
git_repos = deliverables['openstack-ansible-roles']['repos']
repos = []

for repo in git_repos:
    ns, role = repo.split('/')
    path = "https://opendev.org/%s" % (repo)
    clone_path = 'roles/%s' % role

    # Get the latest code
    if os.path.isdir(clone_path):
        print("%s: resetting to origin/master and pulling" % repo)
        repo = git.Repo(clone_path)
        repo.git.reset('--hard')
        repo.heads.master.checkout()
        repo.git.reset('--hard')
        repo.git.clean('-xdf')
        repo.remotes.origin.pull()
    else:
        print("%s: cloning" % repo)
        repo = git.Repo.clone_from(path, clone_path)

    # Add to imported list of repos
    repos.append(repo)