import os
import pytest
from helpers import init_dir, write_file


@pytest.fixture(scope='module')
def basedir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "tmp")
    init_dir(base)
    yield base
    os.chdir(project_dir)


def test_os_walk(basedir):
    wt = os.path.join(basedir, 'test_os_walk')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'README.md', '# README please\n')
    write_file(wt, '.gitignore', '*~\n')
    write_file(wt, 'src/greeting', 'Hello, world!\n')
    write_file(wt, 'src/hello.pl', 'print(\"hello\")\n')
    assert os.path.exists(os.path.join(wt, 'src/greeting'))
    print('\n')
    for root, dirs, files in os.walk(wt, topdown=True):
        for name in files:
            print(os.path.join(".", name))
        for name in dirs:
            print(os.path.join(".", name))
