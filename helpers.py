import os
import pathlib
import pytest
import shutil
import subprocess
from subprocess import PIPE, STDOUT


@pytest.fixture(scope='module')
def basedir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "tmp")
    init_dir(base)
    yield base
    os.chdir(project_dir)


def init_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def write_file(wt, path, text):
    f = pathlib.Path(os.path.join(wt, path))
    os.makedirs(f.parent, exist_ok=True)
    with open(os.path.join(wt, path), 'w') as f:
        f.write(text)


def git_init(wt, verbose=False):
    os.chdir(wt)
    output = subprocess.run('git init'.split(), stdout=PIPE, stderr=STDOUT)
    if verbose:
        print_git_msg(output)


def git_add(wt, path, verbose=False):
    os.chdir(wt)
    output = subprocess.run(['git', 'add', path], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print_git_msg(output)


def git_commit(wt, msg, verbose=False):
    os.chdir(wt)
    output = subprocess.run(['git', 'commit', '-m', msg], stdout=PIPE, stderr=STDOUT)
    if verbose:
        print_git_msg(output)


def print_git_msg(output):
    msg = output.stdout.decode("ascii").strip()
    print("{}".format(msg))
