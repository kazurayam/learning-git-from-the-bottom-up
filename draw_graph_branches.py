from graphviz import Digraph

# branchesのグラフをgraphvizで描いてみよう
g = Digraph("main", comment="Branching and the power of rebase")
g.attr(rankdir="RL")

c = Digraph("cluster_0")
c.attr(label="Commits", color="lightgrey")
c.node("0", "", shape="circle")
c.node("A", "A", shape="circle")
c.node("B", "B", shape="circle")
c.node("C", "C", shape="circle")
c.node("D", "D", shape="circle")
#
c.edge("A", "0", constraint="true")
c.edge("B", "A", constraint="true")
c.edge("C", "B", constraint="true")
c.edge("D", "C", constraint="true")
#
c.node("W", "W", shape="circle")
c.node("X", "X", shape="circle")
c.node("Y", "Y", shape="circle")
c.node("Z", "Z", shape="circle")
#
c.edge("W", "A", constraint="true")
c.edge("X", "W", constraint="true")
c.edge("Y", "X", constraint="true")
c.edge("Z", "Y", constraint="true")
#
b = Digraph("cluster_2")
b.attr(color="white")
b.node("MASTER", "branch: master", shape="larrow")
b.edge("MASTER", "D", label="HEAD", dir="none", constraint="true", style="dotted")
b.node("DEVELOP", "branch: develop", shape="larrow")
b.edge("DEVELOP", "Z", label="HEAD", dir="none", constraint="true", style="dotted")

g.subgraph(c)
g.subgraph(b)

print(g.source)
g.render('tmp/branches.png')
