import codecs
import json
import sys

import pygraphviz as pgv


def load_graph(couples):
    graph = pgv.AGraph(
        strict=True,
        directed=True,
        ranksep=3,
        ratio="auto",
        overlap=False,
        layout="neato",
    )

    peoples = set()
    for c in couples:
        peoples.update(c)

    for i, c in enumerate(couples):
        others = peoples - set(c)
        for p in c:
            for other in others:
                graph.add_edge(p, other)
        g_couple = graph.add_subgraph(
            c, name=f"Couple_{i}", color="blue", label=f"Couple_{i}"
        )
    return graph


def export_to_png(graph, output):
    print(graph.string())
    graph.layout()
    graph.draw(output)


def export_to_txt(graph, output):
    print(graph.string())


def load_config(conf_file):
    with codecs.open(conf_file, "r", "utf8") as fh:
        configuration = json.load(fh)
    return configuration


def help_message():
    print(f"Usage of {sys.argv[0]}:")
    print("{sys.argv[0]} <config_file_to_read>")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        help_message()
    else:
        configuration = load_config(sys.argv[1])
        g = load_graph(configuration["couple"])
        export_to_png(g, sys.argv[2])
