from __future__ import print_function

import time
import json

import graphviz
import matplotlib.pyplot as plt
import numpy as np

import aabbtree
from plot_incremental import plot_contents, plot_tree

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def compare_depth_growth():
    plt.clf()
    np.random.seed(0)

    n_boxes = 300
    max_val = 0
    for n_dim in range(1, 11):
        for k in range(3):
            tree1 = aabbtree.AABBTree()
            tree2 = aabbtree.AABBTree()

            depths = np.zeros((n_boxes, 2))
            for box_num in range(n_boxes):
                pts = np.random.rand(n_dim, 2)
                pts.sort(axis=1)

                lens = pts[:, 1] - pts[:, 0]
                pts[:, 1] = pts[:, 0] + np.minimum(0.1, lens)

                box = aabbtree.AABB(pts)
                tree1.add(box, method='surface-area')
                tree2.add(box, method='volume')

                depths[box_num, 0] = tree1.depth
                depths[box_num, 1] = tree2.depth

            color = 'C' + str((n_dim - 1) % 10)
            if k == 0:
                plt.plot(depths[:, 0], depths[:, 1], '.', color=color,
                         label=str(n_dim) + 'D')
            else:
                plt.plot(depths[:, 0], depths[:, 1], '.', color=color)

            max_val = max(max_val, depths.max())
    plt.plot([0, max_val], [0, max_val], 'gray', lw=0.5)
    plt.axis('square')
    plt.xlim([0, max_val])
    plt.ylim([0, max_val])
    plt.grid(True)
    plt.legend(loc=2)
    plt.xlabel('Tree Depth - Surface Area Method')
    plt.ylabel('Tree Depth - Volume Method')
    plt.title('Tree Depth Comparison')
    plt.savefig('aabbtree_depth.pdf')


def compare_insert_time():
    plt.clf()
    np.random.seed(0)

    n_boxes = 300
    max_val = 0
    for n_dim in range(1, 11):
        for k in range(3):
            tree1 = aabbtree.AABBTree()
            tree2 = aabbtree.AABBTree()

            times = np.zeros((n_boxes, 2))
            for box_num in range(n_boxes):
                pts = np.random.rand(n_dim, 2)
                pts.sort(axis=1)

                lens = pts[:, 1] - pts[:, 0]
                pts[:, 1] = pts[:, 0] + np.minimum(0.1, lens)

                box = aabbtree.AABB(pts)
                start1 = time.time()
                tree1.add(box, method='surface-area')
                end1 = time.time()

                start2 = time.time()
                tree2.add(box, method='volume')
                end2 = time.time()

                times[box_num, 0] = 1000 * (end1 - start1)
                times[box_num, 1] = 1000 * (end2 - start2)

            color = 'C' + str((n_dim - 1) % 10)
            if k == 0:
                plt.plot(times[:, 0], times[:, 1], '.', color=color,
                         label=str(n_dim) + 'D')
            else:
                plt.plot(times[:, 0], times[:, 1], '.', color=color)

            max_val = max(max_val, times.max())
    plt.plot([0, max_val], [0, max_val], 'gray', lw=0.5)
    plt.axis('square')
    plt.xlim([0, max_val])
    plt.ylim([0, max_val])
    plt.grid(True)
    plt.legend(loc=2)
    plt.xlabel('Insertion Time (ms) - Surface Area Method')
    plt.ylabel('Insertion Time (ms) - Volume Method')
    plt.title('Insertion Time Comparison')
    plt.savefig('aabbtree_insertion_time.pdf')


def compare_overlap_time():
    plt.clf()
    np.random.seed(0)

    n_boxes = 300
    max_val = 0
    for n_dim in range(1, 11):
        for k in range(3):
            tree1 = aabbtree.AABBTree()
            tree2 = aabbtree.AABBTree()

            for box_num in range(n_boxes):
                pts = np.random.rand(n_dim, 2)
                pts.sort(axis=1)

                lens = pts[:, 1] - pts[:, 0]
                pts[:, 1] = pts[:, 0] + np.minimum(0.1, lens)

                box = aabbtree.AABB(pts)
                tree1.add(box, method='surface-area')
                tree2.add(box, method='volume')

            times = np.zeros((n_boxes, 2))
            for box_num in range(n_boxes):
                pts = np.random.rand(n_dim, 2)
                pts.sort(axis=1)

                lens = pts[:, 1] - pts[:, 0]
                pts[:, 1] = pts[:, 0] + np.minimum(0.1, lens)

                test_box = aabbtree.AABB(pts)

                start1 = time.time()
                tree1.overlap_values(test_box)
                end1 = time.time()

                start2 = time.time()
                tree2.overlap_values(test_box)
                end2 = time.time()

                times[box_num, 0] = 1000 * (end1 - start1)
                times[box_num, 1] = 1000 * (end2 - start2)

            color = 'C' + str((n_dim - 1) % 10)
            if k == 0:
                plt.plot(times[:, 0], times[:, 1], '.', color=color,
                         label=str(n_dim) + 'D')
            else:
                plt.plot(times[:, 0], times[:, 1], '.', color=color)

            max_val = max(max_val, times.max())

    plt.plot([0, max_val], [0, max_val], 'gray', lw=0.5)
    plt.axis('square')
    plt.xlim([0, max_val])
    plt.ylim([0, max_val])
    plt.grid(True)
    plt.legend(loc=2)
    plt.xlabel('Traversal Time (ms) - Surface Area Method')
    plt.ylabel('Traversal Time (ms) - Volume Method')
    plt.title('Traversal Time Comparison')
    plt.savefig('aabbtree_traversal_time.pdf')


def bounding_volume(tree):
    if tree.is_leaf:
        return 0
    else:
        vol = tree.aabb.volume
        vol_l = bounding_volume(tree.left)
        vol_r = bounding_volume(tree.right)
        return vol + vol_l + vol_r


def sib_overlap(tree):
    if tree.is_leaf:
        return 0
    else:
        p_olap = tree.left.aabb.overlap_volume(tree.right.aabb)
        l_olap = sib_overlap(tree.left)
        r_olap = sib_overlap(tree.right)
        return p_olap + l_olap + r_olap


def compare_bounding_volume():
    plt.clf()
    np.random.seed(0)

    n_boxes = 300
    max_val = 0
    for n_dim in range(1, 11):
        for k in range(3):
            tree1 = aabbtree.AABBTree()
            tree2 = aabbtree.AABBTree()

            vols = np.zeros((n_boxes, 2))
            for box_num in range(n_boxes):
                pts = np.random.rand(n_dim, 2)
                pts.sort(axis=1)

                lens = pts[:, 1] - pts[:, 0]
                pts[:, 1] = pts[:, 0] + np.minimum(0.1, lens)

                box = aabbtree.AABB(pts)
                tree1.add(box, method='surface-area')
                tree2.add(box, method='volume')

                vols[box_num, 0] = bounding_volume(tree1)
                vols[box_num, 1] = bounding_volume(tree2)

            color = 'C' + str((n_dim - 1) % 10)
            if k == 0:
                plt.plot(vols[:, 0], vols[:, 1], '.', color=color,
                         label=str(n_dim) + 'D')
            else:
                plt.plot(vols[:, 0], vols[:, 1], '.', color=color)

            max_val = max(max_val, vols.max())
    plt.plot([0, max_val], [0, max_val], 'gray', lw=0.5)
    plt.axis('square')
    plt.xlim([0, max_val])
    plt.ylim([0, max_val])
    plt.grid(True)
    plt.legend(loc=2)
    plt.xlabel('Total Bounding Volume - Surface Area Method')
    plt.ylabel('Total Bounding Volume - Volume Method')
    plt.title('Bounding Volume Comparison Comparison')
    plt.show()


def plot_state(state, state_color):
    xmin = float('inf')
    xmax = - float('inf')
    ymin = float('inf')
    ymax = - float('inf')

    poly_type = state['type']
    coords = state['coordinates']
    if poly_type == 'Polygon':
        for edge in coords:
            x, y = zip(*edge)
            plt.plot(x, y, state_color)

            xmin = min(min(x), xmin)
            ymin = min(min(y), ymin)

            xmax = max(max(x), xmax)
            ymax = max(max(y), ymax)
    else:
        for mass in coords:
            for edge in mass:
                x, y = zip(*edge)
                plt.plot(x, y, state_color)

                xmin = min(min(x), xmin)
                ymin = min(min(y), ymin)

                xmax = max(max(x), xmax)
                ymax = max(max(y), ymax)

    return [(xmin, xmax), (ymin, ymax)]


def plot_tree_gv(tree, filename):
    graph_edges, graph_values = tree2graph(tree)
    for edge in graph_edges:
        print(edge)
    print(graph_values)

    dot = graphviz.Digraph()
    for i, val in enumerate(graph_values):
        if val is None:
            dot.node(str(i), '')
        else:
            dot.node(str(i), val)

    for kp1, kp2 in graph_edges:
        dot.edge(str(kp1), str(kp2))

    dot.render(filename, view=True)


def tree2graph(tree, n=0):
    node_edges = []
    node_values = [tree.value]

    if tree.is_leaf:
        return node_edges, node_values

    n_left = n + len(node_values)
    node_edges.append((n, n_left))
    left_edges, left_values = tree2graph(tree.left, n_left)
    node_edges.extend(left_edges)
    node_values.extend(left_values)

    n_right = n + len(node_values)
    node_edges.append((n, n_right))
    right_edges, right_values = tree2graph(tree.right, n_right)
    node_edges.extend(right_edges)
    node_values.extend(right_values)

    return node_edges, node_values


def compare_us_states():
    # Plot Settings
    state_color = 'gray'

    # Read in State Data
    with open('us_states.json', 'r') as f:
        data = json.load(f)

    features = data['features']
    pts = {feat['properties']['NAME']: feat['geometry'] for feat in features}

    # Build Trees
    tree1 = aabbtree.AABBTree()
    tree2 = aabbtree.AABBTree()

    exclude = ['Alaska', 'Hawaii', 'Puerto Rico']
    for state in pts:
        if state in exclude:
            continue

        limits = plot_state(pts[state], state_color)
        box = aabbtree.AABB(limits)

        abbrev = us_state_abbrev[state]
        tree1.add(box, abbrev, method='surface-area')
        tree2.add(box, abbrev, method='volume')

    # Plot the Surface Area Method
    bv1 = bounding_volume(tree1)
    bv2 = bounding_volume(tree2)
    so1 = sib_overlap(tree1)
    so2 = sib_overlap(tree2)

    print(bv1, bv2)
    print(so1, so2)

    plot_tree_gv(tree1, 'surface_area.gv')
    plot_tree_gv(tree2, 'volume.gv')



if __name__ == '__main__':
    '''
    compare_depth_growth()
    compare_insert_time()
    compare_overlap_time()
    '''
    # compare_bounding_volume()
    compare_us_states()
