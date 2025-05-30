import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.title("Welcome to the Grit Studio")
st.info("Your one-stop shop for cool and fun stuffs")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    The Grit Studio is a fun web-app deisgined to solve cool and fun problems
    for individuals.
    Our provided tools range from basic QR Code Makers to Advanced AI Apps.
    
    **👈 Select a utility from the sidebar** to see what we provide!

    ### Want to request a utility?
    - Send us a direct email [Here](mailto:iammomohsamuel@gmail.com?subject=Hello%20Samuel&body=I%20wanted%20to%20reach%20out%20about%20...)
"""
)

# Sidebar for navigation
with st.sidebar:
    st.sidebar.caption("We prioritize your privacy - no data is collected or processed")
    
    # Add social links in sidebar
    st.sidebar.markdown("### Connect with us")
    st.sidebar.markdown("[Linkedin](https://www.linkedin.com/in/samuel-o-momoh/) | [Twitter](https://twitter.com/griittyy) | [GitHub](https://github.com/GRIITTYY)")
    
    # App version
    st.sidebar.markdown("---")
    st.sidebar.caption("Version 1.0")