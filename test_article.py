"""
http://keijinsonyaban.blogspot.com/2011/05/git.html#ct3
"""

import os
import pytest
import shutil
import subprocess
from subprocess import PIPE, STDOUT


@pytest.fixture(scope='module')
def manage_dir():
    project_dir = os.getcwd()
    base = os.path.join(project_dir, "tmp")
    init_dir(base)
    yield base
    os.chdir(project_dir)


def init_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def create_greeting(wt):
    with open(os.path.join(wt, 'greeting'), "w") as f:
        f.write("Hello, world!\n")


def test_init_working_tree(manage_dir):
    # wt stands for Working Tree
    wt = os.path.join(manage_dir, "init_working_tree")
    init_dir(wt)
    assert os.path.exists(wt)
    assert len(os.listdir(wt)) == 0


def test_create_a_file(manage_dir):
    wt = os.path.join(manage_dir, 'create_a_file')
    init_dir(wt)
    os.chdir(wt)
    create_greeting(wt)
    greeting = os.path.join(wt, 'greeting')
    assert os.path.exists(greeting)


def test_git_hashobject(manage_dir):
    wt = os.path.join(manage_dir, 'git_hash_object')
    init_dir(wt)
    os.chdir(wt)
    create_greeting(wt)
    out = subprocess.run('git hash-object greeting'.split(), stdout=PIPE, stderr=STDOUT)
    hash_value = out.stdout.decode("ascii").strip()
    # print("(", hash_value, ")")
    # hash_value: af5626b4a114abcb82d63db7c8082c3c4756e51b
    assert len(hash_value) == 40


def commit_greeting():
    out = subprocess.run('git init'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("msg: {}".format(msg))
    out = subprocess.run('git add greeting'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("msg: {}".format(msg))
    out = subprocess.run('git commit -m'.split() + ["Added my greeting"], stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("msg: {}".format(msg))


def test_introducing_the_blob(manage_dir):
    wt = os.path.join(manage_dir, 'git_init_add_commit')
    init_dir(wt)
    os.chdir(wt)
    create_greeting(wt)
    #
    commit_greeting()
    #
    out = subprocess.run('git cat-file -t af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    assert 'blob' in msg
    #
    out = subprocess.run('git cat-file blob af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    assert 'Hello, world!' in msg


def test_blobs_are_stored_in_trees(manage_dir):
    wt = os.path.join(manage_dir, 'blobs_are_stored_in_trees')
    init_dir(wt)
    os.chdir(wt)
    create_greeting(wt)
    #
    commit_greeting()
    #
    """
    Gitはファイルの構造と名前を表現するために、blobをtreeへ
    leaf nodeとしてくっつける。とてもたくさんのtreeがあるだろう。
    どのtreeに目的のblobがあるのかを見つけることは難しい。しかし
    さっき作ったblobをポイントするtreeは、たった今つくったcommit
    つまりHEADが保持しているtreeのなかにあるはずだ。だから
    git ls-tree HEAD
    とやれ。するとgreetingファイルのblobをポイントするtreeが
    みつかるはずだ。
    """
    out = subprocess.run('git ls-tree HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # 100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b greeting
    """
    このコミットはgreetingをリポジトリに追加したことを記録している。
    このコミットはtreeをひとつ含み、そのtreeはleaf nodeをひとつ持っている。
    そのleaf nodeはgreetingのblobを指している。
    """
    assert '100644' in msg
    assert 'blob' in msg
    assert 'af5626b4a114abcb82d63db7c8082c3c4756e51b' in msg
    assert 'greeting' in msg
    #
    """上記のようにgit ls-tree HEADを実行することにより
    HEADコミットによって参照されているtreeの内容を見ることができた。
    しかしそのtreeがどういう名前でレポジトリに存在しているかはまだ
    見ることができていない。git rev-parse HEADを実行することで
    treeオブジェクトを見つけることができる。
    """
    out = subprocess.run('git rev-parse HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # 9429e3ec347cc51565026b3adbecd37be4f92601
    # treeオブジェクトのhash値は一定ではない。
    # タイミングによりけりでさまざまなhash値になりうる。
    out = subprocess.run('git cat-file -t HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # commit
    """
    cat-fileコマンドに -t オプションを指定すると
    引数に指定されたオブジェクトの内容ではなくてオブジェクトのtypeが
    表示される。HEADは常にcommitオブジェクトだ。
    """
    out = subprocess.run('git cat-file commit HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # tree 0563f77d884e4f79ce95117e2d686d7d6e282887
    # author kazurayam <kazuaki.urayama@gmail.com> 1621389261 +0900
    # committer kazurayam <kazuaki.urayama@gmail.com> 1621389261 +0900
    """
    git cat-file commit HEADは、HEADというエリアスが指している
    commitオブジェクトの内容を表示する。上記の例ではこのcommitには
    treeオブジェクトが１つだけ含まれていてそのtreeのhash値は0563..である。
    ひとつのコミットにtreeオブジェクトが２つ以上含まれることもざらにある。
    commitオブジェクトにはそのcommitを作った人の名前とコミットを作成した
    日時も記録されている。名前と日時が可変なので、commitオブジェクトの
    hash値はさまざまな値をとりうる。
    
    いっぽうtreeオブジェクトのhash値(上記の例では 0563f77..)は
    一定だ。なぜ一定なのか？treeオブジェクトのhash値はtreeオブジェクト
    の中身によって決まる。いまみているtreeオブジェクトの中身は下記のとおりだ。
    `100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b greeting`
    ファイルを同じ名前(greeting)にして同じ内容を書き込んだなら、
    greetingファイルのblobのhash値が同一になるはずで、
    その結果としてtreeオブジェクトのhashは一定になる。
    
    hash値が0563f77..であるオブジェクトがたしかにHEADが指している
    treeオブジェクトであることを確かめてみよう。
    """
    out = subprocess.run('git ls-tree 0563f77'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # 100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b    greeting
    """
    わたしのリポジトリはこの時点でただひとつのcommitを含んでおり、
    このcommitは1個のblobを持つ1個のtreeを参照している。
    だから .git/objectsディレクトリのなかにオブジェクトが3個あるはずだ。
    このことをfindコマンドで確かめてみよう。
    """

    out = subprocess.run('find .git/objects -type f'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    # .git/objects/05/63f77d884e4f79ce95117e2d686d7d6e282887
    # .git/objects/54/9d175982bea318c6eba58ac5046f947f00eba8
    # .git/objects/af/5626b4a114abcb82d63db7c8082c3c4756e51b
    """
    たしかに.git/objectsのしたにオブジェクトが3つあった。
    そして3つのオブジェクトのhash値は上記の例で現れた値にほかならない。
    3つのオブジェクトがどういうtypeのオブジェクトであるか、確かめておこう。
    """
    out = subprocess.run('git cat-file -t 0563f77'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))

    # commitオブジェクトのhash値は一定でない。同じgreetingファイルをcommitしたのでも、コミットした時刻が
    # 違っていればいるからだ。だから下記のように549d175という固定文字を指定してcommitオブジェクトをcat-file
    # しようとするときっとエラーになる。だからコメントアウトした。
    # out = subprocess.run('git cat-file -t 549d175'.split(), stdout=PIPE, stderr=STDOUT)
    # msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    #
    out = subprocess.run('git cat-file -t af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    msg = out.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))








"""
How trees are made
The beauty of commits
A commit by any other name…
Branching and the power of rebase
Index Cache: Meet the middle man
Taking the index cache farther
To reset, or not to reset
Last links in the chain: Stashing and the reflog
"""