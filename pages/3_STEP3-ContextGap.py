import streamlit as st
st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    layout="wide"
)

topcol1, topcol2, topcol3 = st.columns([1,1,1])

with topcol1:
    with st.container(height=300):
        "#### Identify internal stakeholders"
        identifyIS_checkbox = st.checkbox("Check me to identify internal stakeholders")
        if identifyIS_checkbox:
            with st.status("Identifying internal stakeholders..."):
                conversation_data = st.session_state.messages
                file_Data = st.session_state.uploaded_files_content
                # st.write(conversation_data)
                st.write(file_Data)
                
with topcol2:
    with st.container(height=300):
        "#### Identify external stakeholders"
        identifyES_checkbox = st.checkbox("Check me to identify external stakeholders")
        if identifyES_checkbox:
            with st.status("Identifying external stakeholders..."):
                st.write("You have checked the box to identify external stakeholders")
    
with topcol3:
    with st.container(height=300):
        "#### Identify the context of the organization"
    
botcol1, botcol2= st.columns([1,1])

with botcol1:
    with st.container(
        # key="botcol1"
        ):
        st.write("# Welcome to ISOEnsure! 👋")
    
with botcol2:
    with st.container(
        # key="botcol2"
        ):
        st.write("ISOEnsure is aAI based Compliance tool for effectively establishing and monitoring a dynamic audit system for Small and Medium Enterprises (SMEs) and Startups. **👈 Select a STEP from the sidebar** to see some examples of what ISOENSURE can do!")