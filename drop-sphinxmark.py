import os
import subprocess

from osa import repos

for repo in repos:
    print(repo.working_dir)

    # Remove from doc/requirements.txt
    req_path = "%s/doc/requirements.txt" % repo.working_dir
    if os.path.isfile(req_path):
        proc = subprocess.run("sed /^sphinxmark/d %s" % (req_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(req_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Remove sphinxmark module reference
    conf_path = "%s/doc/source/conf.py" % repo.working_dir
    if os.path.isfile(conf_path):
        proc = subprocess.run("sed /sphinxmark/d %s" % (conf_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(conf_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Remove watermark reference
    conf_path = "%s/doc/source/conf.py" % repo.working_dir
    if os.path.isfile(conf_path):
        proc = subprocess.run("sed /watermark/d %s" % (conf_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(conf_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Remove trailing sed line reference
    conf_path = "%s/doc/source/conf.py" % repo.working_dir
    if os.path.isfile(conf_path):
        proc = subprocess.run("sed /^\|\ awk/d %s" % (conf_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(conf_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Remove config comment
    conf_path = "%s/doc/source/conf.py" % repo.working_dir
    if os.path.isfile(conf_path):
        proc = subprocess.run("sed /^#.\*sphinxmark/d %s" % (conf_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(conf_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Remove config files
    conf_path = "%s/doc/source/conf.py" % repo.working_dir
    if os.path.isfile(conf_path):
        proc = subprocess.run("sed /^sphinxmark/d %s" % (conf_path),
                              shell=True, check=True, capture_output=True)

        # NOTE(mnaser): macOS doesn't have GNU sed, so `-i` flag is missing.
        with open(conf_path, 'wb') as fd:
            fd.write(proc.stdout)

    # Commit if we have changes
    if repo.is_dirty():
        message = """docs: drop sphinxmark

sphinxmark is no longer compatible with the latest release of Sphinx
which is causing all of our documentation jobs to fail.  This patch
removes it as our current usage of openstacktheme for documentation
already provides watermarks for current branch and notices for which
branch the documentation covers.
"""
        repo.git.commit('-a', '-m', message)

    # Get latest commit
    commit = repo.head.commit

    # Send to Gerrit
    if 'drop sphinxmark' in commit.message:
        repo.git.execute(['git', 'review', '-t', 'osa-drop-sphinxmark'])