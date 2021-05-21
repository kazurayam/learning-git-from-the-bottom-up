from graphviz import Digraph

# このグラフをgraphvizで描いてみよう
g = Digraph("main", comment="Branching and the power of rebase")
g.attr(rankdir="RL")
g.node("0", "", shape="circle")

m = Digraph("master")
m.node("A", "A", shape="circle")
m.node("B", "B", shape="circle")
m.node("C", "C", shape="circle")
m.node("D", "D", shape="circle")
m.edge("A", "0", constraint="true")
m.edge("B", "A", constraint="true")
m.edge("C", "B", constraint="true")
m.edge("D", "C", constraint="true")

d = Digraph("develop")
d.node("W", "W", shape="circle")
d.node("X", "X", shape="circle")
d.node("Y", "Y", shape="circle")
d.node("Z", "Z", shape="circle")
d.edge("W", "A", constraint="true")
d.edge("X", "W", constraint="true")
d.edge("Y", "X", constraint="true")
d.edge("Z", "Y", constraint="true")

b = Digraph("branches")
b.node("MASTER", "branch: master", shape="larrow")
b.edge("MASTER", "D", label="HEAD", dir="none", constraint="true", style="dotted")
b.node("DEVELOP", "branch: develop", shape="larrow")
b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")

g.subgraph(m)
g.subgraph(d)
g.subgraph(b)

print(g.source)
g.render('tmp/branches.png')
