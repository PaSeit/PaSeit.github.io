import streamlit as st
import os
import json

# Paths
ITEMS_JSON_PATH = r'items.json'
IMAGES_DIR = r'images'
ITEMS_DIR = r'Items'

# Ensure the directories exist
for directory in [IMAGES_DIR, ITEMS_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Load existing items from the JSON file
if os.path.exists(ITEMS_JSON_PATH):
    with open(ITEMS_JSON_PATH, 'r') as f:
        items = json.load(f)
else:
    items = []

def save_items():
    with open(ITEMS_JSON_PATH, 'w') as f:
        json.dump(items, f, indent=4)

def add_item(title, image_path, description, category, yaml_file, version, tags, simple_code):
    new_item = {
        'title': title,
        'image': image_path,
        'description': description,
        'yamlFile': yaml_file,
        'category': category,
        'version': version,
        'tags': tags,
        'simpleCode': simple_code
    }
    items.append(new_item)
    save_items()

def update_item(index, title, image_path, description, category, yaml_file, version, tags, simple_code):
    items[index] = {
        'title': title,
        'image': image_path,
        'description': description,
        'yamlFile': yaml_file,
        'category': category,
        'version': version,
        'tags': tags,
        'simpleCode': simple_code
    }
    save_items()

def delete_item(index):
    del items[index]
    save_items()

st.title('Create or Edit Item')

selected_index = st.selectbox('Select Item to Edit (or create new)', [-1] + list(range(len(items))), format_func=lambda x: "Create New Item" if x == -1 else items[x]['title'])

categories = ['Examples', 'Buttons', 'Labels', 'Galleries', 'More', 'Components', 'Functions', 'SVGs', 'Theme']

# Gather all existing versions and tags
existing_versions = list(set(item['version'] for item in items))
existing_tags = list(set(tag for item in items for tag in item.get('tags', [])))
yaml_files = ['None'] + [f for f in os.listdir(ITEMS_DIR) if f.endswith('.yml')]

if selected_index == -1:
    title = st.text_input('Title')
    image_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg', 'svg'])
    description = st.text_input('Description', 'Color adjusts with theme' if 'Icon' in title else '')
    category = st.selectbox('Category', categories)
    yaml_file = st.selectbox('YAML File', yaml_files)
    version = st.selectbox('Version', existing_versions + ['Add new version'])
    if version == 'Add new version':
        version = st.text_input('New Version')
    tags = st.multiselect('Tags', options=existing_tags + ['Add new tag'])
    if 'Add new tag' in tags:
        new_tag = st.text_input('New Tag')
        if new_tag:
            tags.append(new_tag)
    simple_code = st.text_area('Simple Code')
else:
    item = items[selected_index]
    title = st.text_input('Title', item['title'])
    description = st.text_input('Description', item['description'])
    category = st.selectbox('Category', categories, index=categories.index(item['category']))
    
    # Handle None case for yamlFile
    yaml_file_index = yaml_files.index(os.path.basename(item['yamlFile'])) if item['yamlFile'] and os.path.basename(item['yamlFile']) in yaml_files else 0
    yaml_file = st.selectbox('YAML File', yaml_files, index=yaml_file_index)
    
    version = st.selectbox('Version', existing_versions + ['Add new version'], index=existing_versions.index(item.get('version', '')) if item.get('version', '') in existing_versions else -1)
    if version == 'Add new version':
        version = st.text_input('New Version')
    tags = st.multiselect('Tags', options=existing_tags + ['Add new tag'], default=item.get('tags', []))
    if 'Add new tag' in tags:
        new_tag = st.text_input('New Tag')
        if new_tag:
            tags.append(new_tag)
    simple_code = st.text_area('Simple Code', item.get('simpleCode', ''))
    image_path = item['image']
    
    # Display image or SVG
    if image_path.endswith('.svg'):
        st.image(image_path, use_column_width=True, output_format='svg')
    else:
        st.image(image_path, use_column_width=True)
    
    image_file = st.file_uploader('Choose an image...', type=['png', 'jpg', 'jpeg', 'svg'])

if st.button('Save Item'):
    if title and description and category and version and tags:
        tags_list = [tag for tag in tags if tag != 'Add new tag']
        yaml_file_path = None if yaml_file == 'None' else os.path.join(ITEMS_DIR, yaml_file)
        if image_file:
            image_path = os.path.join(IMAGES_DIR, image_file.name)
            with open(image_path, 'wb') as f:
                f.write(image_file.getbuffer())
        if selected_index == -1:
            add_item(title, image_path, description, category, yaml_file_path, version, tags_list, simple_code)
            st.success('Item added successfully')
        else:
            update_item(selected_index, title, image_path, description, category, yaml_file_path, version, tags_list, simple_code)
            st.success('Item updated successfully')
    else:
        st.error('Please fill in all fields')

if selected_index != -1 and st.button('Delete Item'):
    delete_item(selected_index)
    st.success('Item deleted successfully')
    st.experimental_set_query_params()  # Refresh the page
