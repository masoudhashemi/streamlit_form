import os

import streamlit as st

# Set the page layout to wide
st.set_page_config(layout="wide", page_title="R&D Report Reader", page_icon="🧊")

col1, col2, _ = st.columns(3)

with col1:
    folder_name = st.selectbox(
        "Select a folder",
        [folder[8:].replace("_", " ") for folder in os.listdir("reports/") if folder.startswith("reports_")],
    )
if folder_name:
    folder_name = "reports_" + folder_name.replace(" ", "_")


if folder_name in os.listdir("reports/"):
    folder_name = f"reports/{folder_name}"
    if os.path.exists(f"{folder_name}/report.md"):
        with open(f"{folder_name}/report.md", "r") as f:
            lines = f.readlines()
        markdown_lines = []
        for i, line in enumerate(lines):
            if "![image]" in line:
                markdown = "".join(markdown_lines)
                st.markdown(markdown)
                image_path = line.split("(")[1].split(")")[0]
                st.image(image_path, width=300)
                markdown_lines = []
            else:
                markdown_lines.append(line)
        markdown = "".join(markdown_lines)
        st.markdown(markdown)
    else:
        st.warning("Markdown file not found.")
