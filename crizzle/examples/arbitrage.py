import os
import logging
import crizzle
import numpy as np

logging.basicConfig(format='%(asctime)s -- %(levelname)s: %(message)s', handlers=[logging.StreamHandler()],
                    level=logging.DEBUG)

crizzle.set_data_directory('G:/Documents/CrizzleData')
env = crizzle.get_env('binance')
LOWER_LIMIT = 21
UPPER_LIMIT = 55


def main():
    gr = env.current_price_graph()
    # gr._adjacency_matrix = gr._adjacency_matrix[LOWER_LIMIT:UPPER_LIMIT, LOWER_LIMIT:UPPER_LIMIT]
    print(gr.adjacency_matrix)
    # gr.plot_adjacency_matrix()
    print(gr.get_shortest_paths())
    # gr.plot_shortest_paths()


if __name__ == '__main__':
    main()
