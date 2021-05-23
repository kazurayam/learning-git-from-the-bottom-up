import sys
from graphviz import Digraph


def draw_graph1():
    """
    ブランチングとrebaseの力 図その1
    0 <- A <- B <- C <- D ======== master
           <- W <- X <- Y <- Z === develop
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
        m.node('A', label="A")
        m.node('B', label="B")
        m.node('C', label="C")
        m.node('D', label="D")
        m.node('E', shape="point", style="invis")
        m.edge('A', '0')
        m.edge('B', 'A', weight='2')  # to make the edge A <- B as straight as possible
        m.edge('C', 'B')
        m.edge('D', 'C')
        m.edge('E', 'D', dir="none", style="dotted")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white")
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.node('W', label="W")
        d.node('X', label="X")
        d.node('Y', label="Y")
        d.node('Z', label="Z")
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
    0 <- A <- B <- C <- D ============== master
           <- W <- X <- Y <- Z <- Z' === develop
    """
    g = Digraph("main", comment="Branching and the power of rebase / graph2")
    g.attr('graph', layout="dot", rankdir="RL")

    c = Digraph("cluster_0")
    c.attr('graph', label="Commits", color="lightgrey")
    with c.subgraph(name="m") as m:
        m.attr(label="", color="white", ranksep="0.2")
        m.node_attr.update(shape="circle")
        m.edge_attr.update(constraint="true", arrowhead="onormal")
        m.node('0', label="")
        m.node('A', label="A")
        m.node('B', label="B")
        m.node('C', label="C")
        m.node('D', label="D")
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
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.node('W', label="W")
        d.node('X', label="X")
        d.node('Y', label="Y")
        d.node('Z', label="Z")
        d.node("M", shape="doublecircle", label="merge")
        d.edge('W', 'A')
        d.edge('X', 'W')
        d.edge('Y', 'X')
        d.edge('Z', 'Y')
        d.edge("M", 'Z')
        d.edge("M", 'D')

    #
    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "master", shape="larrow")
    b.edge("MASTER", "F", label="HEAD", dir="none", constraint="true", style="dotted")
    b.node("DEVELOP", "develop", shape="larrow")
    b.edge("DEVELOP", "W", label="HEAD~3", dir="none", constraint="true", style="dotted")
    b.edge("DEVELOP", "M", label="HEAD", dir="none", constraint="true", style="dotted")
    #
    g.subgraph(c)
    g.subgraph(b)
    print(g.source)
    g.render('tmp/graph2.png')


def draw_graph3():
    """
    ブランチングとrebaseの力
    0 <- A <- B <- C <- D ======================== master
                           <- W <- X <- Y <- Z === develop
    """
    g = Digraph("main", comment="Branching and the power of rebase / graph3")
    g.attr('graph', layout="dot", rankdir="RL")

    c = Digraph("cluster_0")
    c.attr('graph', label="Commits", color="lightgrey")
    with c.subgraph(name="m") as m:
        m.attr(label="", color="white", ranksep="0.2")
        m.node_attr.update(shape="circle")
        m.edge_attr.update(constraint="true", arrowhead="onormal")
        m.node('0', label="")
        m.node('A', label="A")
        m.node('B', label="B")
        m.node('C', label="C")
        m.node('D', label="D")
        m.node('E', shape="point", style="invis")
        m.node('F', shape="point", style="invis")
        m.node('G', shape="point", style="invis")
        m.node('H', shape="point", style="invis")
        m.edge('A', '0')
        m.edge('B', 'A', weight='2')  # to make the edge A <- B as straight as possible
        m.edge('C', 'B')
        m.edge('D', 'C')
        m.edge('E', 'D', dir="none", style="dotted", weight="2")
        m.edge('F', 'E', dir="none", style="dotted", weight="2")
        m.edge('G', 'F', dir="none", style="dotted", weight="2")
        m.edge('H', 'G', dir="none", style="dotted", weight="2")

    with c.subgraph(name="d") as d:
        d.attr(label="", color="white", ranksep="0.2")
        d.node_attr.update(shape="circle")
        d.edge_attr.update(constraint="true", arrowhead="onormal")
        d.node('W', label="W")
        d.node('X', label="X")
        d.node('Y', label="Y")
        d.node('Z', label="Z")
        d.edge('W', 'D')
        d.edge('X', 'W')
        d.edge('Y', 'X')
        d.edge('Z', 'Y')

#
    b = Digraph("cluster_b")
    b.attr(color="white")
    b.node("MASTER", "master", shape="larrow")
    b.edge("MASTER", "H", label="HEAD", dir="none", constraint="true", style="dotted", weight="2")
    b.node("DEVELOP", "develop", shape="larrow")
    b.edge("DEVELOP", "W", label="HEAD~3", dir="none", constraint="true", style="dotted")
    b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")
    #
    g.subgraph(c)
    g.subgraph(b)
    print(g.source)
    g.render('tmp/graph3.png')



if __name__ == "__main__":
    args = sys.argv
    if len(args) >= 1:
        if args[1] == '1':
            draw_graph1()
        elif args[1] == '2':
            draw_graph2()
        elif args[1] == '3':
            draw_graph3()
        else:
            raise Exception("unknown argument: {}".format(args[1]))
    else:
        raise Exception("?") # just impossible
