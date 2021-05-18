import os
import pytest
import shutil


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
    wt = os.path.join(manage_dir, 'test_create_a_file')
    init_working_tree(wt)
    os.chdir(wt)
    os.system('echo "Hello, world!" > greeting')
    assert os.path.exists(os.path.join(wt, 'greeting'))
