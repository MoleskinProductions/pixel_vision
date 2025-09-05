import json
import networkx as nx
import pickle
import sys
import os


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
        # Add an asset node with its attributes.
        G.add_node(asset_id, **asset, node_type="asset")
        
        # Create a category node for the 'subtype' if available.
        subtype = asset.get("subtype", "").strip()
        if subtype:
            cat_node = f"cat:{subtype.lower()}"
            if cat_node not in G:
                G.add_node(cat_node, name=subtype, node_type="category")
            G.add_edge(asset_id, cat_node)
        
        # Create a subcategory node for the 'subsubtype' if available.
        subsubtype = asset.get("subsubtype", "").strip()
        if subsubtype:
            subcat_node = f"subcat:{subsubtype.lower()}"
            if subcat_node not in G:
                G.add_node(subcat_node, name=subsubtype, node_type="sub_category")
            G.add_edge(asset_id, subcat_node)
            # Also, connect the category and subcategory nodes.
            if subtype:
                G.add_edge(cat_node, subcat_node)
        
        # Create tag nodes for each tag.
        tags = asset.get("tags", [])
        for tag in tags:
            tag_node = f"tag:{tag.lower()}"
            if tag_node not in G:
                G.add_node(tag_node, name=tag, node_type="tag")
            G.add_edge(asset_id, tag_node)
    
    # Save the graph as a pickle file.
    with open(output_pkl_path, 'wb') as f:
        pickle.dump(G, f)
    print(f"Graph saved to {output_pkl_path}")

if __name__ == "__main__":
    master_json_path = "/media/frank-martinelli/SSD-001/A1.MK.PxVision/MXP/data/material_master/material_master.json"
    output_pkl_path = "/media/frank-martinelli/SSD-001/A1.MK.PxVision/MXP/data/material_master/material_master_graph.pkl"
    build_material_graph(master_json_path, output_pkl_path)
