import collections
import re

import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from networkx import degree
from nxviz import CircosPlot
import seaborn as sns


def read_file(filename):
    try:
        df_graph_info = pd.read_csv(filename)
        return df_graph_info
    except FileNotFoundError as err:
        print(err)


def create_adjacency_list_for_graph(graph_data):
    final_adjacency_list = {}
    row, column = graph_data.shape
    for i in range(row):
        local_mapping_list = {}
        column = len(graph_data.iloc[i].dropna())
        submission_node = str(graph_data.iloc[i][str(0)]).split(',')
        submission_node = [re.sub('[\[\] \'\"]', "", item) for item in submission_node]
        local_mapping_list[submission_node[0]] = submission_node[1]
        if submission_node[1] not in final_adjacency_list.keys():
            final_adjacency_list[submission_node[1]] = []
        if column - 2 > 0:
            for j in range(1, column - 1):
                comment_node = str(graph_data.iloc[i][str(j)]).split(',')
                comment_node = [re.sub('[\[\] \'\"]', "", item) for item in comment_node]
                local_mapping_list[comment_node[0]] = comment_node[1]
                start_node = comment_node[1]
                end_node = local_mapping_list[comment_node[2]]
                if start_node in final_adjacency_list.keys():
                    node_list = final_adjacency_list[start_node]
                    if end_node not in node_list:
                        node_list.append(end_node)
                    final_adjacency_list[start_node] = node_list
                else:
                    final_adjacency_list[start_node] = [end_node]
    return final_adjacency_list


def create_graph(graph_adjacency_list):
    graph = nx.Graph()
    node_list = list(graph_adjacency_list.keys())
    graph.add_nodes_from(node_list)
    for key in graph_adjacency_list.keys():
        for item in graph_adjacency_list[key]:
            graph.add_edge(key, item)
    return graph


if __name__ == '__main__':
    file_name_1 = "cancer_praw_comments_3_2020_1_2022_Nodes.csv"
    file_name_2 = "cancer_praw_comments_3_2018_2_2020_Nodes.csv"
    graph_data_1 = read_file(file_name_1)
    graph_data_2 = read_file(file_name_2)
    adjacency_list_1 = create_adjacency_list_for_graph(graph_data_1)
    adjacency_list_2 = create_adjacency_list_for_graph(graph_data_2)
    graph_model_1 = create_graph(adjacency_list_1)
    graph_model_2 = create_graph(adjacency_list_2)
    degrees_1 = pd.DataFrame(graph_model_1.degree(), columns=['Node', 'Degree'])
    degrees_2 = pd.DataFrame(graph_model_2.degree(), columns=['Node', 'Degree'])
    degrees_1 = degrees_1[degrees_1.Node != 'None']
    degrees_2 = degrees_2[degrees_2.Node != 'None']
    degrees_1.to_csv(file_name_1 + '_degree.csv')
    degrees_2.to_csv(file_name_2 + '_degree.csv')
    try:
        file_object = open(file_name_1 + ".txt", "w")
        line = "Nodes : " + str(graph_model_1.number_of_nodes())
        file_object.write(line)
        print("Nodes: ", graph_model_1.number_of_nodes())
        line = "Edges : " + str(graph_model_1.number_of_edges())
        file_object.write(line)
        print("Edges: ", graph_model_1.number_of_edges())
        line = "Number of Component: " + str(nx.number_connected_components(graph_model_1))
        file_object.write(line)
        # print("Degree: ", graph_model.degree)
        line = "Degree of the vertice are below.\n" + str(graph_model_1.degree)
        file_object.write(line)
        file_object.close()
    except FileNotFoundError as err:
        print(err)

    a = degrees_1.loc[degrees_1.Node == "None"]
    # print(a)
    # print(degrees_1['Degree'].tolist())
    dict_data_1 = degrees_1['Degree'].value_counts().to_dict()
    lists_1 = sorted(dict_data_1.items())
    x_1, y_1 = zip(*lists_1)
    dict_data_2 = degrees_2['Degree'].value_counts().to_dict()
    lists_2 = sorted(dict_data_2.items())
    x_2, y_2 = zip(*lists_2)

    pre_mean = np.array(degrees_1['Degree'])
    post_mean = np.array(degrees_2['Degree'])

    print("Pre Pandemic Mean", np.mean(pre_mean))
    print("Mid-pandemic mean", np.mean(post_mean))
    print("pre_-pandemic median", np.median(pre_mean))
    print("Mid_median", np.median(post_mean))
    # plt.plot(x_1,y_1, label='pre-pandemic degree')
    # plt.plot(x_2,y_2, label='post-pandemic degree')
    # plt.boxplot(degrees['Degree'].tolist())
    # plt.barh(y_1,x_1)
    # plt.hist(degrees_1['Degree'].tolist(),bins=2)
    # plt.xlabel("Degree Distribution")
    # plt.ylabel("Degrees of node")
    # plt.show()
    # colors = ['g','b']
    # fig, ax1 = plt.subplots()
    # ax1.hist([degrees_1['Degree'].tolist(), degrees_2['Degree'].tolist()], color=colors, log=True, bins=10)
    # ax1.set_xlim(-50,700)
    # ax1.set_xlabel("Degree Distribution")
    # ax1.set_ylabel("Count")
    # ax1.legend(["Pre-pandemic", "Post-pandemic"])
    # plt.tight_layout()
    # plt.savefig('degree_graph.png')

    data = [degrees_1['Degree'], degrees_2['Degree']]
    fig, ax = plt.subplots()
    # Creating plot
    ax.boxplot(data,showmeans=True)
    ax.title.set_text('Degree Distribution')
    ax.set_xticklabels(["Pre-pandemic", "Mid-pandemic"])
    ax.set_ylabel("Degree Count in Log Scale")
    plt.figure(figsize=(4, 4))
    ax.set_yscale('log')

    plt.savefig('Degree_distribution_graph.png', dpi=300)
    plt.show()
    # ax = sns.boxplot(x='Degree in group', y='Count', data=degrees_1)
    # plt.show()
