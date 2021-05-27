import sys
from graphviz import Digraph


def draw_research0():
    g = Digraph("main", comment="What is the Index in Git")
    g.attr('graph', layout="dot", rank="max", rankdir="LR", splines="ortho")
    g.node_attr.update(fontname="arial", fontsize="10")
    g.edge_attr.update(constraint="true", arrowhead="onormal")
    with g.subgraph(name="cluster_workingtree") as w:
        w.attr(label="working tree", style="dotted", color="grey")
        w.node_attr.update(shape="rectangle", height="0.2")
        w.node("D_basedir", "./", shape="folder")

        w.node("F_hello.pl", "hello.pl")
        w.node("F_greeting", "greeting")
        w.node("D_src", "src/", shape="folder")
        w.node("F_1", "1")
        w.node("F_LICENSE", "LICENSE")
        w.node("F_README", "README")
        w.node("F_gitignore", ".gitignore")

        w.edge("D_basedir", "F_gitignore:w")
        w.edge("D_basedir", "F_README:w")
        w.edge("D_basedir", "D_src:w")
        w.edge("D_basedir", "F_LICENSE:w")
        w.edge("D_basedir", "F_1:w")
        w.edge("D_src", "F_greeting:w")
        w.edge("D_src", "F_hello.pl:w")


    print(g.source)
    g.render('tmp/research0')


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        draw_research0()
