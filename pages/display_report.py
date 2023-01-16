import streamlit as st
import os

if os.path.exists("report.md"):
    with open("report.md", "r") as f:
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
