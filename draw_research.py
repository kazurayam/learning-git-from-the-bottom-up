import sys
from graphviz import Digraph


def draw_research0():
    g = Digraph("main", comment="elbow joint edges example")
    g.attr('graph', layout="dot", rank="max", rankdir="LR", splines="ortho")
    g.node_attr.update(fontname="arial", fontsize="10")
    g.edge_attr.update(constraint="true", arrowhead="onormal")
    with g.subgraph(name="cluster_workingtree") as w:
        w.attr(label="working tree", style="dotted", color="grey")
        w.node_attr.update(shape="rectangle", height="0.2")
        w.node("D_basedir", "./", shape="folder")
        w.node("D_basedir_cp", "", shape="point", width="0")
        w.node("F_hello.pl", "hello.pl")
        w.node("F_greeting", "greeting")
        w.node("D_src", "src/", shape="folder")
        w.node("D_src_cp", "", shape="point", width="0")
        w.node("F_123", "123")
        w.node("F_LICENSE", "LICENSE")
        w.node("F_README", "README")
        w.node("F_gitignore", ".gitignore")
        w.edge("D_basedir", "D_basedir_cp", arrowhead="none")
        w.edge("D_basedir_cp", "F_gitignore:w")
        w.edge("D_basedir_cp", "F_README:w")
        w.edge("D_basedir_cp", "D_src:w")
        w.edge("D_basedir_cp", "F_LICENSE:w")
        w.edge("D_basedir_cp", "F_123:w")
        w.edge("D_src", "D_src_cp:w", arrowhead="none")
        w.edge("D_src_cp", "F_greeting:w")
        w.edge("D_src_cp", "F_hello.pl:w")


    print(g.source)
    g.render('tmp/research0', format='png')
    g.render('tmp/research0', format="pdf")


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        draw_research0()
