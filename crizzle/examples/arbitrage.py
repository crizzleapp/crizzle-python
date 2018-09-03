import os
import logging
import numpy as np
import crizzle

logging.basicConfig(format='%(asctime)s -- %(levelname)s: %(message)s', handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

crizzle.set_data_directory('G:/Documents/CrizzleData')
env = crizzle.get_env('binance')

gr = env.current_price_graph()
print(gr.adjacency_matrix[~np.isnan(gr.adjacency_matrix)])
# print(gr.get_edge_weight('TRX', 'ETH'))
# print(gr.get_edge_weight('ETH', 'TRX'))

# for asset_1 in gr.nodes[:2]:
#     for asset_2 in gr.nodes[:2]:
#         if asset_1 != asset_2:
#             print("{} -> {}:".format(asset_1, asset_2))
#             dist = gr.get_distance(asset_1, asset_2)
#             print(dist)
