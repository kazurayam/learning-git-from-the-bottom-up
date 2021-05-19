"""
http://keijinsonyaban.blogspot.com/2011/05/git.html#ct3
"""

import os
import pytest
import shutil
import subprocess


@pytest.fixture(scope='module')
def manage_dir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "tmp")
    init_working_tree(base)
    yield base
    os.chdir(project_dir)


def init_working_tree(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def create_greeting(wt):
    with open(os.path.join(wt, 'greeting'), "w") as f:
        f.write("Hello, world!\n")


def test_init_working_tree(manage_dir):
    # wt stands for Working Tree
    wt = os.path.join(manage_dir, "init_working_tree")
    init_working_tree(wt)
    assert os.path.exists(wt)
    assert len(os.listdir(wt)) == 0


def test_create_a_file(manage_dir):
    wt = os.path.join(manage_dir, 'create_a_file')
    init_working_tree(wt)
    os.chdir(wt)
    create_greeting(wt)
    greeting = os.path.join(wt, 'greeting')
    assert os.path.exists(greeting)


def test_git_hashobject(manage_dir):
    wt = os.path.join(manage_dir, 'git_hash_object')
    init_working_tree(wt)
    os.chdir(wt)
    create_greeting(wt)
    out = subprocess.run('git hash-object greeting'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    hash_value = out.stdout.decode("ascii").strip()
    # print("(", hash_value, ")")
    # hash_value: af5626b4a114abcb82d63db7c8082c3c4756e51b
    assert len(hash_value) == 40


def test_introducing_the_blob(manage_dir):
    wt = os.path.join(manage_dir, 'git_init_add_commit')
    init_working_tree(wt)
    os.chdir(wt)
    create_greeting(wt)
    #
    out = subprocess.run('git init'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    msg = out.stdout.decode("ascii").strip()
    print("msg: {}".format(msg))
    #
    out = subprocess.run('git add greeting'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    msg = out.stdout.decode("ascii").strip()
    print("msg: {}".format(msg))
    #
    out = subprocess.run('git commit -m'.split() + ["Added my greeting"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    msg = out.stdout.decode("ascii").strip()
    print("msg: {}".format(msg))
    #
    out = subprocess.run('git cat-file -t af5626b'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    msg = out.stdout.decode("ascii").strip()
    assert 'blob' in msg
    #
    out = subprocess.run('git cat-file blob af5626b'.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    msg = out.stdout.decode("ascii").strip()
    assert 'Hello, world!' in msg

"""
Blobs are stored in trees
How trees are made
The beauty of commits
A commit by any other name…
Branching and the power of rebase
Index Cache: Meet the middle man
Taking the index cache farther
To reset, or not to reset
Last links in the chain: Stashing and the reflog
"""