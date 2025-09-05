import json
import networkx as nx
import pickle
import sys
import os

def add_to_geometry_master(json_file, updated):
    """
    Adds the contents of a JSON file to a geometry master file.
    """
    # Load the new geometry data
    # Check if the file exists

    # if not os.path.exists(geometry_master_file):
    #     with open(geometry_master_file, "w") as f:
    #         json.dump({}, f)
    #         print(f"Created new master file: {geometry_master_file}")

    # Load the existing geometry master data
    with open(json_file, "r") as f:
        data_in = json.load(f)

    for id, data in data_in.items():
        if not data.get("usd_path", False):
            data_in[id]["usd_path"] = ""

    
    with open(updated, "w") as f:
        json.dump(data_in, f, indent=4)
        print(f"Updated {updated} with new geometry data from {json_file}")  


def build_material_graph(master_json_path, output_pkl_path):
    # Load the master JSON file.
    with open(master_json_path, 'r') as f:
        master_data = json.load(f)
    
    G = nx.Graph()
    
    # Assume master_data is a dict mapping asset IDs to asset entries.
    if isinstance(master_data, dict):
        items = master_data.items()
    elif isinstance(master_data, list):
        # If it's a list, enumerate it.
        items = enumerate(master_data)
    else:
        print("Unsupported JSON format.")
        return

    for asset_id, asset in items:
        tags = asset.get("tags", [])
        dimensions = asset.get("dimensions", [])
        thumbnail = asset.get("thumbnail", "")

        # Add an asset node with its attributes.
        G.add_node(asset_id, **asset, node_type="asset")
        
        # Create a category node for the 'subtype' if available.

        # Create tag nodes for each tag.
        
        for tag in tags:
            tag_node = f"tag:{tag.lower()}"
            if tag_node not in G:
                G.add_node(tag_node, name=tag, node_type="tag")
            G.add_edge(asset_id, tag_node)
    
    # Save the graph as a pickle file.
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph saved to {output_pkl_path}")