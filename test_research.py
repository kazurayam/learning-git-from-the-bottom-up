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
    write_file(wt, '.gitignore', '*~\n')
    write_file(wt, 'src/greeting', 'Hello, world!\n')
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
    # ファイルのパスが `src/greeting` のようにフォルダを含めて書かれている。いいかえれば
    # サブフォルダ `src` が単独でindexのなかで1行を占めるということがない。このことに注意しよう。
    # この4行はいづれもblobオブジェクトだ。

    # さてコミットしよう
    git_commit(wt, "initial commit")

    # masterブランチのHEADが指すcommitオブジェクトそれ自体の内容をprintしてみよう
    o = subprocess.run("git cat-file -p HEAD".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git cat-file -p HEAD")
    print_git_msg(o)

    # masterブランチのHEADが指すcommitオブジェクトが指しているtreeオブジェクトの内容をprintしてみよう
    tree_hash = o.stdout.decode('ascii').splitlines()[0].split()[1]
    o = subprocess.run(['git', 'cat-file', '-p', tree_hash], stdout=PIPE, stderr=STDOUT)
    # o = subprocess.run("git cat-file -p master^{tree}".split(), stdout=PIPE, stderr=STDOUT)
    # The master^{tree} syntax specifies the tree object that is
    # pointed to by the last commit on your master branch.
    print("\n> git cat-file -p {}".format(tree_hash))
    print_git_msg(o)
    """
100644 blob b25c15b81fae06e1c55946ac6270bfdb293870e8    .gitignore
100644 blob 27ac415058027193f9f7ffdc5b47a192225340d9    README.md
040000 tree a393d373123524366b80788ba2ec12b426459279    src
"""
    # 見よ!
    # サブフォルダ `src` に対応する1行がある。それはblobオブジェクトではなくてtreeオブジェクトだ。
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
    # indexにはblobオブジェクトが4つあった。
    # git commitを実行したらcommitオブジェクト1つができた。
    # そしてtreeオブジェクトが2つできた。
    # ひとつは ./README.md ファイルが位置する ルートのフォルダに対応するtreeで、
    # もうひとつは ./src/greeting ファイルが位置するサブフォルダ src に対応するtreeだ。
    # commitオブジェクトはルートフォルダに対応するtreeへリンクし、
    # ルートフォルダに対応するtreeオブジェクトからsrcフォルダに対応するtreeオブジェクトへ
    # リンクが形成される。
    # そして4つのblobはそれぞれファイルが属するフォルダに対応するtreeオブジェクトからリンクされる。
    # けっきょくcommitオブジェクトからtreeノードの連鎖を経由して4つのblobへアクセスする
    # のに必要な情報が保持されていることがわかる。

    # srcディレクトリの名前をsourceに変更してみよう。何が起こるだろうか？
    print("> mv src source")
    os.rename("src", "source")
    git_add(wt, '.')

    # git commitする前にindexの内容をprintしよう
    # `git ls-files --stage`コマンドを実行すると、stageにファイルが4つ登録されていることがわかる
    o = subprocess.run("git ls-files --stage".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git ls-files --stage")
    print_git_msg(o)
    """
100644 b25c15b81fae06e1c55946ac6270bfdb293870e8 0       .gitignore
100644 27ac415058027193f9f7ffdc5b47a192225340d9 0       README.md
100644 af5626b4a114abcb82d63db7c8082c3c4756e51b 0       source/greeting
100644 11b15b1a4584b08fa423a57964bdbf018b0da0d5 0       source/hello.pl
"""
    # なぜなら
    # ここで git status コマンドを実行してみよう。今回の変更点が絞り込まれて表示される。
    o = subprocess.run("git status".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git status")
    print_git_msg(o)
    """
On branch master
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        renamed:    src/greeting -> source/greeting
        renamed:    src/hello.pl -> source/hello.pl
"""
    # indexをcat-fileしたなかにsource/greetingのblobとsource/hello.plのblobが
    # 含まれているのは当然だとおもう。だってgit statusにそう表示されるくらいなのだから。
    # ところがindexをよくみると、今回変更しなかった .gitignore と README.md のblob
    # も含まれている。僕は驚いた。
    # git statusコマンドはindexに単純にprintしているのではなかった。
    #
    # ひとつのindexのなかにはgit addコマンドが実行された時点において、ワーキングツリーの
    # なかに存在していたすべてのファイルのblobのhash値が列挙されるのだ。ワーキングツリーの
    # なかにファイルが1000個あったら、git addコマンドを実行するとindexは1000個分の
    # blobが列挙されるのだ。
    # git statusコマンドを実行したとき added xxxx とか renamed yyyy -> zzzz という
    # メッセージがほんの数行応答された場合でも、indexをcat-fileしてみると1000個分のblob
    # がそこに列挙されているのだ。
    # こうなっているとは、僕はいまのいままで知らなかった。

    # Gitの内幕がみえてきた。おっとビックリです。



    # ええい、先に進もう。commitしてしまえ。
    git_commit(wt, "renamed the src directory to source")

    # masterブランチのHEADが指すcommitオブジェクトそれ自体の内容をprintしてみよう
    o = subprocess.run("git cat-file -p HEAD".split(), stdout=PIPE, stderr=STDOUT)
    print("\n> git cat-file -p HEAD")
    print_git_msg(o)

    # masterブランチのHEADが指すcommitオブジェクトが指しているtreeオブジェクトの内容をprintしてみよう
    tree_hash = o.stdout.decode('ascii').splitlines()[0].split()[1]
    o = subprocess.run(['git', 'cat-file', '-p', tree_hash], stdout=PIPE, stderr=STDOUT)
    print("\n> git cat-file -p {}".format(tree_hash))
    print_git_msg(o)
    """

"""
