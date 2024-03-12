import streamlit as st
from openai import OpenAI
import re, os
import json

import math
import networkx as nx
import matplotlib.pyplot as plt
import random

# from streamlit_agraph import agraph, Node, Edge, Config
# from streamlit_agraph.config import Config, ConfigBuilder


def generate_text(prompt: str):
    print("§§§§ $$$ CAUTION: A COSTING CALL#### IS BEING MADE $$$ §§§§")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=openai_api_key)
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


if "messages" not in st.session_state:
    st.session_state.messages = []
if "nodes_data" not in st.session_state:
    st.session_state.nodes = []
    
if "rel_data" not in st.session_state:
    st.session_state.edges = []
    
if "init_cycher_query" not in st.session_state:
    st.session_state.init_cycher_query = []

with st.expander("Conversation Data"):
    st.write(st.session_state["messages"])


with st.sidebar:
    st.subheader("Extract Nodes and Relationships")
    st.write(
        "This section is responsible for extracting nodes and relationships from the conversation data"
    )
    with st.expander("Extracted Nodes and Relationships"):
        if st.session_state["init_cycher_query"]:
            st.write(st.session_state["init_cycher_query"])


def draw_relationships(data):
    lines_that_start_with_merge = [
        line for line in data.split("\n") if line.startswith("MERGE")
    ]
    # Switch to a directed graph to incorporate directions
    G = nx.DiGraph()

    for line in lines_that_start_with_merge:
        # Using regular expressions to extract node and relationship information
        entities = re.findall(r"\((.*?)\)", line)
        relationship = re.search(r"\[(.*?)\]", line)

        if entities and relationship and len(entities) >= 2:
            # Extract the first and second entity names
            firstEntity = entities[0]
            secondEntity = entities[1]
            relationshipType = (
                relationship.group(1).split(":")[1]
                if ":" in relationship.group(1)
                else relationship.group(1)
            )

            # Add nodes and edge with relationship type as label, respecting direction
            G.add_node(firstEntity)
            G.add_node(secondEntity)
            G.add_edge(firstEntity, secondEntity, label=relationshipType)

    # Generate positions for each node using the spring layout for aesthetics
    pos = nx.spring_layout(G, k=1.0, iterations=20)

    # Generate random colors for nodes
    colors = ["#" + "".join(random.choices("0123456789ABCDEF", k=6)) for _ in G.nodes()]

    # screen_height = st._get_block_container().height
    # screen_width = st._get_block_container().width
    plt.figure(figsize=(24, 18), facecolor="black")
    nx.draw_networkx_nodes(G, pos, node_color=colors, alpha=0.9)
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="white",
        alpha=0.5,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=10,
    )
    nx.draw_networkx_labels(G, pos, font_color="cyan")

    # Optionally, draw edge labels to show relationship types
    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.axis("off")
    st.pyplot(plt)


# st.expander("Extracted Nodes and Relationships")
conversation_data = st.session_state["messages"]
conversation_string = json.dumps(conversation_data)
if len(conversation_string) > 2:
    with st.form(key="extract_nodes_and_relationships"):
        user_password = st.text_input(
            "Enter your user_passcode, Only valid Signatories proceed to next step",
            type="password",
        )
        if st.form_submit_button("Extract Nodes and Relationships"):
            with st.status("Extracting nodes and relationships..."):
                extracted_cypher = extract_relationship(conversation_string)
                st.session_state["init_cycher_query"] = extracted_cypher
                st.session_state["user_details"] = user_password
                if user_password in [
                    "testswap",
                    "testterje",
                    "testlars",
                    "teststig",
                    "test",
                ]:
                    draw_relationships(extracted_cypher)
                else:
                    st.error("Invalid user_passcode")


# with st.sidebar:
#     with st.expander("extracted user details", expanded=True):
#         if len(st.session_state["user_details"]) > 0:
#             if st.session_state["user_details"] in ["testswap","testterje","testlars","teststig","testuser"]:
#                 if st.session_state["user_details"] == "testswap":
#                     name = "Swapnil"

#                 elif st.session_state["user_details"] == "testterje":
#                     name = "Terje"

#                 elif st.session_state["user_details"] == "testlars":
#                     name = "Lars"

#                 elif st.session_state["user_details"] == "teststig":
#                     name = "Stig"
#                 elif st.session_state["user_details"] == "test":
#                     name = "Generic User"


#                     st.write (f"We have detected that you are {name} and you are authorized to view the extracted nodes and relationships")
#                     f"The Name below shall be the signatory for this process"
#                     signatory= st.text_input("Signatory", name)

#                     with st.button("Submit"):
#                         st.session_state["verified_signatory"] = signatory
