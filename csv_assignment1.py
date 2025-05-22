import os
import pandas as pd
import networkx as nx


pkl_input_folder = os.path.join( "pkl_files") # ".. " gaat één map omhoog


csv_output_folder_a1 = os.path.join( "csv_assignment1")


os.makedirs(csv_output_folder_a1, exist_ok=True)


# 1. Load pickles vanuit de map 'pkl_files'
original_pkl1_name = "montreal_L_space.pkl"
original_pkl2_name = "montreal_P_space.pkl2" # Let op: in je screenshot is dit .pkl2

path_obj1 = os.path.join(pkl_input_folder, original_pkl1_name)
path_obj2 = os.path.join(pkl_input_folder, original_pkl2_name)

print(f"Laden van: {path_obj1}")
obj1 = pd.read_pickle(path_obj1)
print(f"Laden van: {path_obj2}")
obj2 = pd.read_pickle(path_obj2)


# Helper to dump arbitrary Python objects
def dump_obj(obj, base_name, output_folder):
    # Case A: DataFrame → one CSV
    if isinstance(obj, pd.DataFrame):
        out_path = os.path.join(output_folder, f"{base_name}.csv") # Gebruik output_folder
        obj.to_csv(out_path, index=False)
        print(f"Wrote DataFrame → {out_path}")

    # Case B: NetworkX Graph → nodes.csv + edges.csv
    elif isinstance(obj, nx.Graph):
        # Nodes
        nodes = []
        for nid, data in obj.nodes(data=True):
            row = {"node": nid}
            row.update(data)
            nodes.append(row)
        df_nodes = pd.DataFrame(nodes)
        fn_nodes_path = os.path.join(output_folder, f"{base_name}_nodes.csv") # Gebruik output_folder
        df_nodes.to_csv(fn_nodes_path, index=False)
        print(f"Wrote Graph nodes → {fn_nodes_path}")

        # Edges
        edges = []
        for u, v, data in obj.edges(data=True):
            row = {"u": u, "v": v}
            row.update(data)
            edges.append(row)
        df_edges = pd.DataFrame(edges)
        fn_edges_path = os.path.join(output_folder, f"{base_name}_edges.csv") # Gebruik output_folder
        df_edges.to_csv(fn_edges_path, index=False)
        print(f"Wrote Graph edges → {fn_edges_path}")

    # Case C: dict, list of dicts, etc. → try converting to DataFrame
    else:
        try:
            df = pd.DataFrame(obj)
            fn_path = os.path.join(output_folder, f"{base_name}.csv") # Gebruik output_folder
            df.to_csv(fn_path, index=False)
            print(f"Wrote generic object → {fn_path}")
        except Exception as e:
            print(f"⚠️ Could not convert {base_name!r} to CSV: {e}")

# 2. Dump both naar de map 'csv_assignment1'
# AANGEPAST: csv_output_folder_a1 meegegeven aan dump_obj
dump_obj(obj1, "montreal_L_space", csv_output_folder_a1)
dump_obj(obj2, "montreal_P_space", csv_output_folder_a1)

print(f"\nCSV bestanden zijn opgeslagen in de map: {os.path.abspath(csv_output_folder_a1)}")