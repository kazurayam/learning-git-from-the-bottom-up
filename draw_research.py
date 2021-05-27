import sys
from graphviz import Digraph


def draw_research0():
    g = Digraph("main", comment="What is the Index in Git")
    g.attr('graph', layout="dot", rank="max", rankdir="LR", splines="ortho")
    g.edge_attr.update(constraint="true", arrowhead="onormal")

    with g.subgraph(name="cluster_workingtree") as w:
        w.attr(label="working tree", style="dotted", color="grey")
        w.node_attr.update(shape="rectangle", width="0.5")
        w.node("D_basedir", "basedir", shape="folder")
        w.node("F_gitignore", ".gitignore", group="a")
        w.node("F_README", "README", group="a")
        w.node("D_src", "src", shape="folder", group="a")
        w.node("F_greeting", "greeting", group="b")
        w.node("F_hello.pl", "hello.pl", group="b")
        w.edge("D_basedir", "F_gitignore:w")
        w.edge("D_basedir", "F_README:w")
        w.edge("D_basedir", "D_src:w")
        w.edge("D_src", "F_greeting:w")
        w.edge("D_src", "F_hello.pl:w")


    print(g.source)
    g.render('tmp/research0')


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        draw_research0()
