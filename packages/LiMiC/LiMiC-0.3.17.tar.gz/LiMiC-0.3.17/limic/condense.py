IN = (("file_name_in",),{'type':str,'help':"read map data from cache file CACHE",'metavar':'CACHE'})
OUT = (("file_name_out",),{'type':str,'help':"save extracted graph to file GRAPH",'metavar':'GRAPH'})    

CONFIG = [IN,OUT]

def condense_edges(g):
    from networkx import Graph, connected_components
    num2nodes = {}
    for n in g.nodes():
        ns = list(g.neighbors(n))
        nn = len(ns)
        num2nodes.setdefault(nn,[]).append(n)
    add_edges = []
    node2closest = {}
    for k,v in num2nodes.items():
        if k > 2:
            for n in v:
                ns = list(g.neighbors(n))
                for m in ns:
                    path = [n,m]
                    cost = g[n][m]['weight']
                    to_map = []
                    while True:
                        ls = list(g.neighbors(path[-1]))
                        ln = len(ls)
                        if ln < 2:
                            assert(ln==1 and ls[0] == path[-2])
                            to_map.append(path[-1])
                            sg = g.subgraph(path).copy()
                            break
                        if ln == 2:
                            ls.remove(path[-2])
                            assert(len(ls)==1)
                            to_map.append(path[-1])
                            if ls[0] == path[0]:
                                sg = g.subgraph(path).copy()
                                break
                            else:
                                path = list(path)
                                path.append(ls[0])
                                cost += g[path[-2]][path[-1]]['weight']
                        elif ln > 2:
                            if path[0] != path[-1]:
                                sg = g.subgraph(path).copy()
                                add_edges.append((path[0],path[-1],cost,0,sg))
                            break
                    for u in to_map:
                        node2closest.setdefault(u,[]).append((n,sg,cost))
    nodes = []
    nodes.extend(num2nodes.get(0,[]))
    nodes.extend(u for u in num2nodes.get(1,[]) if u not in node2closest)
    nodes.extend(u for u in num2nodes.get(2,[]) if u not in node2closest)
    h = g.subgraph(nodes).copy()
    (h.add_nodes_from(v) for k,v in num2nodes.items() if k > 2)
    for u,v,w,t,p in add_edges:
        h.add_edge(u,v,weight=w,type=t,path=p)
    cs = [h.subgraph(c).copy() for c in connected_components(h)]
    node2c = {u:c for c in cs for u in c.nodes()}
    return cs, node2closest, node2c

def condense(file_name_in,file_name_out):
    from limic.util import start, end, file_size, status, save_pickled, load_pickled, check_overwrite
    if not check_overwrite(file_name_in,file_name_out):
        return
    start("Loading from",file_name_in)
    g = load_pickled(file_name_in)
    end('')
    file_size(file_name_in)
    start("Condensing edges")
    h = condense_edges(g)
    end()
    start("Saving to",file_name_out)
    save_pickled(file_name_out,h)
    end('')
    file_size(file_name_out)
