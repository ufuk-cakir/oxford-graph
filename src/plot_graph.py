import argparse
import json
from pyvis.network import Network
import networkx as nx
from utils import load_json

# Define the function to create the network graph
def create_supervisor_network(input_file, output_file):
    # Load the JSON data
    supervisors = load_json(input_file)
    
    # Initialize a NetworkX graph
    G = nx.Graph()

    # Add nodes and edges based on keywords
    for supervisor in supervisors:
        supervisor_node = supervisor["name"]
        G.add_node(supervisor_node, type="supervisor")

        # Add keyword nodes and edges
        for keyword in supervisor.get("keywords", []):
            G.add_node(keyword, type="research_area")
            G.add_edge(supervisor_node, keyword)

    # Convert NetworkX graph to Pyvis graph
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    net.from_nx(G)

    # Customize appearance and add info for supervisor nodes
    for supervisor in supervisors:
        net_node = net.get_node(supervisor["name"])
        if net_node:  # Ensure the node exists in the network
            net_node['title'] = f"<b>{supervisor['name']}</b><br>{supervisor.get('description', 'No description available')}"
            net_node['color'] = 'cyan'
            net_node['url'] = supervisor.get("link", "#")  # Add URL for the supervisor profile

    # Customize keyword nodes appearance
    for keyword in {k for s in supervisors for k in s.get("keywords", [])}:  # Unique keywords
        net_node = net.get_node(keyword)
        if net_node:  # Ensure the node exists in the network
            net_node['title'] = f"<b>Research Area:</b> {keyword}"
            net_node['color'] = 'orange'

    # Save the interactive network as an HTML file
    net.save_graph(output_file)
    print(f"Network graph saved to {output_file}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Create an interactive network graph of supervisors and research areas.")
    parser.add_argument("input_file", type=str, help="Path to the input JSON file with supervisor data")
    parser.add_argument("output_file", type=str, help="Path to save the output HTML file")
    args = parser.parse_args()

    # Run the function with provided arguments
    create_supervisor_network(args.input_file, args.output_file)