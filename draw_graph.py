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
        m.node_attr.update(shape="oval")
        m.edge_attr.update(constraint="true", arrowhead="onormal")
        m.node('0', label="")
        m.node('A', label="add A")
        m.node('B', label="add B")
        m.node('C', label="add C")
        m.node('D', label="add D")
        m.node('E', shape="point", style="invis")
        m.edge('A', '0')
        m.edge('B', 'A', weight='2')  # to make the edge A <- B as straight as possible
        m.edge('C', 'B')
        m.edge('D', 'C')
        m.edge('E', 'D', dir="none", style="dotted")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white")
        d.node_attr.update(shape="oval")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.node('W', label="add W")
        d.node('X', label="add X")
        d.node('Y', label="add Y")
        d.node('Z', label="add Z")
        d.edge('W', 'A')
        d.edge('X', 'W')
        d.edge('Y', 'X')
        d.edge('Z', 'Y')

    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "master", shape="larrow")
    b.edge("MASTER", "E:c", label="HEAD", dir="none", constraint="true", style="dotted")
    b.node("DEVELOP", "develop", shape="larrow")
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

    c = Digraph("cluster_0")
    c.attr('graph', label="Commits", color="lightgrey")
    with c.subgraph(name="m") as m:
        m.attr(label="", color="white", ranksep="0.2")
        m.node_attr.update(shape="oval")
        m.edge_attr.update(constraint="true", arrowhead="onormal")
        m.node('0', label="")
        m.node('A', label="add A")
        m.node('B', label="add B")
        m.node('C', label="add C")
        m.node('D', label="add D")
        m.node('E', shape="point", style="invis")
        m.node('F', shape="point", style="invis")
        m.edge('A', '0')
        m.edge('B', 'A', weight='2')  # to make the edge A <- B as straight as possible
        m.edge('C', 'B')
        m.edge('D', 'C')
        m.edge('E', 'D', dir="none", style="dotted")
        m.edge('F', 'E', dir="none", style="dotted")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white", ranksep="0.2")
        d.node_attr.update(shape="oval")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.node('W', label="add W")
        d.node('X', label="add X")
        d.node('Y', label="add Y")
        d.node('Z', label="add Z")
        d.node("Z'", label="merge\nmaster")
        d.edge('W', 'A')
        d.edge('X', 'W')
        d.edge('Y', 'X')
        d.edge('Z', 'Y')
        d.edge("Z'", 'Z')
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
