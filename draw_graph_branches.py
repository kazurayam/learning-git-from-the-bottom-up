from graphviz import Digraph

# branchesのグラフをgraphvizで描いてみよう
g = Digraph("main", comment="Branching and the power of rebase")
g.attr(layout="dot", rankdir="RL")

c = Digraph("cluster_0")
c.attr(label="Commits", color="lightgrey")

m = Digraph("m")
m.attr(label="", color="white")
m.node("0", "", shape="circle")
m.node("A", "A", shape="circle")
m.node("B", "B", shape="circle")
m.node("C", "C", shape="circle")
m.node("D", "D", shape="circle")
#
m.edge("A", "0", constraint="true")
m.edge("B", "A", constraint="true")
m.edge("C", "B", constraint="true")
m.edge("D", "C", constraint="true")
#
c.subgraph(m)
#
d = Digraph("d")
d.attr(label="", color="white")
d.node("W", "W", shape="circle")
d.node("X", "X", shape="circle")
d.node("Y", "Y", shape="circle")
d.node("Z", "Z", shape="circle")
d.edge("W", "A", constraint="true")
d.edge("X", "W", constraint="true")
d.edge("Y", "X", constraint="true")
d.edge("Z", "Y", constraint="true")

c.subgraph(d)
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
