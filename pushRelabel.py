class Edge:
    def get_flow(self):
        return self.flow

    def set_flow(self, flow):
        self.flow = flow

    def get_capacity(self):
        return self.capacity

    def set_capacity(self, capacity):
        self.capacity = capacity

    def get_start_vertex(self):
        return self.start_vertex

    def set_start_vertex(self, vertex):
        self.end_vertex = vertex

    def get_end_vertex(self):
        return self.end_vertex

    def set_end_vertex(self, vertex):
        self.end_vertex = vertex

    def __init__(self, flow, capacity, u, v):
        self.flow = flow
        self.capacity = capacity
        self.start_vertex = u
        self.end_vertex = v


class Vertex:
    def get_height(self):
        return self.height

    def set_height(self, h):
        self.height = h

    def get_excess_flow(self):
        return self.excess_flow

    def set_excess_flow(self, flow):
        self.excess_flow = flow

    def __init__(self, height, excess_flow):
        self.height = height
        self.excess_flow = excess_flow


class Graph:
    def __init__(self, n):
        self.vertices_count = n
        self.vertices = []
        self.edges = []

        # Initialize the vertices with 0 height and 0 excess flow
        for i in range(0, n):
            self.vertices.append(Vertex(0, 0))

    def add_edge(self, start, end, capacity):
        self.edges.append(Edge(0, capacity, start, end))

    def pre_flow(self, source_vertex_index):
        # Set the height of source vertex to number of vertices
        self.vertices[source_vertex_index].set_height(len(self.vertices))

        # Initialize the values for all edges starting from the source
        for i in range(0, len(self.edges)):
            if self.edges[i].get_start_vertex() == source_vertex_index:
                # Set the flow of the source vertex to capacity of this edge
                self.edges[i].set_flow(self.edges[i].get_capacity())

                # Initializing the excess flow for edges emanating from the source
                self.vertices[self.edges[i].get_end_vertex()].set_excess_flow(self.vertices[self.edges[i].get_end_vertex()].get_excess_flow() + self.edges[i].get_flow())

                # Add an edge between the destination and the source of this edge to the residual
                # graph with capacity 0
                self.edges.append(
                    Edge(
                        -self.edges[i].get_flow(), # reversing the flow through this edge
                        0, # capacity is initialized to 0
                        self.edges[i].get_end_vertex(), # setting the source for this new edge
                        source_vertex_index # setting the destination of this new edge
                    )
                )

    def overflow_vertex(self):
        # Check if any of the vertices have their excess flow > 0 and return its index
        for i in range(1, len(self.vertices) - 1):
            if self.vertices[i].get_excess_flow() > 0:
                return i

        return -1

    def update_reverse_edge_flow(self, index, new_flow):
        # Find the end points of the reverse edge
        start_vertex_index = self.edges[index].get_end_vertex()
        end_vertex_index = self.edges[index].get_start_vertex()

        # Search for the reverse edge using the above vertices and update the flow for this
        # edge by reducing the flow of this edge by the value of 'new_flow'

        # Check if the reverse edge already exists
        for i in range(0, len(self.edges)):
            if self.edges[i].get_end_vertex() == end_vertex_index and self.edges[i].get_start_vertex() == start_vertex_index:
                self.edges[i].set_flow(self.edges[i].get_flow() - new_flow)
                return

        # Since the reverse edge doesn't exists, add it to the residual graph
        self.edges.append(Edge(0, new_flow, start_vertex_index, end_vertex_index))

    def push_flow(self, vertex_i):
        # We need to push the overflow on this vertex to an outgoing edge which has the capacity
        for i in range(0, len(self.edges)):
            if self.edges[i].get_start_vertex() == vertex_i:
                # Check if flow = capacity since in such a case we cannot push the overflow into
                # this edge
                if self.edges[i].get_flow() == self.edges[i].get_capacity():
                    continue

                # We can push the overflow into this edge if the height of its end vertex < height
                # of the source vertex
                if self.vertices[vertex_i].get_height() > self.vertices[self.edges[i].get_end_vertex()].get_height():
                    # The new flow will be equal to the minimum of remaining flow on edge and excess flow
                    new_flow = 0
                    if self.edges[i].get_capacity() - self.edges[i].get_flow() < self.vertices[vertex_i].get_excess_flow():
                        new_flow = self.edges[i].get_capacity() - self.edges[i].get_flow()
                    else:
                        new_flow = self.vertices[vertex_i].get_excess_flow()

                    # Reduce the excess flow for overflowing vertex
                    self.vertices[vertex_i].set_excess_flow(self.vertices[vertex_i].get_excess_flow() - new_flow)

                    # Increase the excess flow for the adjacent vertex
                    self.vertices[self.edges[i].get_end_vertex()].set_excess_flow(self.vertices[self.edges[i].get_end_vertex()].get_excess_flow() + new_flow)

                    # Adding residual flow
                    self.edges[i].set_flow(self.edges[i].get_flow() + new_flow)

                    self.update_reverse_edge_flow(i, new_flow)

                    return True
        return False

    def relabel(self, vertex_i):
        max_height = 9999 # Random large number to intialize the minimum height of an adjacent vertex

        # Find the adjacent vertex with minimum height
        for i in range(0, len(self.edges)):
            if self.edges[i].get_start_vertex() == vertex_i:
                # Do not relabel if the flow is equal to the capacity
                if self.edges[i].get_flow() == self.edges[i].get_capacity():
                    continue

                # Update the minimum height
                if self.vertices[self.edges[i].get_end_vertex()].get_height() < max_height:
                    max_height = self.vertices[self.edges[i].get_end_vertex()].get_height()
                    self.vertices[vertex_i].set_height(max_height + 1)

    def get_max_flow(self, source, sink):
        self.pre_flow(source)

        # Repeat the operation until none of the vertices are in overflow
        while self.overflow_vertex() != -1:
            vertex_i = self.overflow_vertex()
            if not self.push_flow(vertex_i):
                self.relabel(vertex_i)

        # Return the excess flow of the last vertex since this will be the max flow
        return self.vertices[-1].get_excess_flow()


def main():
    graph = Graph(6)

    graph.add_edge(0, 1, 16)
    graph.add_edge(0, 2, 13)
    graph.add_edge(1, 2, 10)
    graph.add_edge(2, 1, 4)
    graph.add_edge(1, 3, 12)
    graph.add_edge(2, 4, 14)
    graph.add_edge(3, 2, 9)
    graph.add_edge(3, 5, 20)
    graph.add_edge(4, 3, 7)
    graph.add_edge(4, 5, 4)

    source = 0
    sink = 5

    print "Maximum Flow: " + str(graph.get_max_flow(source, sink))


if __name__ == '__main__':
    main()