import os
import pytest
import shutil
import subprocess


@pytest.fixture(scope='module')
def manage_dir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "tmp")
    yield base
    os.chdir(project_dir)


def init_working_tree(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def test_init_working_tree(manage_dir):
    wt = os.path.join(manage_dir, "test_init_working_tree")
    init_working_tree(wt)
    assert os.path.exists(wt)
    assert len(os.listdir(wt)) == 0


def test_create_a_file(manage_dir):
    wt = os.path.join(manage_dir, 'create_a_file')
    init_working_tree(wt)
    os.chdir(wt)
    greeting = os.path.join(wt, 'greeting')
    with open(greeting, "w") as f:
        f.write("Hello, world")
    assert os.path.exists(greeting)


def test_git_hash_object(manage_dir):
    wt = os.path.join(manage_dir, 'git_hash_object')
    init_working_tree(wt)
    os.chdir(wt)
    with open(os.path.join(wt, 'greeting'), "w") as f:
        f.write("Hello, world")
    out = subprocess.run('git hash-object greeting'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    hash_value = out.stdout.decode("ascii").strip()
    print(hash_value)
    assert len(hash_value) == 40
