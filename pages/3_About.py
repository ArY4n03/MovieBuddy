import streamlit as st

about = """
<p>
This is my side project during my winter vacation <br>
Just wanted to try TheMovieDataBase api

Github link to this project
</p>
"""

github_project_link = "https://github.com/ArY4n03/MovieBuddy"
st.html(about)
st.page_link(github_project_link,label="Project link", icon=None, help=None, disabled=False, use_container_width=None)