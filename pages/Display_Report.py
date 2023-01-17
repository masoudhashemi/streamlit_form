import os

import streamlit as st

folder_name = st.selectbox(
    "Select a folder", [folder[8:].replace("_", " ") for folder in os.listdir() if folder.startswith("reports_")]
)
if folder_name:
    folder_name = "reports_" + folder_name.replace(" ", "_")

if folder_name in os.listdir():
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
