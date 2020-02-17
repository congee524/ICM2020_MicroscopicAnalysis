"""
the program is used to draw the passing network applying networkx
"""
import networkx as nx
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt


if __name__ == '__main__':
    pass_dir = './image/Match1.csv'
    pos_dir = './image/pos_1.csv'
    close_dir = './image/closeness.csv'
    pass_csv = pd.read_csv(pass_dir, header=0, index_col=0)
    pos_csv = pd.read_csv(pos_dir, header=0, index_col=0)
    close_csv = pd.read_csv(close_dir, header=0)
    player_name = close_csv.columns.to_list()
    pos = {}
    for i in range(11):
        pos[player_name[i]] = (pos_csv.iloc[i, 0], pos_csv.iloc[i, 1])

    G = nx.DiGraph()
    for i in range(11):
        for j in range(11):
            G.add_edge(player_name[i], player_name[j])
    close_list = close_csv.iloc[0].to_list()
    pass_net = []
    for i in range(11):
        pass_net += pass_csv.iloc[i].to_list()

    node_sizes = [i * 120 for i in close_list] # node_sizes represents the closeness of the players
    edge_colors = [i + 20 for i in pass_net] # use the color exchange to note the passing times
    edge_alphas = [0 if i == 0 else 1 for i in pass_net]
    # if there's no passing between the certain two player, the edge is invisible
    # edge_width = [i / 2 for i in pass_net]
    edge_width = 6

    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='red')
    edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                                   arrowsize=20, edge_color=edge_colors,
                                   edge_cmap=plt.cm.Blues, width=edge_width)
    # set alpha value for each edge
    for i in range(11):
        edges[i].set_alpha(edge_alphas[i])

    pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
    pc.set_array(pass_net)
    plt.colorbar(pc)

    ax = plt.gca()
    ax.set_axis_off()
    plt.show()