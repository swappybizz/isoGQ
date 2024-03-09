import streamlit as st
from openai import OpenAI
import re,os

import math
import networkx as nx
import matplotlib.pyplot as plt
import random

def generate_text(prompt:str):
    print("§§§§ $$$ CAUTION: A COSTING CALL#### IS BEING MADE $$$ §§§§")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(
        
       api_key=openai_api_key
    )
    completion = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    # print(type(completion.choices[0].message.content))
    return str(completion.choices[0].message.content)

def extract_relationship(conversation_data: str):
    
    prompt = f"""
You are given an input in the form of a document, conversation, or other textual information, which you will use to extract relationships between the nodes. You will identify 25 nodes and at least 1 (preferably 3 or more) relationships for each node. These relationships must be related to general information regarding the company, leadership and employees, operations, planning, support, finance, sales, marketing, product, technology, and other relevant areas. Relationships must contain actual names and details where possible.

Based on the information provided, you will generate Cypher queries to insert each node and its relationships into a graph database. Focus on the connections that involve aspects such as reporting structure, collaborative projects, departmental interactions, financial dependencies, product development pipelines, technology stacks, and market strategies.

Remember, your response should consist exclusively of Cypher queries for creating nodes and defining their relationships. Do not include comments, instructions, or any other content outside of these queries.

Here is how you might structure a response for a company with entities related to 'Employee', 'Department', and 'Project', with 'Alice' as an example employee working in the 'Technology' department on a 'NewProductLaunch' project:

CREATE (Employee:Person {{name: 'Alice', role: 'Software Developer'}})
CREATE (Department:Department {{name: 'Technology'}})
CREATE (Project:Project {{name: 'NewProductLaunch'}})
MERGE (Employee)-[:WORKS_IN]->(Department)
MERGE (Employee)-[:CONTRIBUTES_TO]->(Project)
CREATE (Employee2:Person {{name: 'Bob', role: 'Project Manager'}})
MERGE (Employee2)-[:MANAGES]->(Project)
CREATE (Department2:Department {{name: 'Marketing'}})
... so on

    ###
    Data:
    {conversation_data}
    ###
    
    """
    return generate_text(prompt)

def extract_nodes(cypher_string):
    node_pattern = re.compile(r'CREATE \((?P<node>\w+):(?P<type>\w+) \{')
    return {match.group('node'): match.group('type') for match in node_pattern.finditer(cypher_string)}

def extract_node_relationships(cypher_string):
    relationship_pattern = re.compile(r'MERGE \((?P<source>\w+)\)-\[:(?P<relation>\w+)\]->\((?P<target>\w+)\)')
    return [(match.group('source'), match.group('target'), match.group('relation')) for match in relationship_pattern.finditer(cypher_string)]


st.set_page_config(page_title="ISOGRAPHQ", page_icon="🔍", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("ISOGRAPHQ")
# st.session_state["file_contents"] if not already in session state, initialize it to an empty string
if "file_contents" not in st.session_state:
    st.session_state["file_contents"] = ""
    
if "nodes" not in st.session_state:
    st.session_state["nodes"] = ""
    
if "relationships" not in st.session_state:
    st.session_state["relationships"] = ""
    

with st.sidebar:
    "Isomorphic Graph Querying"
    """---"""
uploaded_file = st.sidebar.file_uploader("Upload JSON or TXT file", type=["json", "txt"])

# # topic = st.sidebar.text_input("Enter a Topic",placeholder="Hit ↩️Enter")
# number_of_nodes = st.sidebar.number_input("Number of Nodes to Identify ", min_value=1, max_value=100, value=10)

if uploaded_file is not None:
    # if its a json file convert it to string and replace the session state
    if uploaded_file.type == "application/json":
        file_contents = str(uploaded_file.getvalue())
        st.session_state["file_contents"] = file_contents
        
    elif uploaded_file.type == "text/plain":
        file_contents = uploaded_file.getvalue().decode("utf-8")
        st.session_state["file_contents"] = file_contents
    
    
with st.sidebar.expander("Suggest Changes"):
    suggestion1 = st.text_area("Suggestion 1")
    suggestion2 = st.text_area("Suggestion 2")
    if st.button("Submit"):
        # Your code to handle the submitted suggestions goes here
        st.success("Suggestions submitted successfully!")
        
with st.sidebar:   
    "---"
    log_expander =  st.sidebar.expander("Log", )
    file_contents = st.session_state["file_contents"]
    log_expander.code(file_contents)






def draw_graph_in_grid_layout(data):
    if "```cypher" in data:
        lines_that_start_with_create = [line for line in data.split("\n") if line.startswith("CREATE")]
        node_data = []  
        for line in lines_that_start_with_create:
            node_data.append(line.split("(")[1].split("{")[0])
    
    # Ensure only unique nodes are added to the graph
    unique_node_data = set(node_data)
    G = nx.Graph()
    G.add_nodes_from(unique_node_data)
    
    # Use the length of unique_node_data for num_nodes
    num_nodes = len(unique_node_data)
    grid_size = math.ceil(math.sqrt(num_nodes))
    spacing = 1
    node_size = max(100, 10000 // num_nodes)
    font_size = max(10, 16 // grid_size)
    
    # Generate random colors for nodes, matching the number of unique nodes
    colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in range(num_nodes)]
    
    # Calculate node positions
    pos = {node: (col * spacing, -row * spacing) for i, node in enumerate(G.nodes()) for row in [i // grid_size] for col in [i % grid_size]}
    
    # Visualization with black background
    plt.figure(figsize=(24, 12), facecolor='black')
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=colors, alpha=0.9)
    nx.draw_networkx_labels(G,
                            pos,
                            font_size=font_size,
                            font_color='white',
                            font_weight='bold',
                            verticalalignment='top',)
    plt.axis('off')
    st.pyplot(plt)  # Display the plot in Streamlit

def draw_relationships(data):
    if "```cypher" in data:
        lines_that_start_with_merge = [line for line in data.split("\n") if line.startswith("MERGE")]
        G = nx.Graph()
        
        for line in lines_that_start_with_merge:
            # Using regular expressions to extract node and relationship information
            entities = re.findall(r"\((.*?)\)", line)
            relationship = re.search(r"\[(.*?)\]", line)
            
            if entities and relationship and len(entities) >= 2:
                # Extract the first and second entity names
                firstEntity = entities[0]
                secondEntity = entities[1]
                relationshipType = relationship.group(1).split(":")[1] if ':' in relationship.group(1) else relationship.group(1)
                
                # Add nodes and edge with relationship type as label
                G.add_node(firstEntity)
                G.add_node(secondEntity)
                G.add_edge(firstEntity, secondEntity, label=relationshipType)
        
        # Generate positions for each node using the spring layout for aesthetics
        pos = nx.spring_layout(G)
        
        # Generate random colors for nodes
        colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in G.nodes()]
        
        # Visualization
        plt.figure(figsize=(12, 12), facecolor='black')
        nx.draw_networkx_nodes(G, pos, node_color=colors, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color='white', alpha=0.5)
        nx.draw_networkx_labels(G, pos, font_color='white')
        
        # Optionally, draw edge labels to show relationship types
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
        
        plt.axis('off')
        st.pyplot(plt)

        


if len(st.session_state["file_contents"]) > 0:
    nodes = extract_relationship((str(st.session_state["file_contents"])))
    st.session_state["file_contents"] = nodes
    print(nodes)
    # col1, col2 = st.columns(2)
    with st.expander("Visualize relationships", expanded=True):
        draw_relationships(st.session_state["file_contents"])
        
    
    with st.expander("Visualize nodes"):
        draw_graph_in_grid_layout(st.session_state["file_contents"])
        
    with st.expander("Extracted Nodes and Relationships"):
        st.code(st.session_state["file_contents"], language='cypher')
    with st.expander("Download Neo4j Graph"):
        nodes = extract_nodes(st.session_state["file_contents"])
        relationships = extract_node_relationships(st.session_state["file_contents"])
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.write("Nodes")
                st.session_state["nodes"] = nodes
                st.code(nodes)
        with col2:
            with st.container():
                st.write("Relationships")
                st.session_state["relationships"] = relationships
                st.code(relationships)
                
                
                
    
        

