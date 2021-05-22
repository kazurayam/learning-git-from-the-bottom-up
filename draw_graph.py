import sys
from graphviz import Digraph

def draw_graph0():
    g = Digraph("main", comment="Branching and the power of rebase")
    g.attr('graph', layout="dot", rankdir="RL")

    c = Digraph("cluster_0")
    c.attr('graph', label="Commits", color="lightgrey")

    with c.subgraph(name="m") as m:
        m.attr(label="", color="white")
        m.node_attr.update(shape="circle")
        m.edge_attr.update(constraint="true", arrowhead="onormal")
        m.node('0', label="")
        m.edge('B', 'A', weight='2')  # to make the edge A <- B as straight as possible
        m.edges([('D', 'C'), ('C', 'B'), ('A', '0')])
        m.node('E', shape="point", style="invis")
        m.edge('E:c', 'D', dir="none", style="dotted")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white")
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.edges([('Z', 'Y'), ('Y', 'X'), ('X', 'W'), ('W', 'A')])

    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "branch: master", shape="larrow")
    b.edge("MASTER", "E:c", label="HEAD", dir="none", constraint="true", style="dotted")
    b.node("DEVELOP", "branch: develop", shape="larrow")
    b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")

    g.subgraph(c)
    g.subgraph(b)

    print(g.source)
    g.render('tmp/graph0.png')


if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 1:
        if args[1] == '0':
            draw_graph0()
        else:
            raise Exception("unknown argument: {}".format(args[1]))
    else:
        raise Exception("?") # just impossible
