import matplotlib.pyplot as plt
import networkx as nx
import random
import os

import json

def generate_network_image(output_path):
    # Load themes
    themes_path = os.path.join(os.path.dirname(__file__), "..", "data", "themes.json")
    with open(themes_path, 'r') as f:
        themes_data = json.load(f)
    theme_titles = [t['title'] for t in themes_data]

    # Create a Small-World network for "intricate" community feel
    n = 180
    k = 6
    p = 0.1
    G = nx.watts_strogatz_graph(n, k, p, seed=55)
    
    # Add a few "hubs"
    hubs = []
    for _ in range(len(theme_titles)):
        hub = random.choice(list(G.nodes()))
        hubs.append(hub)
        for _ in range(15):
            target = random.choice(list(G.nodes()))
            if hub != target:
                G.add_edge(hub, target)
    
    # Calculate layout
    pos = nx.spring_layout(G, k=0.15, iterations=300, seed=55)
    
    # Select hubs that are spatially separated for better label placement
    degrees = dict(G.degree())
    hub_candidates = sorted(degrees.items(), key=lambda x: x[1], reverse=True)[:30]
    selected_hubs = []
    min_dist = 0.4
    
    for node, deg in hub_candidates:
        if len(selected_hubs) >= len(theme_titles):
            break
        
        # Check distance from already selected hubs
        too_close = False
        for other in selected_hubs:
            d = ((pos[node][0] - pos[other][0])**2 + (pos[node][1] - pos[other][1])**2)**0.5
            if d < min_dist:
                too_close = True
                break
        
        if not too_close:
            selected_hubs.append(node)

    # Create figure
    plt.figure(figsize=(12, 6.3), dpi=200) 
    plt.gca().set_facecolor('white')
    
    # Colors
    teal = '#00a9b7'
    navy = '#003d5b'
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color=navy, alpha=0.1, width=0.4)
    
    # Draw nodes
    node_sizes = [pow(v, 1.8) * 1.5 for v in degrees.values()]
    # Hubs are navy, others are teal
    node_colors = [navy if node in selected_hubs else teal for node in G.nodes()]
    
    nx.draw_networkx_nodes(G, pos, 
                           node_size=node_sizes, 
                           node_color=node_colors,
                           alpha=0.9,
                           linewidths=0.4,
                           edgecolors='white')

    # Sprinkle in Theme Labels
    for i, hub in enumerate(selected_hubs):
        if i < len(theme_titles):
            x, y = pos[hub]
            # Offset labels slightly for clarity
            plt.text(x, y + 0.06, theme_titles[i], 
                     fontsize=6, 
                     fontweight='bold',
                     fontfamily='sans-serif',
                     color=navy,
                     ha='center',
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=0.8))
    
    # Clean up
    plt.axis('off')
    plt.tight_layout()
    
    # Save
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close()

if __name__ == "__main__":
    # Ensure media directory exists relative to script or absolute
    output_dir = os.path.join(os.path.dirname(__file__), "..", "media")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, "thumbnail.png")
    generate_network_image(output_path)
    print(f"Generated spiderwebby thumbnail at {output_path}")
