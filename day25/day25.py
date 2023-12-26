import operator
import re
import sys
import time
from functools import reduce


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to run.")
        return result

    return wrapper


# get current day from path and read input data
cwd = sys.argv[0]
if not ("day" in cwd):
    print("Run this from the day directory")
    sys.exit(0)
year = int(re.search("\\d{4}", cwd).group(0))
day = int(re.search("\\/day(\\d+)", cwd).group(1))
input = open(f"day{day}/input_{year}_{day}.txt", "r").read()


def part1(input):
    print(f"Part 1: {None}")
    pass


def part2(input):
    print(f"Part 2: {None}")
    pass


def print_graph(G):
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(G)  # positions for all nodes
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color="white")
    plt.show()


def print_graph_bokeh(G):
    from bokeh.io import output_notebook, show
    from bokeh.models import (
        BoxZoomTool,
        Circle,
        HoverTool,
        MultiLine,
        Plot,
        Range1d,
        ResetTool,
    )
    from bokeh.models.graphs import from_networkx
    from bokeh.palettes import Spectral4
    from bokeh.plotting import figure

    # Create a plot — set dimensions, toolbar, and title
    plot = figure(
        title="Networkx Integration Demonstration",
        x_range=(-1.1, 1.1),
        y_range=(-1.1, 1.1),
        tools="",
        toolbar_location=None,
    )

    # Create a Bokeh graph from the NetworkX input using nx.spring_layout
    graph = from_networkx(G, nx.spring_layout, scale=2, center=(0, 0))
    graph.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
    graph.edge_renderer.glyph = MultiLine(line_color="#CCCCCC", line_alpha=0.8, line_width=1)
    plot.renderers.append(graph)

    # Add tools to the plot
    plot.add_tools(HoverTool(tooltips=None), BoxZoomTool(), ResetTool())

    show(plot)


import networkx as nx

if __name__ == "__main__":

    @timer
    def find_cuts():
        return nx.minimum_edge_cut(G)

    G = nx.Graph()

    for line in input.splitlines():
        node, nodes = line.split(": ")
        nodes = nodes.split(" ")
        G.add_node(node)
        for n in nodes:
            G.add_node(n)
            G.add_edge(node, n)

    plt_graph = False

    # Option 1: visualize the graph and identify the 3 wires to cut, then cut the wires
    if plt_graph:
        print_graph(G)
        # print_graph_bokeh(G)
        G.remove_edge("btp", "qxr")
        G.remove_edge("bqq", "rxt")
        G.remove_edge("vfx", "bgl")

    # Option 2: use networkx to find the minimum edge cut
    print(cuts := find_cuts())
    for cut in cuts:
        G.remove_edge(*cut)

    components = list(nx.connected_components(G))
    for i, component in enumerate(components, start=1):
        print(f"Group {i} has {len(component)} nodes")

    print(
        f"Part 1 and only: found {len(components)} groups, with sizes {[len(c) for c in components]}. Total {reduce(operator.mul, [len(c) for c in components])}"
    )
