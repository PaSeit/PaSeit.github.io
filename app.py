import streamlit as st
import os
import json
from PIL import Image

# Path to the JSON file
ITEMS_JSON_PATH = r'items.json'
IMAGES_DIR = r'images'

# Ensure the images directory exists
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

# Load existing items from the JSON file
if os.path.exists(ITEMS_JSON_PATH):
    with open(ITEMS_JSON_PATH, 'r') as f:
        items = json.load(f)
else:
    items = []

def save_items():
    with open(ITEMS_JSON_PATH, 'w') as f:
        json.dump(items, f, indent=4)

def add_item(title, image_path, description, category, yaml_code):
    new_item = {
        'title': title,
        'image': image_path,
        'description': description,
        'yamlCode': yaml_code,
        'category': category
    }
    items.append(new_item)
    save_items()

def update_item(index, title, image_path, description, category, yaml_code):
    items[index] = {
        'title': title,
        'image': image_path,
        'description': description,
        'yamlCode': yaml_code,
        'category': category
    }
    save_items()

def delete_item(index):
    del items[index]
    save_items()

st.title('Create or Edit Item')

selected_index = st.selectbox('Select Item to Edit (or create new)', [-1] + list(range(len(items))), format_func=lambda x: "Create New Item" if x == -1 else items[x]['title'])

if selected_index == -1:
    title = st.text_input('Title')
    image_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg'])
    description = st.text_input('Description')
    category = st.selectbox('Category', ['Examples', 'Buttons', 'Labels', 'Galleries', 'More', 'Components', 'Functions', 'SVGs'])
    yaml_code = st.text_input('YAML Code')
else:
    item = items[selected_index]
    title = st.text_input('Title', item['title'])
    description = st.text_input('Description', item['description'])
    category = st.selectbox('Category', ['Examples', 'Buttons', 'Labels', 'Galleries', 'More', 'Components', 'Functions', 'SVGs'], index=['Examples', 'Buttons', 'Labels', 'Galleries', 'More', 'Components', 'Functions', 'SVGs'].index(item['category']))
    yaml_code = st.text_input('YAML Code', item['yamlCode'])
    image_path = item['image']
    st.image(image_path, use_column_width=True)
    image_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg'])

if st.button('Save Item'):
    if title and description and category and yaml_code:
        if image_file:
            image_path = os.path.join(IMAGES_DIR, image_file.name)
            with open(image_path, 'wb') as f:
                f.write(image_file.getbuffer())
        if selected_index == -1:
            add_item(title, image_path, description, category, yaml_code)
            st.success('Item added successfully')
        else:
            update_item(selected_index, title, image_path, description, category, yaml_code)
            st.success('Item updated successfully')
    else:
        st.error('Please fill in all fields')

if selected_index != -1 and st.button('Delete Item'):
    delete_item(selected_index)
    st.success('Item deleted successfully')
    st.experimental_set_query_params()  # Refresh the page
