Learning Git from the bottom up
=======

Reading
- [Git from the bottom up, John Wiegley](http://newartisans.com/2008/04/git-from-the-bottom-up/)
- 日本語訳 [Git をボトムアップから理解する](http://keijinsonyaban.blogspot.com/2011/05/git.html#ct3)

while I wrote a series of pytest codes with file name of `*-test.py` to reproduce the sample interactions with Git.



https://forum.graphviz.org/t/dot-more-layout-control/586


# Python実行環境を整える

このりpygraphvisをインストールする。

大筋において https://github.com/kazurayam/MyPythonProjectTemplate に書いてある手順に従う。

Macにpyenvがインストールする。

pyenvでanaccondaをインストールする。

pipenvでlearning-git-from-the-bottom-upプロジェクトのためにPython仮想環境を作る。

```
$ cd learning-git-from-the-bottom-up
$ pipenv --python 3
```

Python仮想環境がどのパスに作られたかを確認するにはこうする
```
$ cd learning-git-from-the-bottom-up
$ 

```

仮想環境のなかにpytestとpygraphvizをインストールする。

```
$ cd learning-git-from-the-bottom-up
$ pipenv install --dev pytest
$ pipenv install --dev graphviz
```

IntelliJ IDEAに設定を加える。前に作ったPython仮想環境をPythoon SDKとしてIDEAに登録する。そしてIDEAで開いたlearning-git-from-the-bottom-upプロジェクトがそのPython SDKを参照して動くようにする。



