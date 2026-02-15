"""Home page of the BAI2 Reader UI"""

import streamlit as st

st.write("""
# Welcome to the BAI2 Reader!
""")

pg = st.navigation(
    [
        st.Page("bai2_reader_app.py", title="BAI2 Reader", default=True),
        st.Page("examples.py", title="Examples"),
        st.Page("about.py", title="About"),
    ]
)
pg.run()
