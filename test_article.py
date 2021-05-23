def basedir():
def write_file(wt, path, text):
    with open(os.path.join(wt, path), 'w') as f:
        f.write(text)
def git_init(wt):
    os.chdir(wt)


def git_add(wt, path):
    os.chdir(wt)
    output = subprocess.run(['git', 'add', path], stdout=PIPE, stderr=STDOUT)
def git_commit(wt, msg):
    os.chdir(wt)
    output = subprocess.run(['git', 'commit', '-m', msg], stdout=PIPE, stderr=STDOUT)
def test_init_working_tree(basedir):
    wt = os.path.join(basedir, "init_working_tree")
def test_create_a_file(basedir):
    wt = os.path.join(basedir, 'create_a_file')
    write_file(wt, 'greeting', 'Hello, world!\n')
def test_git_hashobject(basedir):
    wt = os.path.join(basedir, 'git_hash_object')
    write_file(wt, 'greeting', 'Hello, world!\n')
def test_introducing_the_blob(basedir):
    wt = os.path.join(basedir, 'git_init_add_commit')
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
def test_blobs_are_stored_in_trees(basedir):
    wt = os.path.join(basedir, 'blobs_are_stored_in_trees')
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
def test_how_trees_are_made(basedir):
    wt = os.path.join(basedir, 'how_trees_are_made')
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
def test_the_beauty_of_commits(basedir):
    wt = os.path.join(basedir, 'the_beauty_of_commits')
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
def test_a_commit_by_any_other_name(basedir):
def test_branching_and_the_power_of_rebase(basedir):
    wt = os.path.join(basedir, 'branching_and_the_power_of_rebase')
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
    write_file(wt, path='greeting', text='Hello, a!\n')
    write_file(wt, path='greeting', text='Hello, w!\n')
    write_file(wt, path='greeting', text='Hello, x!\n')
    write_file(wt, path='greeting', text='Hello, y!\n')
    write_file(wt, path='greeting', text='Hello, z!\n')
    write_file(wt, path='greeting', text='Hello, b!\n')
    write_file(wt, path='greeting', text='Hello, c!\n')
    write_file(wt, path='greeting', text='Hello, d!\n')