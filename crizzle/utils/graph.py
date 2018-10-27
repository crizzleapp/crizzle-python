import cv2
import logging
import numpy as np
from scipy.sparse import csgraph

logger = logging.getLogger(__name__)
np.set_printoptions(edgeitems=22, precision=4, linewidth=200)


def floyd_warshall(graph):
    assert graph.shape[0] == graph.shape[1]
    num_nodes = graph.shape[0]
    graph = np.copy(graph)
    np.fill_diagonal(graph, 0)
    graph[np.isinf(graph)] = np.inf
    for i in range(num_nodes):
        graph = np.minimum(graph, graph[np.newaxis, i, :] + graph[:, i, np.newaxis])
    return graph


class DiGraph:
    def __init__(self, adjacency_matrix=None, edges=None, nodes=None, is_fresh=True, use_negative_log=False):
        """
        Instantiate a weighted directional graph.

        Args:
            adjacency_matrix: Adjacency matrix to initialize the graph from. When given, the
            edges: List of edges to initialize te graph from. If not given, an adjacency matrix and a list of nodes must
                be provided.
            nodes: List of nodes in the graph. Used in conjunction with a given adjacency matrix to generate a list of
                edges.
            is_fresh:
            use_negative_log:
        """
        assert (adjacency_matrix is None) != (edges is None)  # Check XOR: one or the other should be given
        assert (adjacency_matrix is None) == (nodes is None)
        self.use_negative_log = use_negative_log
        self.is_fresh = is_fresh
        self._nodes = nodes
        self._edges = edges
        self._adjacency_matrix = adjacency_matrix
        if edges is not None:
            self.create_adjacency_matrix()
        else:
            self.create_edges()
        if self.is_fresh:
            self.add_inverse()

    def create_adjacency_matrix(self):
        # region construct name and index maps
        edges = sorted(self._edges, key=lambda edge: edge[0] + edge[1])
        if self.use_negative_log:
            edges = list(map(lambda edge: (edge[0], edge[1], -np.log(edge[2])), edges))
        seen_nodes = set()
        nodes = []
        for origin, destination, weight in edges:
            if origin not in seen_nodes:
                seen_nodes.add(origin)
                nodes.append(origin)
            if destination not in seen_nodes:
                seen_nodes.add(destination)
                nodes.append(destination)
        argsort = sorted(range(len(nodes)), key=nodes.__getitem__)
        nodes = [nodes[i] for i in argsort]
        indices = {nodes[i]: i for i in argsort}
        # endregion
        adjacency_matrix = np.full((len(nodes), len(nodes)), np.inf)
        for origin, destination, weight in edges:
            index = (indices[origin], indices[destination])
            adjacency_matrix[index] = weight
        adjacency_matrix[np.diag_indices(len(nodes))] = 0
        self._nodes = nodes
        self._edges = edges
        self._adjacency_matrix = adjacency_matrix

    def create_edges(self):
        assert len(self._nodes) == len(self._adjacency_matrix)
        self._nodes = sorted(self._nodes)
        edge_indices = np.argwhere(~np.isinf(self._adjacency_matrix))
        edges = [(self._nodes[index[0]], self._nodes[index[1]], self._adjacency_matrix[tuple(index)]) for index in
                 edge_indices]
        self._edges = edges

    @property
    def inverse(self):
        if self.use_negative_log:
            inverse_matrix = -self._adjacency_matrix
        else:
            inverse_matrix = 1 / self._adjacency_matrix
        return DiGraph(adjacency_matrix=inverse_matrix.T, nodes=self._nodes,
                       use_negative_log=self.use_negative_log, is_fresh=False)

    @property
    def negative_log(self):
        log_adjacency_matrix = -np.log(self._adjacency_matrix)
        return DiGraph(adjacency_matrix=log_adjacency_matrix, nodes=self.nodes, use_negative_log=True, is_fresh=False)

    @property
    def exp(self):
        exp_adjacency_matrix = np.exp(-self._adjacency_matrix)
        return DiGraph(adjacency_matrix=exp_adjacency_matrix, nodes=self.nodes, use_negative_log=False, is_fresh=False)

    @property
    def nodes(self):
        return self._nodes

    @property
    def adjacency_matrix(self):
        return self._adjacency_matrix

    @property
    def adjacency_filtered(self):
        return self._adjacency_matrix[~np.isinf(self._adjacency_matrix)]

    @property
    def edges(self):
        return self._edges

    def get_edge_weight(self, source, destination, true_value=True):
        indices = (self._nodes.index(source), self._nodes.index(destination))
        weight = self._adjacency_matrix[indices]
        if self.use_negative_log and true_value:
            weight = np.exp(weight)
        return np.asscalar(weight)

    def add_inverse(self):
        inverse_matrix = self.inverse.adjacency_matrix
        indices = ~np.isinf(inverse_matrix)
        np.putmask(self._adjacency_matrix, indices, inverse_matrix)
        self.create_edges()

    def get_shortest_paths(self):
        distances = floyd_warshall(self._adjacency_matrix)
        return distances

    def plot_adjacency_matrix(self):
        matrix = np.copy(self.adjacency_matrix)
        print("MIN:", matrix.min())
        print("MAX:", matrix[~np.isinf(matrix)].max())
        # matrix[np.isinf(matrix)] = 0
        mean = np.mean(matrix[~np.isinf(matrix)])
        matrix -= mean
        maximum = np.max(matrix[~np.isinf(matrix)])
        matrix /= maximum
        matrix *= 255
        matrix = matrix.astype(np.uint8)
        matrix = cv2.applyColorMap(matrix, cv2.COLORMAP_JET)
        matrix = cv2.resize(matrix, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('image', matrix)
        cv2.waitKey(0)

    def plot_shortest_paths(self):
        matrix = self.get_shortest_paths()
        matrix[np.isinf(matrix)] = 0
        # matrix = matrix / np.linalg.norm(matrix)
        mean = np.mean(matrix[~np.isinf(matrix)])
        matrix -= mean
        maximum = np.max(matrix[~np.isinf(matrix)])
        matrix /= maximum
        matrix *= 255
        matrix = matrix.astype(np.uint8)
        matrix = cv2.applyColorMap(matrix, cv2.COLORMAP_JET)
        matrix = cv2.resize(matrix, (0, 0), fx=5, fy=5, interpolation=cv2.INTER_NEAREST)
        cv2.imshow('image', matrix)
        cv2.waitKey(0)

    def __str__(self):
        return str(self.edges)
