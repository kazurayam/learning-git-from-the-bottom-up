import os
from helpers import basedir, init_dir, write_file, git_init, git_add, git_commit, print_git_msg
import subprocess
from subprocess import PIPE, STDOUT


def test_what_if_file_under_subdir_was_added(basedir):
    """
    fileがblobオブジェクトとして表されるのはわかった。
    basedir直下のfileについては疑問はない。
    ではサブフォルダの下にあるfileについてはどうなのか？
    というのもフォルダ（あるいはディレクトリと読んでもいいが）はblobにならないからだ。
    サブフォルダの下にあるfileをindexにaddしたとき、indexがどういう状態になるのか？
    つまりサブフォルダがindexのなかにではどう表現されるのか？
    またサブフォルダの下にあるfileの変更を含むindexをcommitしたとき、
    commitオブジェクトのなかでサブフォルダはどのように表現されるのか？

    コミットする直前のindexからcommitオブジェクトが作られる。
    indexの形とcommitオブジェクトの形が、サブフォルダをどう表現するかという点において、
    同じなのか違うのか？違うならどう違っているのか？
    """
    wt = os.path.join(basedir, 'test_what_if_file_under_subdir_was_added')
    init_dir(wt)
    os.chdir(wt)
    git_init(wt)
    write_file(wt, 'README.md', '# README please\n')
    write_file(wt, 'src/greeting', 'Hello, world!\n')
    git_add(wt, '.')
    write_file(wt, '.gitignore', '*~\n')
    write_file(wt, 'src/hello.pl', 'print(\"hello\")\n')
    git_add(wt, '.')
    # git commitする前にindexの内容をprintしよう
    # `git ls-files --stage`コマンドを実行すると、stageにファイルが4つ登録されていることがわかる
    o = subprocess.run("git ls-files --stage".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git ls-files --stage")
    print_git_msg(o)
    """
100644 b25c15b81fae06e1c55946ac6270bfdb293870e8 0       .gitignore
100644 27ac415058027193f9f7ffdc5b47a192225340d9 0       README.md
100644 af5626b4a114abcb82d63db7c8082c3c4756e51b 0       src/greeting
100644 11b15b1a4584b08fa423a57964bdbf018b0da0d5 0       src/hello.pl
"""
    # ファイルのパスが `src/greeting` のようにフォルダを含めて書かれている。
    # サブフォルダ `src` が単独でindexのなかで1行を占めていないことに注意しよう。

    # 次に `git ls-files --debug`コマンドを実行すると、stageに登録済みのファイルの詳細がわかる
    o = subprocess.run("git ls-files --debug".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git ls-files --debug")
    print_git_msg(o)
    """
.gitignore
  ctime: 1622011275:375825753
  mtime: 1622011275:375825753
  dev: 16777221 ino: 34067138
  uid: 501      gid: 20
  size: 3       flags: 0
README.md
  ctime: 1622011275:359680512
  mtime: 1622011275:359680512
  dev: 16777221 ino: 34067126
  uid: 501      gid: 20
  size: 16      flags: 0
src/greeting
  ctime: 1622011275:360260241
  mtime: 1622011275:360260241
  dev: 16777221 ino: 34067128
  uid: 501      gid: 20
  size: 14      flags: 0
src/hello.pl
  ctime: 1622011275:376391416
  mtime: 1622011275:376391416
  dev: 16777221 ino: 34067139
  uid: 501      gid: 20
  size: 15      flags: 0
"""
    # さてコミットしよう
    git_commit(wt, "initial commit")

    # masterブランチのHEADが指すcommitオブジェクトが指しているtreeオブジェクトの内容をprintしてみよう
    o = subprocess.run("git cat-file -p master^{tree}".split(), stdout=PIPE, stderr=STDOUT)
    # The master^{tree} syntax specifies the tree object that is
    # pointed to by the last commit on your master branch.
    print("\n> git cat-file -p master^{tree}")
    print_git_msg(o)
    """
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8    .gitignore
100644 blob 27ac415058027193f9f7ffdc5b47a192225340d9    README.md
040000 tree a393d373123524366b80788ba2ec12b426459279    src
"""
    # 見よ! サブフォルダ `src` に対応する1行がある。
    # "git commit"コマンドを実行したときサブフォルダ `src` に対応するtreeオブジェクトが作成されたのだ。
    # このtreeオブジェクトの中には`src`フォルダに含まれる2つのファイルに対応するblobが記録されているだろう。
    # そのことを確かめてみよう。
    for line in o.stdout.decode('ascii').splitlines():
        if line.split()[1] == 'tree':
            tree_hash = line.split()[2]
            output = subprocess.run(['git', 'cat-file', '-p', tree_hash],
                                    stdout=PIPE, stderr=STDOUT)
            print("\n> git cat-file -p {}".format(tree_hash))
            print_git_msg(output)
    """
100644 blob af5626b4a114abcb82d63db7c8082c3c4756e51b    greeting
100644 blob 11b15b1a4584b08fa423a57964bdbf018b0da0d5    hello.pl
"""
    # サブディレクトリ src に対応するtreeオブジェクトのなかで、ふたつのファイルgreetingとhello.plの
    # パスがサブディレクトリ名を除外したファイル名のみになっていることに注目しよう。
    # つじつまがちゃんと合っている。
