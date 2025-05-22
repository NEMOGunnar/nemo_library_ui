import streamlit as st
from streamlit_option_menu import option_menu
from nemo_library import NemoLibrary

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "nemo_library" not in st.session_state:
    st.session_state.nemo_library = None


def login():
    st.title("Login")

    with st.form("login_form"):
        environment = st.selectbox(
            "Select Environment",
            ("prod", "test", "dev", "challenge", "demo"),
            index=3,
        )
        tenant = st.text_input("Tenant", value="mig")
        userid = st.text_input("Username", value="schug_g_mig")
        password = st.text_input("Password", type="password", value="totvy8-xurpap-nusZiq")
        submitted = st.form_submit_button("Login")

        if submitted:
            nl = NemoLibrary(
                environment=environment,
                tenant=tenant,
                userid=userid,
                password=password,
            )

            nl.testLogin()
            st.session_state.logged_in = True
            st.session_state.nemo_library = nl
            st.success("Login successful!")

            # Force re-run to reload UI based on new login state
            st.rerun()


# Show login form or main app
if not st.session_state.logged_in:
    login()
else:

    # Function to get the NemoLibrary instance
    def getNL():
        if st.session_state.nemo_library is None:
            st.error("NemoLibrary instance not found in session state.")
            return None
        return st.session_state.nemo_library
    
    st.set_page_config(layout="wide")
    
    # Title bar of the application
    st.title("User Interface for NEMO Library")
    st.markdown(
        "This is a user interface for the NEMO library, allowing users to interact with NEMO's functionalities."
    )

    with st.sidebar:
        st.markdown(
            f"**Version:** {NemoLibrary.__version__}"
        )  # Display version in the sidebar

        menu = option_menu(
            "Menu",
            [
                "Projects",
            ],
            icons=["briefcase"],  # Add icons for better UI
            menu_icon="menu-app",  # Icon for the menu
            default_index=0,  # Default selected menu
        )

    if menu == "Projects":
        st.subheader("Projects")
        st.markdown(
            "This section allows you to manage and interact with projects."
        )
        tabs = st.tabs(
            [
                "Project List",
            ]
        )  # Create tabs for different functionalities
        with tabs[0]:
            nl = getNL()
            projects = nl.getProjects()

            # Display projects in a grid control
            if projects:
                # Assuming projects is a list of dictionaries
                st.dataframe(
                    projects, use_container_width=True, height=600
                )  # Display as a grid with max width and custom height
            else:
                st.write("No projects found.")
        