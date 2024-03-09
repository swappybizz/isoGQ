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
You are given an input in the form of a document, conversation, or other textual information, which you will use to extract relationships between the nodes. You will identify as many releavant nodes as possible with at least 1-3 relationships for each node. These relationships must be related to general information regarding the company, leadership and employees, operations, planning, support, finance, sales, marketing, product, technology, and other relevant areas. Relationships must contain actual names and details where possible.

Based on the information provided, you will generate Cypher queries to insert each node and its relationships into a graph database. Focus on the connections that involve aspects such as reporting structure, collaborative projects, departmental interactions, financial dependencies, product development pipelines, technology stacks, and market strategies.

Remember, your response should consist exclusively of Cypher queries for creating nodes and defining their relationships. Do not include comments, instructions, or any other content outside of these queries.

Text between the first and second '***' describes a company's scenario and provides an expample of how to respond. Use this information to generate Cypher queries for creating nodes and defining their relationships.
***
At TechSolutions, the Quality Assurance (QA) department plays a critical role in ensuring the company's software products, including CyberGuard and its new product line - SecureNet (a network security tool) and DataShield (a data encryption application), adhere to the highest quality standards. Led by Dave, the QA Manager, the department is gearing up for ISO 9001 certification to cement its commitment to continuous improvement and excellence in software quality.

Products Under QA Oversight:

CyberGuard: Enterprise security software offering comprehensive threat protection.
SecureNet: A network security tool designed to prevent unauthorized access and ensure data integrity across corporate networks.
DataShield: A data encryption application that provides end-to-end encryption for sensitive corporate data.
Leadership:

Dave: QA Manager, responsible for overseeing the department's ISO 9001 certification process and ensuring compliance with relevant quality standards.
Emma: Senior QA Analyst, specializes in automated testing for SecureNet, ensuring it meets specific security benchmarks.
Fiona: QA Specialist for DataShield, focuses on encryption standards and data privacy laws compliance.
Context and Stakeholders:

Internal Stakeholders: Technology department (led by Alice) relies on QA feedback for product enhancements. The Sales and Marketing departments (led by Carol and Bob, respectively) depend on the QA seal of approval to assure clients of product reliability.
External Stakeholders: CyberSafeCertifiers conduct external audits for ISO 9001 compliance. Clients and end-users expect the highest quality and security from TechSolutions products.
Laws and Regulations:

General Data Protection Regulation (GDPR): DataShield's development is heavily influenced by GDPR requirements to ensure data privacy and security for users in the European Union.
The Cybersecurity Information Sharing Act (CISA): SecureNet incorporates guidelines from CISA to facilitate the sharing of cyber threat indicators.
Impacted Departments:

The Technology department must adjust its development processes based on QA feedback, particularly concerning SecureNet's network security capabilities and DataShield's encryption mechanisms.
KPIs for Evaluation:

Defect Detection Rate: The percentage of detected defects before product release.
Customer Satisfaction Score: Based on feedback regarding the security and reliability of the products.
Compliance Rate: The degree to which products adhere to external regulations and internal standards.
Processes in Operations:

Automated Testing Pipeline: Managed by Emma, this process involves continuous testing of SecureNet using a suite of automated tools to identify vulnerabilities.
Encryption Standards Review: Fiona leads a quarterly review of DataShield's encryption algorithms to ensure they exceed industry standards and comply with new regulations.
ISO 9001 Preparation Meetings: Weekly meetings led by Dave to align QA processes with ISO standards, including documentation reviews and quality audits.
Quality Standards for Processes:

ISO/IEC 27001: For information security management, guiding the development and testing of SecureNet and DataShield.
OWASP Top 10: SecureNet's testing protocols include assessments against the OWASP Top 10 Web Application Security Risks.
By focusing on these specific aspects, the QA department at TechSolutions not only supports the company's mission to deliver top-quality cybersecurity products but also positions the firm for successful ISO 9001 certification, ensuring continuous improvement and adherence to best practices in software quality assurance.


YOUR RESPONSE BELOW:
CREATE (techDepartment:Department {{name: 'Technology', aim: 'ISO 27001 Certification'}})
CREATE (firewallPlus:Product {{name: 'Firewall Plus'}})
CREATE (intrusionDetector:Product {{name: 'Intrusion Detector'}})
CREATE (vpnGateway:Product {{name: 'VPN Gateway'}})
CREATE (dataEncryptor:Product {{name: 'Data Encryptor'}})
CREATE (alice:Employee {{name: 'Alice', role: 'Lead Developer'}})
CREATE (jack:Employee {{name: 'Jack', role: 'Security Architect'}})
CREATE (eva:Employee {{name: 'Eva', role: 'Compliance Manager'}})
CREATE (tom:Employee {{name: 'Tom', role: 'Senior Developer'}})
CREATE (lucy:Employee {{name: 'Lucy', role: 'Product Analyst'}})
CREATE (legalDepartment:Department {{name: 'Legal', focus: 'Compliance'}})
CREATE (salesDepartment:Department {{name: 'Sales', focus: 'Product Sales'}})
CREATE (hrDepartment:Department {{name: 'Human Resources', focus: 'Employee Well-being'}})
CREATE (financeDepartment:Department {{name: 'Finance', focus: 'Budget Management'}})
CREATE (cyberSafeCertifiers:ExternalEntity {{name: 'CyberSafeCertifiers', type: 'Auditor', specialization: 'ISO 27001'}})
CREATE (europeanPrivacyBoard:ExternalEntity {{name: 'European Privacy Board', type: 'Regulatory Body'}})
CREATE (gdpr:Regulation {{name: 'GDPR'}})
CREATE (iso27001:Standard {{name: 'ISO 27001'}})
CREATE (iso9001:Standard {{name: 'ISO 9001'}})
CREATE (securityDesignReview:Process {{name: 'Security Design Review'}})
CREATE (gdprComplianceCheck:Process {{name: 'GDPR Compliance Check'}})
CREATE (ciCd:Process {{name: 'CI/CD', description: 'Continuous Integration and Deployment'}})
CREATE (vulnerabilityAssessment:Process {{name: 'Vulnerability Assessment'}})
CREATE (codeReview:Process {{name: 'Code Review'}})
MERGE (techDepartment)-[:DEVELOPS]->(firewallPlus)
MERGE (techDepartment)-[:DEVELOPS]->(intrusionDetector)
MERGE (techDepartment)-[:DEVELOPS]->(vpnGateway)
MERGE (techDepartment)-[:DEVELOPS]->(dataEncryptor)
MERGE (alice)-[:LEADS]->(techDepartment)
MERGE (jack)-[:DESIGNS]->(securityDesignReview)
MERGE (eva)-[:ENSURES_COMPLIANCE]->(gdprComplianceCheck)
MERGE (techDepartment)-[:COLLABORATES_WITH]->(legalDepartment)
MERGE (techDepartment)-[:IMPACTS]->(salesDepartment)
MERGE (techDepartment)-[:RECEIVES_SUPPORT_FROM]->(hrDepartment)
MERGE (techDepartment)-[:COORDINATES_WITH]->(financeDepartment)
MERGE (techDepartment)-[:TARGETED_BY]->(cyberSafeCertifiers)
MERGE (firewallPlus)-[:COMPLIES_WITH]->(gdpr)
MERGE (intrusionDetector)-[:COMPLIES_WITH]->(gdpr)
MERGE (vpnGateway)-[:COMPLIES_WITH]->(iso27001)
MERGE (dataEncryptor)-[:COMPLIES_WITH]->(iso27001)
MERGE (techDepartment)-[:AIMS_FOR]->(iso27001)
MERGE (jack)-[:RESPONSIBLE_FOR]->(securityDesignReview)
MERGE (eva)-[:MANAGES]->(gdprComplianceCheck)
MERGE (alice)-[:OVERSEES]->(ciCd)
MERGE (tom)-[:PARTICIPATES_IN]->(vulnerabilityAssessment)
MERGE (lucy)-[:CONDUCTS]->(codeReview)
MERGE (firewallPlus)-[:SUBJECT_TO]->(securityDesignReview)
MERGE (intrusionDetector)-[:SUBJECT_TO]->(securityDesignReview)
MERGE (vpnGateway)-[:SUBJECT_TO]->(vulnerabilityAssessment)
MERGE (dataEncryptor)-[:SUBJECT_TO]->(codeReview)
MERGE (techDepartment)-[:USES]->(ciCd)
MERGE (securityDesignReview)-[:ADHERES_TO]->(iso27001)
MERGE (gdprComplianceCheck)-[:ADHERES_TO]->(iso27001)
MERGE (ciCd)-[:ADHERES_TO]->(iso27001)
MERGE (vulnerabilityAssessment)-[:SUPPORTS]->(iso27001)
MERGE (codeReview)-[:ENSURES_COMPLIANCE_WITH]->(iso27001)
MERGE (legalDepartment)-[:PROVIDES_GUIDANCE_TO]->(techDepartment)
MERGE (salesDepartment)-[:SELLS]->(firewallPlus)
MERGE (salesDepartment)-[:SELLS]->(intrusionDetector)
MERGE (salesDepartment)-[:SELLS]->(vpnGateway)
MERGE (salesDepartment)-[:SELLS]->(dataEncryptor)
MERGE (cyberSafeCertifiers)-[:AUDITS]->(techDepartment)
MERGE (europeanPrivacyBoard)-[:REGULATES]->(techDepartment)
MERGE (techDepartment)-[:FOLLOWS]->(gdpr)
MERGE (techDepartment)-[:SEEKS_CERTIFICATION_FROM]->(cyberSafeCertifiers)
MERGE (hrDepartment)-[:SUPPORTS]->(techDepartment)
MERGE (financeDepartment)-[:FINANCES]->(techDepartment)
MERGE (vpnGateway)-[:REQUIRES]->(securityDesignReview)
MERGE (dataEncryptor)-[:REQUIRES]->(gdprComplianceCheck)
MERGE (firewallPlus)-[:TESTED_BY]->(vulnerabilityAssessment)
MERGE (intrusionDetector)-[:REVIEWED_BY]->(codeReview)

... so on

    ###
    Data:
    {conversation_data}
    ###
    REMEMBER YOU MUST ONLY RETURN THE CYPER QUERIES
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
    "Visualise your Company's ISO-Graph"
    """---"""
uploaded_file = st.sidebar.file_uploader("Upload Text file/JSON From Previous Process or General Info", type=["json", "txt"])

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
    
    
# with st.sidebar.expander("Suggest Changes"):
#     suggestion1 = st.text_area("Suggestion 1")
#     suggestion2 = st.text_area("Suggestion 2")
#     if st.button("Submit"):
#         # Your code to handle the submitted suggestions goes here
#         st.success("Suggestions submitted successfully!")
        
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
        pos = nx.spring_layout(G, k=1.0, iterations=20)
        
        # Generate random colors for nodes
        colors = ["#" + ''.join(random.choices('0123456789ABCDEF', k=6)) for _ in G.nodes()]
        
        # Visualization
        plt.figure(figsize=(16, 16), facecolor='black')
        nx.draw_networkx_nodes(G, pos, node_color=colors, alpha=0.9)
        nx.draw_networkx_edges(G, pos, edge_color='white', alpha=0.5,)
        nx.draw_networkx_labels(G, pos, font_color='cyan')
        
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
                
                
                
    
        

