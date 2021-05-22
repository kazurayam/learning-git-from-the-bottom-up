import sys
from graphviz import Digraph


def draw_graph1():
    """
    ブランチングとrebaseの力 図その1
    0 <- A <- B <- C <- D
           <- W <- X <- Y <- Z
    """
    g = Digraph("main", comment="Branching and the power of rebase / graph1")
    g.attr('graph', layout="dot", rankdir="RL")
    #
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
        m.node('F', shape="point", style="invis")
        m.edge('E', 'D', dir="none", style="dotted")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white")
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.edges([('Z', 'Y'), ('Y', 'X'), ('X', 'W'), ('W', 'A')])
    #
    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "branch: master", shape="larrow")
    b.edge("MASTER", "E:c", label="HEAD", dir="none", constraint="true", style="dotted")
    b.node("DEVELOP", "branch: develop", shape="larrow")
    b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")
    #
    g.subgraph(c)
    g.subgraph(b)
    # print(g.source)
    g.render('tmp/graph1.png')


def draw_graph2():
    """
    ブランチングとrebaseの力 図その1
    0 <- A <- B <- C <- D
           <- W <- X <- Y <- Z <- Z'
    """
    g = Digraph("main", comment="Branching and the power of rebase / graph2")
    g.attr('graph', layout="dot", rankdir="RL")
    #
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
        m.edge('E', 'D', dir="none", style="dotted")
        m.node('F', shape="point", style="invis")
        m.edge('F', 'E', dir="none", style="dotted")
    with c.subgraph(name="d") as d:
        d.attr(label="", color="white")
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.edges([("Z'", 'Z'), ('Z', 'Y'), ('Y', 'X'), ('X', 'W'), ('W', 'A')])
        d.edge("Z'", 'D')
    #
    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "branch: master", shape="larrow")
    b.edge("MASTER", "F", label="HEAD", dir="none", constraint="true", style="dotted")
    b.node("DEVELOP", "branch: develop", shape="larrow")
    b.edge("DEVELOP", "Z'", label="HEAD", dir="none", constraint="true", style="dotted")
    #
    g.subgraph(c)
    g.subgraph(b)
    print(g.source)
    g.render('tmp/graph2.png')


if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 1:
        if args[1] == '1':
            draw_graph1()
        elif args[1] == '2':
            draw_graph2()
        else:
            raise Exception("unknown argument: {}".format(args[1]))
    else:
        raise Exception("?") # just impossible
