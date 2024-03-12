import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "nodes_data" not in st.session_state:
    st.session_state.nodes = []

if "rel_data" not in st.session_state:
    st.session_state.edges = []
    
if "init_cycher_query" not in st.session_state:
    st.session_state.init_cycher_query = []
    
if "user_details" not in st.session_state:
    st.session_state.user_details = []
    
st.write("# Welcome to ISOEnsure! 👋")

st.sidebar.success("Select a STEP.")

st.markdown(
    """
    ISOEnsure is aAI based Compliance tool for effectively establishing and monitoring a dynamic audit system for Small and Medium Enterprises (SMEs) and Startups.
    **👈 Select a STEP from the sidebar** to see some examples
    of what ISOENSURE can do!
    ### Want to learn more?
    - Check out [noffice.no](https://www.nooffice.no)
    - Jump into our [documentation](https://www.nooffice.no)
    - Ask a question in our [community
        forums](https://www.nooffice.no)
    ### See more complex demos
    - Use Consultation 👨‍🦳👭 [ISO-Cosultation](https://www.nooffice.no)
    - Explore a [Mock audit on Norsk AS](https://www.nooffice.no)
"""
)