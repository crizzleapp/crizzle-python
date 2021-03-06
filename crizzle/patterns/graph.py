def initialize(graph, source):
    d = {}  # Stands for destination
    p = {}  # Stands for predecessor
    for node in graph:
        d[node] = float('Inf')  # We start assuming that the rest of nodes are unreachable
        p[node] = None
    d[source] = 0  # For the source we know how to reach
    return d, p


def relax(node, neighbour, graph, d, p):
    # If the distance between the node and the neighbour is lower than the one we have now
    if d[neighbour] > d[node] + graph[node][neighbour]:
        # Record this lower distance
        d[neighbour] = d[node] + graph[node][neighbour]
        p[neighbour] = node


def bellman_ford_iteration(graph, d, p):
    for u in graph:
        for v in graph[u]:  # For each neighbour of u
            relax(u, v, graph, d, p)  # relax the edge between u and v


def bellman_ford(graph, source):
    d, p = initialize(graph, source)
    for i in range(len(graph) - 1):  # Run iterations until convergence
        bellman_ford_iteration(graph, d, p)

    # Check for negative-weight cycles
    for u in graph:
        for v in graph[u]:
            try:
                assert d[v] <= d[u] + graph[u][v]
            except AssertionError:
                print("Detected a negative weight cycle:", u, v)
    return d, p


class DiGraph:
    def __init__(self, adjacency=None, edges=None, name=None):
        self._adjacency = {}
        self.name = None
        if isinstance(adjacency, dict):
            assert edges is None
            self.repair_adjacency(adjacency)
            self._adjacency = adjacency
        elif isinstance(edges, list):
            assert adjacency is None
            adjacency = self.edges_to_adjacency(edges)
            self.repair_adjacency(adjacency)
            self._adjacency = adjacency
        if name is not None:
            self.name = name

    @staticmethod
    def repair_adjacency(adjacency):
        missing_origins = []
        for adj in adjacency.values():
            for dest in adj:
                if dest not in adjacency:
                    missing_origins.append(dest)
                    # raise ValueError("Adjacency list is malformed.")
        for origin in missing_origins:
            adjacency.update({origin: {}})

    @staticmethod
    def edges_to_adjacency(edges):
        adjacency = {}
        for edge in edges:
            source, destination, weight = edge
            if source not in adjacency:
                adjacency[source] = {}
            if destination not in adjacency[source]:
                adjacency[source][destination] = weight
        return adjacency

    @property
    def inverse(self):
        inverse_edges = []
        for origin in self._adjacency:
            for destination in self._adjacency[origin]:
                inverse = [destination, origin, 1.0 / self._adjacency[origin][destination]]
                inverse_edges.append(inverse)
        return DiGraph(edges=inverse_edges)

    @property
    def nodes(self):
        return list(self._adjacency.keys())

    @property
    def adjacency(self):
        return self._adjacency

    @property
    def edges(self):
        edges = []
        for node, neighbors in self._adjacency.items():
            for nb in neighbors:
                edges.append((node, nb, neighbors[nb]))
        return edges

    def add_node(self, name):
        if name not in self._adjacency:
            self._adjacency[name] = {}

    def add_nodes(self, *names):
        for name in names:
            self.add_node(name)

    def add_edge(self, origin, destination, weight):
        self.add_nodes(origin, destination)
        if destination not in self._adjacency[origin]:
            self._adjacency[origin][destination] = weight

    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(*edge)

    def edge_weight(self, origin, destination):
        return self._adjacency[origin][destination]

    def shortest_path(self, source, destination):
        try:
            path = [destination]
            d, p = bellman_ford(self._adjacency, source)
            predecessor = p[destination]
            while predecessor != source:
                path.append(predecessor)
                predecessor = p[predecessor]
            return list(reversed(path))
        except AssertionError as e:
            print(e)

    def add_inverse(self):
        inverse = self.inverse
        self.add_edges(inverse.edges)

    def __str__(self):
        return str(self._adjacency)


if __name__ == '__main__':
    def test():
        g = DiGraph({
            1: {3: 1},
            2: {5: 1},
            3: {2: 1},
            4: {6: 1},
            5: {4: 1},
            6: {},
        })

        l = DiGraph(
            edges=[['ETH', 'BTC', 0.07825], ['LTC', 'BTC', 0.01648], ['BNB', 'BTC', 0.001557], ['NEO', 'BTC', 0.009144],
                   ['QTUM', 'ETH', 0.030492], ['EOS', 'ETH', 0.024566], ['SNT', 'ETH', 0.00022463],
                   ['BNT', 'ETH', 0.006775], ['BCC', 'BTC', 0.159161], ['GAS', 'BTC', 0.003328],
                   ['BNB', 'ETH', 0.019955], ['BTC', 'USDT', 9227.93], ['ETH', 'USDT', 721.8], ['HSR', 'BTC', 0.001625],
                   ['OAX', 'ETH', 0.001267], ['DNT', 'ETH', 0.00015217], ['MCO', 'ETH', 0.01633],
                   ['ICN', 'ETH', 0.0022095], ['MCO', 'BTC', 0.001273], ['WTC', 'BTC', 0.0017839],
                   ['WTC', 'ETH', 0.022596], ['LRC', 'BTC', 0.00010308], ['LRC', 'ETH', 0.00131682],
                   ['QTUM', 'BTC', 0.002385], ['YOYO', 'BTC', 2.077e-05], ['OMG', 'BTC', 0.002002],
                   ['OMG', 'ETH', 0.025562], ['ZRX', 'BTC', 0.00015625], ['ZRX', 'ETH', 0.0019903],
                   ['STRAT', 'BTC', 0.0008153], ['STRAT', 'ETH', 0.010462], ['SNGLS', 'BTC', 1.345e-05],
                   ['SNGLS', 'ETH', 0.000172], ['BQX', 'BTC', 0.00038511], ['BQX', 'ETH', 0.004925],
                   ['KNC', 'BTC', 0.00028073], ['KNC', 'ETH', 0.0036015], ['FUN', 'BTC', 5.81e-06],
                   ['FUN', 'ETH', 7.419e-05], ['SNM', 'BTC', 3.196e-05], ['SNM', 'ETH', 0.00041026],
                   ['NEO', 'ETH', 0.117234], ['IOTA', 'BTC', 0.00024135], ['IOTA', 'ETH', 0.003082],
                   ['LINK', 'BTC', 6.134e-05], ['LINK', 'ETH', 0.00078451], ['XVG', 'BTC', 8.4e-06],
                   ['XVG', 'ETH', 0.00010781], ['SALT', 'BTC', 0.0004662], ['SALT', 'ETH', 0.005993],
                   ['MDA', 'BTC', 0.00013226], ['MDA', 'ETH', 0.0016931], ['MTL', 'BTC', 0.0005846],
                   ['MTL', 'ETH', 0.007475], ['SUB', 'BTC', 8.853e-05], ['SUB', 'ETH', 0.00113],
                   ['EOS', 'BTC', 0.0019206], ['SNT', 'BTC', 1.755e-05], ['ETC', 'ETH', 0.030127],
                   ['ETC', 'BTC', 0.00236], ['MTH', 'BTC', 1.534e-05], ['MTH', 'ETH', 0.0001969],
                   ['ENG', 'BTC', 0.00032181], ['ENG', 'ETH', 0.004115], ['DNT', 'BTC', 1.189e-05],
                   ['ZEC', 'BTC', 0.032013], ['ZEC', 'ETH', 0.40854], ['BNT', 'BTC', 0.000529],
                   ['AST', 'BTC', 6.256e-05], ['AST', 'ETH', 0.0008033], ['DASH', 'BTC', 0.052548],
                   ['DASH', 'ETH', 0.67451], ['OAX', 'BTC', 9.911e-05], ['ICN', 'BTC', 0.00017335],
                   ['BTG', 'BTC', 0.008073], ['BTG', 'ETH', 0.103765], ['EVX', 'BTC', 0.00019571],
                   ['EVX', 'ETH', 0.0025065], ['REQ', 'BTC', 3.181e-05], ['REQ', 'ETH', 0.000405],
                   ['VIB', 'BTC', 2.439e-05], ['VIB', 'ETH', 0.00031168], ['HSR', 'ETH', 0.020849],
                   ['TRX', 'BTC', 9.27e-06], ['TRX', 'ETH', 0.00011849], ['POWR', 'BTC', 6.158e-05],
                   ['POWR', 'ETH', 0.00079], ['ARK', 'BTC', 0.0003993], ['ARK', 'ETH', 0.005135],
                   ['YOYO', 'ETH', 0.00026401], ['XRP', 'BTC', 9.218e-05], ['XRP', 'ETH', 0.00117996],
                   ['MOD', 'BTC', 0.0003299], ['MOD', 'ETH', 0.004231], ['ENJ', 'BTC', 1.78e-05],
                   ['ENJ', 'ETH', 0.0002275], ['STORJ', 'BTC', 0.00012877], ['STORJ', 'ETH', 0.00164],
                   ['BNB', 'USDT', 14.3645], ['VEN', 'BNB', 0.3553], ['YOYO', 'BNB', 0.01324], ['POWR', 'BNB', 0.03941],
                   ['VEN', 'BTC', 0.00055333], ['VEN', 'ETH', 0.00706967], ['KMD', 'BTC', 0.0004275],
                   ['KMD', 'ETH', 0.005503], ['NULS', 'BNB', 0.27999], ['RCN', 'BTC', 1.653e-05],
                   ['RCN', 'ETH', 0.00021188], ['RCN', 'BNB', 0.01062], ['NULS', 'BTC', 0.00043749],
                   ['NULS', 'ETH', 0.00558107], ['RDN', 'BTC', 0.00025423], ['RDN', 'ETH', 0.0032574],
                   ['RDN', 'BNB', 0.1634], ['XMR', 'BTC', 0.026552], ['XMR', 'ETH', 0.34051], ['DLT', 'BNB', 0.0227],
                   ['WTC', 'BNB', 1.1448], ['DLT', 'BTC', 3.52e-05], ['DLT', 'ETH', 0.00044999],
                   ['AMB', 'BTC', 8.455e-05], ['AMB', 'ETH', 0.00107929], ['AMB', 'BNB', 0.05424],
                   ['BCC', 'ETH', 2.03324], ['BCC', 'USDT', 1468.0], ['BCC', 'BNB', 102.32], ['BAT', 'BTC', 5.425e-05],
                   ['BAT', 'ETH', 0.00069514], ['BAT', 'BNB', 0.03483], ['BCPT', 'BTC', 6.879e-05],
                   ['BCPT', 'ETH', 0.00088194], ['BCPT', 'BNB', 0.04415], ['ARN', 'BTC', 0.00022733],
                   ['ARN', 'ETH', 0.00290011], ['GVT', 'BTC', 0.0027851], ['GVT', 'ETH', 0.03552],
                   ['CDT', 'BTC', 8.3e-06], ['CDT', 'ETH', 0.00010615], ['GXS', 'BTC', 0.0004795],
                   ['GXS', 'ETH', 0.006139], ['NEO', 'USDT', 84.4], ['NEO', 'BNB', 5.87], ['POE', 'BTC', 6.63e-06],
                   ['POE', 'ETH', 8.473e-05], ['QSP', 'BTC', 2.315e-05], ['QSP', 'ETH', 0.0002961],
                   ['QSP', 'BNB', 0.01488], ['BTS', 'BTC', 3.989e-05], ['BTS', 'ETH', 0.00051092],
                   ['BTS', 'BNB', 0.02574], ['XZC', 'BTC', 0.004866], ['XZC', 'ETH', 0.062305], ['XZC', 'BNB', 3.108],
                   ['LSK', 'BTC', 0.0015109], ['LSK', 'ETH', 0.0193], ['LSK', 'BNB', 0.9676], ['TNT', 'BTC', 1.528e-05],
                   ['TNT', 'ETH', 0.00019507], ['FUEL', 'BTC', 1.21e-05], ['FUEL', 'ETH', 0.00015466],
                   ['MANA', 'BTC', 1.904e-05], ['MANA', 'ETH', 0.00024387], ['BCD', 'BTC', 0.003518],
                   ['BCD', 'ETH', 0.04493], ['DGD', 'BTC', 0.029553], ['DGD', 'ETH', 0.37898], ['IOTA', 'BNB', 0.15467],
                   ['ADX', 'BTC', 0.00011448], ['ADX', 'ETH', 0.0014649], ['ADX', 'BNB', 0.07385],
                   ['ADA', 'BTC', 4.058e-05], ['ADA', 'ETH', 0.00051895], ['PPT', 'BTC', 0.0025933],
                   ['PPT', 'ETH', 0.033227], ['CMT', 'BTC', 3.041e-05], ['CMT', 'ETH', 0.00039004],
                   ['CMT', 'BNB', 0.01945], ['XLM', 'BTC', 4.689e-05], ['XLM', 'ETH', 0.00060124],
                   ['XLM', 'BNB', 0.03018], ['CND', 'BTC', 1.276e-05], ['CND', 'ETH', 0.00016356],
                   ['CND', 'BNB', 0.00823], ['LEND', 'BTC', 9.96e-06], ['LEND', 'ETH', 0.00012767],
                   ['WABI', 'BTC', 0.00015676], ['WABI', 'ETH', 0.00201298], ['WABI', 'BNB', 0.10078],
                   ['LTC', 'ETH', 0.20993], ['LTC', 'USDT', 151.66], ['LTC', 'BNB', 10.54], ['TNB', 'BTC', 7.32e-06],
                   ['TNB', 'ETH', 9.37e-05], ['WAVES', 'BTC', 0.0008034], ['WAVES', 'ETH', 0.010255],
                   ['WAVES', 'BNB', 0.5129], ['GTO', 'BTC', 5.922e-05], ['GTO', 'ETH', 0.00075833],
                   ['GTO', 'BNB', 0.03808], ['ICX', 'BTC', 0.0004773], ['ICX', 'ETH', 0.006107],
                   ['ICX', 'BNB', 0.30653], ['OST', 'BTC', 3.046e-05], ['OST', 'ETH', 0.000389],
                   ['OST', 'BNB', 0.01943], ['ELF', 'BTC', 0.00020577], ['ELF', 'ETH', 0.00262642],
                   ['AION', 'BTC', 0.00043], ['AION', 'ETH', 0.005495], ['AION', 'BNB', 0.27641],
                   ['NEBL', 'BTC', 0.001726], ['NEBL', 'ETH', 0.022144], ['NEBL', 'BNB', 1.10824],
                   ['BRD', 'BTC', 9.041e-05], ['BRD', 'ETH', 0.0011509], ['BRD', 'BNB', 0.05784],
                   ['MCO', 'BNB', 0.81551], ['EDO', 'BTC', 0.0003027], ['EDO', 'ETH', 0.003893],
                   ['WINGS', 'BTC', 7.162e-05], ['WINGS', 'ETH', 0.000915], ['NAV', 'BTC', 0.0001586],
                   ['NAV', 'ETH', 0.002029], ['NAV', 'BNB', 0.10198], ['LUN', 'BTC', 0.0015931],
                   ['LUN', 'ETH', 0.020428], ['TRIG', 'BTC', 0.0001801], ['TRIG', 'ETH', 0.00231],
                   ['TRIG', 'BNB', 0.11587], ['APPC', 'BTC', 7.62e-05], ['APPC', 'ETH', 0.0009774],
                   ['APPC', 'BNB', 0.04895], ['VIBE', 'BTC', 3.475e-05], ['VIBE', 'ETH', 0.000445],
                   ['RLC', 'BTC', 0.0001822], ['RLC', 'ETH', 0.002339], ['RLC', 'BNB', 0.11703],
                   ['INS', 'BTC', 0.0002189], ['INS', 'ETH', 0.002797], ['PIVX', 'BTC', 0.0006441],
                   ['PIVX', 'ETH', 0.008244], ['PIVX', 'BNB', 0.41349], ['IOST', 'BTC', 6.78e-06],
                   ['IOST', 'ETH', 8.695e-05], ['CHAT', 'BTC', 1.48e-05], ['CHAT', 'ETH', 0.00018902],
                   ['STEEM', 'BTC', 0.0004253], ['STEEM', 'ETH', 0.005444], ['STEEM', 'BNB', 0.27295],
                   ['NANO', 'BTC', 0.0009072], ['NANO', 'ETH', 0.011588], ['NANO', 'BNB', 0.5807],
                   ['VIA', 'BTC', 0.0002869], ['VIA', 'ETH', 0.003662], ['VIA', 'BNB', 0.18426],
                   ['BLZ', 'BTC', 7.52e-05], ['BLZ', 'ETH', 0.0009623], ['BLZ', 'BNB', 0.04836],
                   ['AE', 'BTC', 0.0005008], ['AE', 'ETH', 0.006419], ['AE', 'BNB', 0.32211], ['RPX', 'BTC', 1.551e-05],
                   ['RPX', 'ETH', 0.00019811], ['RPX', 'BNB', 0.00995], ['NCASH', 'BTC', 5.19e-06],
                   ['NCASH', 'ETH', 6.627e-05], ['NCASH', 'BNB', 0.00334], ['POA', 'BTC', 8.031e-05],
                   ['POA', 'ETH', 0.00102901], ['POA', 'BNB', 0.05143], ['ZIL', 'BTC', 1.313e-05],
                   ['ZIL', 'ETH', 0.00016783], ['ZIL', 'BNB', 0.00844], ['ONT', 'BTC', 0.0010533],
                   ['ONT', 'ETH', 0.013506], ['ONT', 'BNB', 0.67729], ['STORM', 'BTC', 6.99e-06],
                   ['STORM', 'ETH', 8.936e-05], ['STORM', 'BNB', 0.00448], ['QTUM', 'BNB', 1.53046],
                   ['QTUM', 'USDT', 21.979], ['XEM', 'BTC', 4.52e-05], ['XEM', 'ETH', 0.000579],
                   ['XEM', 'BNB', 0.02912], ['WAN', 'BTC', 0.0009977], ['WAN', 'ETH', 0.012772],
                   ['WAN', 'BNB', 0.64124], ['WPR', 'BTC', 1.7e-05], ['WPR', 'ETH', 0.00021762],
                   ['QLC', 'BTC', 2.495e-05], ['QLC', 'ETH', 0.00031953], ['SYS', 'BTC', 6.049e-05],
                   ['SYS', 'ETH', 0.00077095], ['SYS', 'BNB', 0.03889], ['QLC', 'BNB', 0.016],
                   ['GRS', 'BTC', 0.00015789], ['GRS', 'ETH', 0.00202985], ['ADA', 'USDT', 0.37455],
                   ['ADA', 'BNB', 0.02604], ['CLOAK', 'BTC', 0.0016176], ['CLOAK', 'ETH', 0.020852],
                   ['GNT', 'BTC', 9.48e-05], ['GNT', 'ETH', 0.00121369], ['GNT', 'BNB', 0.06136],
                   ['LOOM', 'BTC', 5.451e-05], ['LOOM', 'ETH', 0.00069659], ['LOOM', 'BNB', 0.03492]])

        l.add_inverse()
        print(l)
        print(l.shortest_path('CHAT', 'SYS'))

    test()
