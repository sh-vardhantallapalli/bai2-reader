"""BAI2 Reader UI"""

import uuid
import os
import json
import tempfile
import streamlit as st
from typing import Dict
from bai2_reader.src.reader import BAI2Reader, bai_to_flat_dataframe
from bai2_reader.src.models import Bai2Model


def add_new_lines(n=1):
    """Adds input n number of empty lines to UI"""
    for _ in range(n):
        st.markdown("<br>", unsafe_allow_html=True)


def handle_file_upload():
    """Run for every file upload"""
    if st.session_state.get(f"uploader_{st.session_state.file_uploader_key}") is not None:
        temp_dir = tempfile.mkdtemp()
        abs_file_path = os.path.join(temp_dir, str(uuid.uuid4()))
        with open(abs_file_path, "wb") as f:
            f.write(st.session_state[f"uploader_{st.session_state.file_uploader_key}"].getbuffer())
        reader = BAI2Reader(
            write_to_files=False,
            run_validation=run_validation,
            encoding=encoding,
        )
        reader.read_file(file_path=abs_file_path)
        st.session_state.uploaded_file_data = reader.bai_data
    else:
        st.session_state.file_uploader_key += 1
        st.session_state.uploaded_file_data = None


def dict_to_form(
    input_dict: Dict,
    num_of_sections: int = 2,
    **kwargs,
) -> None:
    """Converts any python dict to a form like structure.
    :param input_dict: input dictionary
    :param num_of_sections: How many side by side columns you need default is 2 parallel columns
    """
    with st.container():
        parallel_sections = st.columns([1] * num_of_sections, **kwargs)
        columns = list(input_dict.keys())
        sep_length = int(len(columns) / num_of_sections)
        for section in range(num_of_sections):
            for each_column in columns[section if section == 0 else section * sep_length : (section + 1) * sep_length]:
                with parallel_sections[section]:
                    st.text(each_column.upper())
                    st.code(input_dict[each_column])
                    # st.text_input(each_column.upper(), input_dict[each_column], disabled=True)
                    # st.write(f"{each_column.upper()}: {input_dict[each_column]}")


st.set_page_config(page_title="BAI2 Reader", layout="wide")
top_col_left, top_col_right = st.columns([4, 1], gap="medium")

# 1. Initialize session state variables
if "file_uploader_key" not in st.session_state:
    st.session_state.file_uploader_key = 0
if "uploaded_file_data" not in st.session_state:
    st.session_state.uploaded_file_data: Bai2Model | None = None

custom_css = """
.uploadedFiles {
    display: none;
}

"""
st.markdown(f"<style>{custom_css}</style>", unsafe_allow_html=True)


with top_col_left:
    # 3. Use the file uploader with a unique key and a callback
    uploaded_file = st.file_uploader(
        label="Upload BAI File",
        key=f"uploader_{st.session_state.file_uploader_key}",
        on_change=handle_file_upload,
        accept_multiple_files=False,
        width=400,
    )

with top_col_right:
    st.write("Settings")
    encoding = st.selectbox(
        "Encoding",
        ("utf-8", "ascii", "cp037", "utf_32", "utf_16"),
        index=0,
        help="About encodings: https://docs.python.org/3/library/codecs.html#standard-encodings",
        accept_new_options=True,
    )

    run_validation = st.checkbox("Run Validations", False)

# 4. Process the file data if available in session state
if st.session_state.uploaded_file_data is not None:
    tabular_view, class_view, json_view = st.tabs(["Tabular View", "Classic View", "JSON View"])
    add_new_lines(1)

    # Read the data from the stored buffer
    bai_df = bai_to_flat_dataframe(st.session_state.uploaded_file_data)

    with tabular_view:
        tabular_view_left, tabular_view_right = st.columns([4, 1], gap="medium")

        with tabular_view_right:
            add_new_lines(2)
            remove_file_header = st.checkbox("Remove File Header Columns", True)
            remove_group_header = st.checkbox("Remove Group Header Columns", False)
            remove_group_trailer = st.checkbox("Remove Group Trailer Columns", False)
            remove_file_trailer = st.checkbox("Remove File Trailer Columns", True)

    with tabular_view_left:
        bai_columns = bai_df.columns
        col_config = {
            "account_identifier_opening_balance": st.column_config.NumberColumn(format="dollar"),
            "transaction_amount": st.column_config.NumberColumn(format="dollar"),
        }

        if remove_file_header:
            for col in bai_columns:
                if col.startswith("file_header_"):
                    col_config[col] = None

        if remove_file_trailer:
            for col in bai_columns:
                if col.startswith("file_trailer_"):
                    col_config[col] = None

        if remove_group_header:
            for col in bai_columns:
                if col.startswith("group_header_"):
                    col_config[col] = None

        if remove_group_trailer:
            for col in bai_columns:
                if col.startswith("group_trailer_"):
                    col_config[col] = None

        add_new_lines(2)
        st.dataframe(bai_df, column_config=col_config, width="stretch", height=800, hide_index=True)

    with json_view:
        json_view_left, json_view_right = st.columns([4, 1], gap="medium")

        with json_view_right:
            st.info("Hiding columns in JSON View is not supported", icon=":material/info:")
            add_new_lines(1)
            # expand_all = st.button("Expand All sections", icon=":material/add:")
            # collapse_all = st.button("Collapse all sections", icon=":material/remove:")
            code_view = st.checkbox("View JSON as code", False, help="Allows you to Copy entire JSON")
            # collapse_all = st.button("Collapse all sections", icon=":material/remove:")

        with json_view_left:
            add_new_lines(2)
            # st.write(bai_df.to_dict(orient='records'))
            # st.write(bai_to_json(st.session_state.uploaded_file_data))
            if code_view:
                st.code(st.session_state.uploaded_file_data.model_dump_json(indent=2), language="json")
            else:
                st.write(json.loads(st.session_state.uploaded_file_data.model_dump_json()))

    with class_view:
        class_view_left, class_view_right = st.columns([4, 1], gap="medium")

        with class_view_right:
            st.info("Hiding columns in Classic View is not supported", icon=":material/info:")
            add_new_lines(1)
            # expand_all = st.button("Expand All sections", icon=":material/add:")
            # collapse_all = st.button("Collapse all sections", icon=":material/remove:")
            expand_all = st.checkbox(":material/add: Expand All sections", False)
            # collapse_all = st.button("Collapse all sections", icon=":material/remove:")

        with class_view_left:
            # st.write(st.session_state.uploaded_file_data)
            add_new_lines(2)
            with st.container(width=1500, horizontal_alignment="center"):
                with st.expander("File Header"):
                    dict_to_form(st.session_state.uploaded_file_data.header.model_dump(), gap="large")
                for group_cntr, group in enumerate(st.session_state.uploaded_file_data.groups, 1):
                    with st.expander(
                        f"Group - {group_cntr}", expanded=True if group_cntr == 1 or expand_all else False
                    ):
                        dict_to_form(group.group_header.model_dump(), gap="large", width=800, num_of_sections=3)
                        with st.container(width=1000):
                            for account in group.accounts:
                                with st.expander(
                                    f"Account - {account.account_identifier.account_number}", expanded=expand_all
                                ):
                                    add_new_lines(1)
                                    with st.expander(f"Header - {account.account_identifier.account_number}"):
                                        st.write(account.account_identifier.model_dump())
                                        dict_to_form(account.account_identifier.model_dump(), gap="large", width=800)
                                    add_new_lines(1)
                                    st.write("Transactions:<br>", unsafe_allow_html=True)
                                    for txn_cntr, transaction in enumerate(account.transactions, 1):
                                        with st.expander(
                                            f"Transaction - {transaction.transaction.record_counter} "
                                            f"| Amount: {transaction.transaction.amount} "
                                            f"| Reference Num: {transaction.transaction.bank_reference_number}",
                                            expanded=True if txn_cntr == 1 or expand_all else False,
                                        ):
                                            dict_to_form(transaction.transaction.model_dump(), gap="large", width=800)
                                            st.text("SUMMARY")
                                            st.code(
                                                "\n".join(txn.record for txn in transaction.summary),
                                                # key=f"txn_{transaction.transaction.record_counter}",
                                                width=1000,
                                            )
                                    add_new_lines(1)
                                    with st.expander(f"Trailer - {account.account_identifier.account_number}"):
                                        st.write(account.account_trailer.model_dump())
                                    add_new_lines(1)
                        with st.expander("Group Trailer"):
                            st.write(group.group_trailer)
                with st.expander("File Trailer"):
                    st.write(st.session_state.uploaded_file_data.file_trailer)

else:
    st.write("Please upload a file to begin.")
