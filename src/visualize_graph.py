import networkx as nx
import matplotlib.pyplot as plt
from app import create_app, db
from adapters.output.persistence.sqlalchemy.models.tag import (
    TagModel,
    TagRelationshipModel,
)


def create_mood_graph():
    """Create and visualize the mood relationship graph."""
    # Create graph
    G = nx.Graph()

    # Get all tags and relationships from database
    app = create_app()
    with app.app_context():
        tags = TagModel.query.all()
        relationships = TagRelationshipModel.query.all()

        print(f"Found {len(tags)} tags and {len(relationships)} relationships")

        if not tags or not relationships:
            print("No data found in database. Please run data_test.py first.")
            return

        # Add nodes (tags)
        for tag in tags:
            G.add_node(tag.name)
            print(f"Added node: {tag.name}")

        # Add edges (relationships)
        for rel in relationships:
            # Only add one edge between nodes (relationships are bidirectional)
            if not G.has_edge(rel.source_tag_name, rel.target_tag_name):
                G.add_edge(rel.source_tag_name, rel.target_tag_name, weight=rel.weight)
                print(
                    f"Added edge: {rel.source_tag_name} -- {rel.weight} -- {rel.target_tag_name}"
                )

    print(f"\nGraph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Set up the plot with a white background
    plt.figure(figsize=(20, 20), facecolor="white")

    # Create layout with more space between nodes
    pos = nx.spring_layout(G, k=2, iterations=100, seed=42)

    # Draw edges with varying thickness based on weight
    edge_weights = [G[u][v]["weight"] * 3 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, width=edge_weights, alpha=0.5, edge_color="gray")

    # Draw nodes with white background for better visibility
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color="lightblue",
        node_size=3000,
        alpha=0.7,
        edgecolors="black",
        linewidths=1,
    )

    # Draw labels with larger font
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    # Draw edge labels (weights) with background
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=8,
        bbox=dict(facecolor="white", edgecolor="none", alpha=0.7),
    )

    # Set title and remove axes
    plt.title("Mood Relationship Graph", fontsize=16, pad=20)
    plt.axis("off")

    # Adjust layout to prevent label cutoff
    plt.tight_layout()

    # Save the plot with high resolution
    plt.savefig(
        "mood_graph.png", format="png", dpi=300, bbox_inches="tight", facecolor="white"
    )
    plt.close()

    print("\nGraph has been saved as 'mood_graph.png'")


if __name__ == "__main__":
    create_mood_graph()
