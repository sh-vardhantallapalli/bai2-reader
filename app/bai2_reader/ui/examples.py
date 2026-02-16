"""This is UI page where users can download some sample BAI files"""

import streamlit as st
from pathlib import Path


st.write("""Sample BAI2 format files""")

st.info(
    "We only show top 10 lines in the file, click Download to see the entire file", icon=":material/info:", width=600
)
st.write("")

for file in sorted(Path(Path(__file__).parent.parent, "samples").glob("*.bai")):
    with open(file) as input_file:
        data = input_file.read()

    file_name = Path(file).name

    st.write(file_name.upper())
    st.code("\n".join(data.split("\n")[:10]))

    st.download_button(
        label=f"Download {file_name}",
        data=data,
        file_name=file_name,
        on_click="ignore",
        type="primary",
        icon=":material/download:",
    )

    st.write("")
