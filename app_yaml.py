import csv
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
import yaml

with open("info.yaml", "r") as stream:
    try:
        yaml_data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

title = yaml_data["title"]
entries_data = [yaml_data[f"entry_{i}"] for i in range(1, len(yaml_data))]
for entry in entries_data:
    entry["checkbox_options"] = []
    radio_options = entry["options"]
    for option in radio_options:
        for key, value in option.items():
            entry["checkbox_options"].append(f"{key}: {value}")


checkboxes_textboxes = []
for entry in entries_data:
    checkboxes_textboxes.append(
        {
            "expander_label": entry["description"],
            "checkbox_label": entry["question"],
            "checkbox_options": entry["checkbox_options"],
            "textbox_labels": entry["sub_questions"],
            "image_label": "Upload images [Optional]",
            "caption_label": "Captoin of the image [Optional]",
        }
    )


def generate_df(chosen_options, text_inputs, images_name, captions):
    df = pd.DataFrame(columns=["Group", "Text Input", "Image", "Caption"])
    for i in range(len(chosen_options)):
        if images_name[i]:
            image_entry = images_name[i]
        else:
            image_entry = None
        df = pd.concat(
            [
                df,
                pd.DataFrame.from_records(
                    [
                        {
                            "Group": chosen_options[i],
                            "Text Input": text_inputs[i],
                            "Image": image_entry,
                            "Caption": captions[i],
                        }
                    ]
                ),
            ]
        )
    return df


# Create a template for the report
template = """
## Description: {group}

Question -- {question}

    Answer -- {answer}

### Detailed Questions: 
{text_input}
{image_template_text}
----------------
"""

image_template = """
### Relevant Image

![{caption}](images/{image})

*Figure*: {caption}
"""

report = """
# Report

"""


def md_report(df, checkboxes_textboxes, report, template, image_template):
    # Iterate over the rows of the DataFrame
    for i, row in df.iterrows():
        # Format the template with the values from the DataFrame
        if pd.isna(row["Image"]):
            image_template_text = ""
        else:
            image_template_text = image_template.format(image=row["Image"], caption=row["Caption"])

        text_input = ""
        for j, text_input_ in enumerate(row["Text Input"]):
            text_input += f"- {checkboxes_textboxes[i]['textbox_labels'][j]['question']}: {text_input_} \n \n"

        report += template.format(
            group=checkboxes_textboxes[i]["expander_label"],
            question=checkboxes_textboxes[i]["checkbox_label"],
            answer=row["Group"],
            text_input=text_input,
            image_template_text=image_template_text,
        )

    # Write the report to a file
    with open("report.md", "w") as f:
        f.write(report)


text_inputs = []
chosen_options = []
images = []
images_name = []
captions = []

# Set the page layout to wide
st.set_page_config(layout="wide")
# Add a page to the sidebar
page = st.sidebar.selectbox("Select a page", ["Form", "CSV Content"])

st.markdown(f"# {title}")

# Show the form page
if page == "Form":
    with st.spinner("Loading..."):

        # Read the data from the CSV file and store it in a DataFrame
        try:
            df = pd.read_csv("data.csv")
        except:
            df = pd.DataFrame(columns=["Group", "Text Input", "Image", "Caption"])

        for i in range(len(checkboxes_textboxes)):
            st.markdown("""---""")
            group = ""
            text_input = ""

            checkboxes_textbox = checkboxes_textboxes[i]

            # create a checkbox for each group
            expanded = st.expander(checkboxes_textbox["expander_label"], expanded=False)

            with expanded:
                col1, col2 = st.columns(2)
                with col1:
                    index = checkboxes_textbox["checkbox_options"].index(df.iloc[i]["Group"]) if len(df) > i else 0
                    group = st.radio(
                        checkboxes_textbox["checkbox_label"],
                        checkboxes_textbox["checkbox_options"],
                        key=f"group{i}",
                        index=index,
                        help=checkboxes_textbox["expander_label"],
                    )
                    chosen_options.append(group)
                with col2:
                    text_input_ = []
                    if group[0] == "A":
                        for j, textbox_label in enumerate(checkboxes_textbox["textbox_labels"]):
                            text_input = st.text_area(
                                textbox_label["question"],
                                key=f"text_input_{i}_{j}",
                                value=eval(df.iloc[i]["Text Input"])[j] if len(df) > i else "",
                                disabled=True,
                                help=textbox_label["help"],
                            )
                            text_input_.append("N/A")
                    else:
                        for j, textbox_label in enumerate(checkboxes_textbox["textbox_labels"]):
                            text_input = st.text_area(
                                textbox_label["question"],
                                key=f"text_input_{i}_{j}",
                                value=eval(df.iloc[i]["Text Input"])[j] if len(df) > i else "",
                                help=textbox_label["help"],
                            )
                            text_input_.append(text_input)
                    text_inputs.append(text_input_)

                    # Add the option to upload images
                    if group[0] != "A":
                        image = st.file_uploader(
                            checkboxes_textbox["image_label"],
                            type=["jpg", "jpeg", "png"],
                            accept_multiple_files=False,
                            key=f"image_upload_input_{i}",
                        )
                        images.append(image)
                        images_name.append(image.name if image else df["Image"][i] if len(df) > i else None)
                        caption = st.text_input(
                            checkboxes_textbox["caption_label"],
                            value=df.iloc[i]["Caption"] if len(df) > i else "",
                            key=f"image_caption_input_{i}",
                        )
                        captions.append(caption)
                    else:
                        images.append(None)
                        images_name.append(None)
                        captions.append("")

        st.markdown("""---""")

        # submit button to save the values of chosen checkbox and the text in the text inputs in csv
        if st.button("Save"):
            df = pd.DataFrame(columns=["Group", "Text Input", "Image", "Caption"])
            for i in range(len(checkboxes_textboxes)):
                if images_name[i]:
                    image_entry = images_name[i]
                else:
                    image_entry = None
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame.from_records(
                            [
                                {
                                    "Group": chosen_options[i],
                                    "Text Input": text_inputs[i],
                                    "Image": image_entry,
                                    "Caption": captions[i],
                                }
                            ]
                        ),
                    ]
                )

                if not pd.isna(images[i]):
                    # Save uploaded file to 'images' folder.
                    save_folder = "./images"
                    save_path = Path(save_folder, images[i].name)
                    Path(save_folder).mkdir(parents=True, exist_ok=True)
                    with open(save_path, mode="wb") as w:
                        try:
                            w.write(images[i].read())
                        # TODO: does not work for some reason
                        except TypeError:
                            pass
                    if save_path.exists():
                        st.success(f"File {save_folder} is successfully saved!")
            df.to_csv("data.csv", index=False)
            st.success("Data saved.")

        if st.button("Reset"):
            df = pd.DataFrame(columns=["Group", "Text Input", "Image", "Caption"])
            df.to_csv("data.csv", index=False)
            st.success("Data reset.")

        if st.button("Generate Report"):
            df = generate_df(chosen_options, text_inputs, images_name, captions)
            md_report(df, checkboxes_textboxes, report, template, image_template)
            st.success("Report successfully generated.")


# Show the CSV content page
if page == "CSV Content":
    csv_file = st.selectbox("Select a CSV file", ["data.csv"])
    if csv_file:
        # Read the selected CSV file and display its content
        df = pd.read_csv(csv_file)
        st.dataframe(df[[c for c in df.columns]])
