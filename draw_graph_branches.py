from graphviz import Digraph

# branchesのグラフをgraphvizで描いてみよう
g = Digraph("main", comment="Branching and the power of rebase")
g.attr(layout="dot", rankdir="RL")

c = Digraph("cluster_0")
c.attr(label="Commits", color="lightgrey")

with c.subgraph(name="m") as m:
    m.attr(label="", color="white")
    m.node_attr.update(shape="circle")
    m.edge_attr.update(constraint="true", arrowhead="onormal")
    m.edges([('D', 'C'), ('C', 'B'), ('B', 'A'), ('A', '0')])

with c.subgraph(name="d") as d:
    d.attr(label="", color="white")
    d.node_attr.update(shape="circle")
    d.edge_attr.update(constraint="true", arrowhead="onormal")
    d.edges([('Z', 'Y'), ('Y', 'X'), ('X', 'W'), ('W', 'A')])
#
b = Digraph("cluster_b")
b.attr(color="white")
b.node("MASTER", "branch: master", shape="larrow")
b.edge("MASTER", "D", label="HEAD", dir="none", constraint="true", style="dotted")
b.node("DEVELOP", "branch: develop", shape="larrow")
b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")

g.subgraph(c)
g.subgraph(b)

print(g.source)
g.render('tmp/branches.png')
