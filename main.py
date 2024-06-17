import dearpygui.dearpygui as dpg
# import numpy as np
# import random as rd
from math import sin, cos, pi
# from dearpygui import demo

dpg.create_context()
dpg.create_viewport(title='Custom Title', decorated=True)

DIRECTED = True
COUNT_OF_GRAPHS = 0


# DATA_FOR_FF_VALUE = []


def to_normal_coordinates(any_x: int, any_y: int):
    return any_x + 300, -any_y + 300


def to_not_normal_coordinates(any_x: int, any_y: int):
    return any_x - 300, -any_y + 300


def my_ff_value(adj_matrix, source, stock):
    max_flow = 0


def ford_fulkerson(graph, source, stock):
    parent = [-1 for _ in range(len(graph))]
    max_flow = 0

    def bfs(graph, source, stock, parent):
        visited = [False for _ in range(len(graph))]
        queue = [source]
        visited[source] = True

        while queue:
            u = queue.pop(0)
            for ind, val in enumerate(graph[u]):
                if not visited[ind] and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        print(parent)
        return visited[stock]

    while bfs(graph, source, stock, parent):
        path_flow = float('Inf')
        s = stock
        while s != source:
            print(path_flow, graph[parent[s]][s], parent[s])
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]

        max_flow += path_flow
        v = stock
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]

    return max_flow


def create_graph():
    global COUNT_OF_GRAPHS
    count_of_source_plus_stock = 0
    is_source, is_stock = float("Inf"), float("Inf")
    COUNT_OF_GRAPHS += 1
    nods = list()
    xn, yn = -250, 0
    color = (127, 127, 127)
    work_array0 = list()
    work_array1 = list()
    for i in range(n := dpg.get_value("dimension")):
        for j in range(n):
            if (value := dpg.get_value(f"{i} {j}")) < 0:
                raise ValueError("Value < 0")
            work_array1.append(value)
        work_array0.append(work_array1)
        work_array1 = list()
    del work_array1
    adj_matrix = work_array0
    with (dpg.window(label=f"Graph {COUNT_OF_GRAPHS}", tag=f"graph{COUNT_OF_GRAPHS}", autosize=True, no_collapse=True)):
        dpg.add_text(default_value=f"Calculate the maximum flow:\n~0", tag=f"ff_value{COUNT_OF_GRAPHS}")
        with dpg.drawlist(width=600, height=600, tag=f"draw{COUNT_OF_GRAPHS}"):
            # center = (300, 300)
            # radius = 250
            # dpg.draw_circle(center, radius)
            for i in range(n):
                alpha = (2 * pi) / n
                xn, yn = yn * sin(alpha) + xn * cos(alpha), yn * cos(alpha) - xn * sin(alpha)
                dpg.draw_circle(to_normal_coordinates(xn, yn), 20, fill=color, tag=f"nod{i}-{COUNT_OF_GRAPHS}",
                                thickness=3.0)
                x0, y0 = to_normal_coordinates(xn, yn)
                key1, key2 = True, True
                text_color = (0, 255, 0)
                for k in range(n):
                    key1 = key1 and (adj_matrix[i][k] == 0)
                    key2 = key2 and (adj_matrix[k][i] == 0)
                if key1 or key2:
                    if key1:
                        is_stock = i
                        count_of_source_plus_stock += 1
                    if key2:
                        is_source = i
                        count_of_source_plus_stock += 1
                    text_color = (200, 0, 200)
                dpg.draw_text((x0 + 10, y0 + 10), f"V{i}", size=30, color=text_color)
                nods.append((to_normal_coordinates(xn, yn), f"nod{i}-{COUNT_OF_GRAPHS}"))
            for i in range(n):
                for j in range(n):
                    if i == j:
                        pass
                    else:
                        if adj_matrix[i][j] != 0:
                            # x1, y1 = to_not_normal_coordinates(*nods[i][0])
                            # x2, y2 = to_not_normal_coordinates(*nods[j][0])
                            dpg.draw_arrow(nods[j][0], nods[i][0], thickness=2.0, size=6)
                            dpg.draw_text(((nods[j][0][0] + nods[i][0][0]) / 2, (nods[j][0][1] + nods[i][0][1]) / 2),
                                          text=f"{adj_matrix[i][j]}", size=25)
        if count_of_source_plus_stock == 2 and is_source != is_stock:
            dpg.set_value(f"ff_value{COUNT_OF_GRAPHS}", f"Calculate the maximum flow:\n{ford_fulkerson(adj_matrix,
                                                                                                       is_source, is_stock)}")


def oriented():
    global DIRECTED
    if DIRECTED:
        DIRECTED = False
        ...
    else:
        DIRECTED = True
        ...


def output_matrix():
    global DIRECTED
    if not DIRECTED:
        dpg.delete_item("adj_matrix")
        with dpg.table(parent=settings, header_row=False, tag="adj_matrix"):
            for i in range(n := dpg.get_value("dimension")):
                dpg.add_table_column()
                with dpg.table_row():
                    for j in range(n):
                        dpg.add_drag_int(width=30, tag=f"{i} {j}")
    else:
        dpg.delete_item("adj_matrix")
        with dpg.table(parent=settings, header_row=False, tag="adj_matrix"):
            for i in range(n := dpg.get_value("dimension")):
                dpg.add_table_column()
                with dpg.table_row():
                    for j in range(n):
                        dpg.add_drag_int(width=30, tag=f"{i} {j}")


with dpg.window(no_collapse=True, no_resize=True, no_close=True,
                no_title_bar=True, tag='main_menu') as main_menu_window:
    with dpg.window(label='Settings', autosize=True, no_collapse=True,
                    no_resize=True, no_close=True, no_move=True, tag='Settings') as settings:
        dpg.add_checkbox(label="Oriented", callback=oriented, default_value=True)
        dpg.add_input_int(min_value=1, min_clamped=True, default_value=1, width=100,
                          callback=output_matrix, tag="dimension")
        dpg.add_button(label="Create", callback=create_graph)
        with dpg.table(header_row=False, tag="adj_matrix") as adj_matrix:
            for i in range(n := dpg.get_value("dimension")):
                dpg.add_table_column()
                with dpg.table_row():
                    for j in range(n):
                        dpg.add_drag_int(width=30, tag=f"{i} {j}")

# demo.show_demo()

dpg.set_primary_window(window=main_menu_window, value=True)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
