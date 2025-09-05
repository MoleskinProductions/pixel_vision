import networkx as nx

def search_assets_by_tag(G: nx.Graph, tag: str):
    """
    Returns a set of asset node IDs that are connected to the tag node.
    The tag node is expected to be named "tag:<tag>" (in lowercase).
    """
    tag_node = f"tag:{tag.lower()}"
    if tag_node not in G:
        return set()
    # Neighbors of tag node that are assets.
    assets = {n for n in G.neighbors(tag_node) if G.nodes[n].get("node_type") == "asset"}
    return assets

def search_assets_by_category(G: nx.Graph, category: str):
    """
    Returns a set of asset node IDs that are connected to the category node.
    The category node is expected to be named "cat:<category>" (in lowercase).
    """
    cat_node = f"cat:{category.lower()}"
    if cat_node not in G:
        return set()
    assets = {n for n in G.neighbors(cat_node) if G.nodes[n].get("node_type") == "asset"}
    return assets

def search_assets_by_subcategory(G: nx.Graph, subcategory: str):
    """
    Returns a set of asset node IDs that are connected to the subcategory node.
    The subcategory node is expected to be named "subcat:<subcategory>" (in lowercase).
    """
    subcat_node = f"subcat:{subcategory.lower()}"
    if subcat_node not in G:
        return set()
    assets = {n for n in G.neighbors(subcat_node) if G.nodes[n].get("node_type") == "asset"}
    return assets

def search_assets(G: nx.Graph, tags=None, category=None, subcategory=None):
    """
    Returns the set of asset node IDs that match all provided criteria.
    
    :param tags: A list of tags (e.g. ["city", "street"]) that should all be matched.
    :param category: A string for the category (subtype), e.g. "tiles".
    :param subcategory: A string for the subcategory (subsubtype), e.g. "sidewalk".
    """
    # Start with the set of all asset nodes.
    assets_all = {n for n, attr in G.nodes(data=True) if attr.get("node_type") == "asset"}
    result = assets_all

    if tags:
        # For each tag, intersect with the assets matching that tag.
        for tag in tags:
            assets_by_tag = search_assets_by_tag(G, tag)
            result = result.intersection(assets_by_tag)
    
    if category:
        assets_by_cat = search_assets_by_category(G, category)
        result = result.intersection(assets_by_cat)
        
    if subcategory:
        assets_by_subcat = search_assets_by_subcategory(G, subcategory)
        result = result.intersection(assets_by_subcat)
        
    return result

def print_assets(G: nx.Graph, asset_ids):
    """
    Utility function to print details (e.g. name, usd_path) of asset nodes.
    """
    for aid in asset_ids:
        attr = G.nodes[aid]
        name = attr.get("name", "Unnamed")
        usd_path = attr.get("usd_path", "No USD path")
        print(f"Asset ID: {aid}\n  Name: {name}\n  USD Path: {usd_path}\n")

# Example usage:
if __name__ == "__main__":
    # Load your graph (assuming you saved it as a pickle from the previous script).
    import pickle
    with open("/media/frank-martinelli/SSD-001/A1.MK.PxVision/MXP/data/material_master/material_master_graph.pkl", "rb") as f:
        G = pickle.load(f)
    
    # Example 1: Search for assets tagged with "city"
    assets_tag = search_assets_by_tag(G, "city")
    print("Assets with tag 'city':")
    print_assets(G, assets_tag)
    
    # Example 2: Search for assets in category "tiles" and subcategory "sidewalk"
    assets_cat = search_assets(G, category="tiles", subcategory="sidewalk")
    print("Assets in category 'tiles' and subcategory 'sidewalk':")
    print_assets(G, assets_cat)
    
    # Example 3: Combined search: assets with tag "city" and in category "tiles"
    assets_combined = search_assets(G, tags=["city"], category="tiles")
    print("Assets with tag 'city' and in category 'tiles':")
    print_assets(G, assets_combined)
