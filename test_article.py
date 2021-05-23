"""
http://keijinsonyaban.blogspot.com/2011/05/git.html#ct3
"""

import os
import re
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
    print("\n{}\n".format(msg))


def test_init_working_tree(basedir):
    # wt stands for Working Tree
    wt = os.path.join(basedir, "init_working_tree")
    init_dir(wt)
    assert os.path.exists(wt)
    assert len(os.listdir(wt)) == 0


def test_create_a_file(basedir):
    wt = os.path.join(basedir, 'create_a_file')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    greeting = os.path.join(wt, 'greeting')
    assert os.path.exists(greeting)


def test_git_hashobject(basedir):
    wt = os.path.join(basedir, 'git_hash_object')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    output = subprocess.run('git hash-object greeting'.split(), stdout=PIPE, stderr=STDOUT)
    hash_value = output.stdout.decode("ascii").strip()
    # print("(", hash_value, ")")
    # hash_value: af5626b4a114abcb82d63db7c8082c3c4756e51b
    assert len(hash_value) == 40


def test_introducing_the_blob(basedir):
    wt = os.path.join(basedir, 'git_init_add_commit')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
    #
    output = subprocess.run('git cat-file -t af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    msg = output.stdout.decode("ascii").strip()
    assert 'blob' in msg
    #
    output = subprocess.run('git cat-file blob af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    msg = output.stdout.decode("ascii").strip()
    assert 'Hello, world!' in msg


def test_blobs_are_stored_in_trees(basedir):
    wt = os.path.join(basedir, 'blobs_are_stored_in_trees')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
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
    output = subprocess.run('git ls-tree HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    # 100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b greeting
    msg = output.stdout.decode('ascii').strip()
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
    output = subprocess.run('git rev-parse HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    # 9429e3ec347cc51565026b3adbecd37be4f92601
    # treeオブジェクトのhash値は一定ではない。
    # タイミングによりけりでさまざまなhash値になりうる。
    output = subprocess.run('git cat-file -t HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    """commit"""
    """
    cat-fileコマンドに -t オプションを指定すると
    引数に指定されたオブジェクトの内容ではなくてオブジェクトのtypeが
    表示される。HEADは常にcommitオブジェクトだ。
    """
    output = subprocess.run('git cat-file commit HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    """
tree 0563f77d884e4f79ce95117e2d686d7d6e282887
author kazurayam <kazuaki.urayama@gmail.com> 1621389261 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1621389261 +0900
"""
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
    output = subprocess.run('git ls-tree 0563f77'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    # 100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b    greeting
    """
    わたしのリポジトリはこの時点でただひとつのcommitを含んでおり、
    このcommitは1個のblobを持つ1個のtreeを参照している。
    だから .git/objectsディレクトリのなかにオブジェクトが3個あるはずだ。
    このことをfindコマンドで確かめてみよう。
    """

    output = subprocess.run('find .git/objects -type f'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    # .git/objects/05/63f77d884e4f79ce95117e2d686d7d6e282887
    # .git/objects/54/9d175982bea318c6eba58ac5046f947f00eba8
    # .git/objects/af/5626b4a114abcb82d63db7c8082c3c4756e51b
    """
    たしかに.git/objectsのしたにオブジェクトが3つあった。
    そして3つのオブジェクトのhash値は上記の例で現れた値にほかならない。
    3つのオブジェクトがどういうtypeのオブジェクトであるか、確かめておこう。
    """
    output = subprocess.run('git cat-file -t 0563f77'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)

    # commitオブジェクトのhash値は一定でない。同じgreetingファイルをcommitしたのでも、コミットした時刻が
    # 違っていればいるからだ。だから下記のように549d175という固定文字を指定してcommitオブジェクトをcat-file
    # しようとするときっとエラーになる。だからコメントアウトした。
    # output = subprocess.run('git cat-file -t 549d175'.split(), stdout=PIPE, stderr=STDOUT)
    # msg = output.stdout.decode("ascii").strip()
    # print("\n{}\n".format(msg))
    #
    output = subprocess.run('git cat-file -t af5626b'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)

    """
    git show HEADコマンドでHEADというエリアスが指すcommitオブジェクトの
    内容を調べられる。やってみよう。
    """
    output = subprocess.run('git show HEAD'.split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    '''commit ea920998ab1630d9d92a4be618a5fdcfd428f657
Author: kazurayam <kazuaki.urayama@gmail.com>
Date:   Wed May 19 18:16:30 2021 +0900

Added my greeting

diff --git a/greeting b/greeting
new file mode 100644
index 0000000..af5626b
--- /dev/null
+++ b/greeting
@@ -0,0 +1 @@
+Hello, world!
'''
    """
    git show HEADコマンドが応答したテキストの1行目をみれば
    HEADに対応するcommitオブジェクトのhash値がわかる。そのhash値を引数として
    git cat-file commit <hash>
    を実行してみよう。そのcommitオブジェクトの中身を見ることができる。
    """
    commit_hash = output.stdout.decode("ascii").splitlines()[0].split(' ')[1]
    output = subprocess.run("git cat-file commit {}".format(commit_hash).split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)\
    """tree 0563f77d884e4f79ce95117e2d686d7d6e282887
author kazurayam <kazuaki.urayama@gmail.com> 1621417997 +0900
committer kazurayam <kazuaki.urayama@gmail.com> 1621417997 +0900

Added my greeting
    """


def test_how_trees_are_made(basedir):
    """
    blobを保持するtreeがどう作られるか、
    treeがその親となるcommitへどうリンクされるか、を見てみよう
    indexにgreetingファイルをaddすることからtreeは始まる
    """
    wt = os.path.join(basedir, 'how_trees_are_made')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    """
    まだコミットがひとつも無い時点でgit logすると失敗する
    """
    output = subprocess.run("git log".split(), stdout=PIPE, stderr=STDOUT)
    assert output.returncode is not 0
    msg = output.stdout.decode("ascii").strip()
    assert "fatal: your current branch 'master' does not have any commits yet" in msg
    # print("\n{}\n".format(msg))
    """
    git add greetingするとblobオブジェクトがひとつ作られる。
    そのblobの中身はgreetingファイルをzlibで圧縮したもの。
    そのblobの名前はgreetingファイルのSHA1ハッシュであり、af5626b..
    git addコマンドによりこのblobオブジェクトはindexに登録された状態(staged)になっている。
    """
    output = subprocess.run("git ls-files --stage".split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(output)
    msg = output.stdout.decode("ascii").strip()
    # 100644 af5626b4a114abcb82d63db7c8082c3c4756e51b 0       greeting
    assert "af5626b" in msg
    assert "greeting" in msg
    """
    .git/index というファイルがあって、そのなかにこのblobオブジェクトが
    存在していることが書かれている。
    このblobオブジェクトはまだtreeになっていない。
    git write-treeコマンドを実行すると、indexの内容をひとつの
    treeとして記録することになる。
    """
    output = subprocess.run("git write-tree".split(), stdout=PIPE, stderr=STDOUT)
    msg = output.stdout.decode("ascii").strip()
    tree_hash = msg
    """
    treeオブジェクトがひとつ作られた。そのhash値は0563f77..だ。
    """
    # print("\n{}\n".format(msg))
    # 0563f77d884e4f79ce95117e2d686d7d6e282887
    """
    このtreeオブジェクトの中身はどんな内容だろうか?
    """
    output = subprocess.run("git cat-file -p {}".format(tree_hash).split(), stdout=PIPE, stderr=STDOUT)
    # 100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b    greeting
    msg = output.stdout.decode("ascii").strip()
    assert "af5626b" in msg
    assert "greeting" in msg
    # print_git_msg(output)
    """
    みてのとおり、treeオブジェクトにはblobオブジェクトのhash値と
    元となったファイルのパスが書いてある
    
    こうやって作ったtreeオブジェクトを元にして新しいcommitオブジェクトを作ろう。
    git commit-tree <tree_hash>コマンドで
    """
    echo = subprocess.Popen(('echo', 'Initial commit'), stdout=PIPE)
    o = subprocess.run("git commit-tree {}".format(tree_hash).split(),
                            stdin=echo.stdout, stdout=PIPE, stderr=STDOUT)
    echo.wait()
    assert output.returncode is 0
    commit_hash = output.stdout.decode('ascii').strip()
    # print_git_msg(o)
    # 34236b10b84c6081389af1554c351c400bc079d9
    """
    git commit-tree <tree_hash>コマンドによってcommitオブジェクトが
    ひとつ作られる。このコマンドは作られたcommitオブジェクトのhash値をstdoutに出力する。
    
    つぎに、新しく作られたcommitを現在のブランチ(master)のHEADとして登録しよう。
    
    まずrefs/heads/masterブランチを作ろう。そのなかに最新のcommitのhash値を記録する。
    """
    # with open(os.path.join(wt, '.git/refs/heads/master'), "w") as f:
    #     f.write("{}\n".format(commit_hash))
    o = subprocess.run("git update-ref refs/heads/master {}".format(commit_hash).split(),
                            stdout=PIPE, stderr=STDOUT)
    """
    これ以降、新しいcommitを作ろうとするたび、かならず refs/heads/master に書かれた
    最終のcommitのハッシュ値を親(parent) commitとして参照しよう。親commitのhash値を
    パラメータとして渡しつつ新しいcommitを作ろう。
    こうすることで新しいcommitオブジェクトから最終commitオブジェクトへのリンクが記録される。
    時間が流れる向きを正とみれば、新しいcommitから最終commitへのリンクは逆向きである。
    
    これ以降、新しいcommitを作ったらかならず refs/heads/master に
    新しいcommitのhash値を書き込むことにしよう。これが重要だ。
    こうすることによってcommitからcommitへ連鎖する論理的なチェーンが形作られる。
    """
    """
    シンボル HEAD をmasterブランチに関連付けておこう。こうすることによりHEADを始点として
    最新のcommitから古いcommitへ連鎖をたどることができる。
    """
    o = subprocess.run("git symbolic-ref HEAD refs/heads/master".split(),
                            stdout=PIPE, stderr=STDOUT)
    """
    git logでHEADから始まるcommitの連鎖を表示することができるようになった。
    """
    o = subprocess.run("git log".split(),
                            stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    """commit db35a3b0b0cd84098ba64f11af2eae13c1087127
Author: kazurayam <kazuaki.urayama@gmail.com>
Date:   Thu May 20 11:26:20 2021 +0900

    Initial commit
    """


def test_the_beauty_of_commits(basedir):
    wt = os.path.join(basedir, 'the_beauty_of_commits')
    init_dir(wt)
    os.chdir(wt)
    write_file(wt, 'greeting', 'Hello, world!\n')
    git_init(wt)
    git_add(wt, 'greeting')
    git_commit(wt, 'Added greeting')
    """
    masterブランチのHEADつまり最新のものとして参照されているコミットを調べよう
    """
    o = subprocess.run("git branch -v".split(),
                            stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    msg = o.stdout.decode('ascii').strip()
    """
    * master 444a7a7 Added my greeting
    """
    commit_hash = msg.split()[2]
    # e.g, commit_hash == '444a7a7'
    # commitオブジェクトのhash値の先頭7桁が得られた
    assert re.match(r'\w{7}', commit_hash)

    """
    commitオブジェクトのhash値を使って
    ワーキングツリーをリセットすることができる。
    エリアスHEADはここで指定されたcommitオブジェクトを指すように変更される。
    """
    o = subprocess.run("git reset --hard".split() + [commit_hash],
                            stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    # HEAD is now at 2c495c1 Added my greeting
    """
    git reset --hard commitId はワーキングツリーのなかに現在ある
    すべての変更内容を消去する。

    commitのIDを指定してワーキングツリーを戻す方法がもうひとつある。
    git checkout だ。こちらはワーキングツリーの変更を消去しない。
    またHEADが指すcommitIDはgit checkoutによって変更されない。
    """
    o = subprocess.run("git checkout".split() + [commit_hash],
                            stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    # HEAD is now at 9b189ef Added my greeting


def test_a_commit_by_any_other_name(basedir):
    pass


def write_add_commit_file(wt, path, text, msg, verbose=False):
    write_file(wt, path=path, text=text)
    git_add(wt, path, verbose=verbose)
    git_commit(wt, msg, verbose=verbose)


def test_branching_and_the_power_of_rebase(basedir):
    wt = os.path.join(basedir, 'branching_and_the_power_of_rebase')
    init_dir(wt)
    os.chdir(wt)
    git_init(wt)
    write_add_commit_file(wt, path='greeting', text="Hello, world!\n", msg="Added greeting")
    write_add_commit_file(wt, path='A', text="Hello, A!\n", msg="Added A")
    #
    o = subprocess.run("git branch develop".split(), stdout=PIPE, stderr=STDOUT)
    o = subprocess.run("git checkout develop".split(), stdout=PIPE, stderr=STDOUT)
    #
    write_add_commit_file(wt, path='W', text="Hello, W!\n", msg="Added W")
    write_add_commit_file(wt, path='X', text="Hello, X!\n", msg="Added X")
    write_add_commit_file(wt, path='Y', text="Hello, Y!\n", msg="Added Y")
    write_add_commit_file(wt, path='Z', text="Hello, Z!\n", msg="Added Z")
    #
    o = subprocess.run("git checkout master".split(), stdout=PIPE, stderr=STDOUT)
    #
    write_add_commit_file(wt, path='B', text="Hello, B!\n", msg="Added B")
    write_add_commit_file(wt, path='C', text="Hello, C!\n", msg="Added C")
    write_add_commit_file(wt, path='D', text="Hello, D!\n", msg="Added D")
    #
    o = subprocess.run("git branch".split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    """
  develop
* master    
"""
    # `git show branch` shows branches and their commits
    o = subprocess.run("git show-branch".split(), stdout=PIPE, stderr=STDOUT)
    # print_git_msg(o)
    """
! [develop] Added Z
 * [master] Added D
--
 * [master] Added D
 * [master^] Added C
 * [master~2] Added B
+  [develop] Added Z
+  [develop^] Added y
+  [develop~2] Added X
+  [develop~3] Added W
+* [master~3] Added A
"""
    """
    git show-branchコマンドはbranchesのグラフを出力する。
    ただしグラフをフラフィックスで表示するのではなく
    すこし癖のある形式のテキストで表現する。
    --の前と--の後で二分される。
    --の前はブランチの一覧。
    --の後はコミットの履歴。履歴は下から上へ順番に読むのがよい。
    --の前において行頭の*はいま現在checkoutされているブランチであることを示す
    --の前において行頭の!はいま現在checkoutされていないその他ブランチであることを示す
    --の後において行頭の+の前にインデントがいくつあるかが重要で、
      そのcommitがどのブランチに対して行われたのかをインデントが示す。
    一番下の行がブランチングの様子を示す。master~3からdevelopブランチが
      派生したとわかる。
    """

    """
    B,C,Dでやった修正をZに取り込みたい。
    そこでmasterブランチをdevelopブランチにmergeしよう。
    """
    o = subprocess.run("git checkout develop".split(), stdout=PIPE, stderr=STDOUT)
    o = subprocess.run("git show-branch".split(), stdout=PIPE, stderr=STDOUT)
    print_git_msg(o)
    o = subprocess.run("git merge master".split(), stdout=PIPE, stderr=STDOUT)
    print_git_msg(o)
    """
    きっとコンフリクトが発生する。
    Auto-merging greeting
    CONFLICT (content): Merge conflict in greeting
    Automatic merge failed; fix conflicts and then commit the result.    
    コミットDとZが同じgreetingファイルの同じ箇所の文字を
    書きかえているので、コンフリクトが発生するのは当然。
    """








"""
A commit by any other name…
Branching and the power of rebase
Index Cache: Meet the middle man
Taking the index cache farther
To reset, or not to reset
Last links in the chain: Stashing and the reflog
"""