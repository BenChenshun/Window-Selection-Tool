import streamlit as st
from utils import Go_to_Location

# Sidebar navigation
# st.sidebar.title("Navigation")
# st.sidebar.markdown("Use the buttons below or the sidebar to navigate.")
# if st.sidebar.button("Previous Page"):
#     go_to_previous_page()
# if st.sidebar.button("Next Page"):
#     go_to_next_page()

st.title("Home: Welcome to the Window Selection Tool")
st.markdown(
    """
    Welcome to the Window Selection Tool!  
    Use the sidebar to navigate through the app.  
    - **Page 1**: Input your zip code.
    - **Page 2**: Enter house information.
    - **Page 3**: Specify window details.
    - **Page 4**: View the results.
    - Use **Next** and **Previous** buttons to navigate.
    """
)

Go_to_Location()

# elif st.session_state.page == 2:
#     import pages.Location
# elif st.session_state.page == 3:
#     import pages.Page_2
# elif st.session_state.page == 4:
#     import pages.Page_3
# elif st.session_state.page == 5:
#     import pages.Page_4