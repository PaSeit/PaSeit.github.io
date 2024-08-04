let galleryData = [];

function toggleSubcategories(element) {
    const subcategories = element.nextElementSibling;
    const chevron = element.querySelector('.fa-chevron-down, .fa-chevron-up');
    if (subcategories && subcategories.classList.contains('subcategories')) {
        element.classList.toggle('open');
        if (subcategories.style.display === 'block') {
            subcategories.style.display = 'none';
            chevron.classList.remove('fa-chevron-up');
            chevron.classList.add('fa-chevron-down');
        } else {
            subcategories.style.display = 'block';
            chevron.classList.remove('fa-chevron-down');
            chevron.classList.add('fa-chevron-up');
        }
    }
}

async function copyToClipboard(yamlFile, element, isYAML = false) {
    try {
        const response = await fetch(yamlFile);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const content = await response.text();

        const tempTextarea = document.createElement("textarea");
        tempTextarea.value = content;
        document.body.appendChild(tempTextarea);
        tempTextarea.select();
        document.execCommand("copy");
        document.body.removeChild(tempTextarea);

        // Add the copied class to trigger the animation
        element.classList.add("copied");
        setTimeout(() => {
            element.classList.remove("copied");
        }, 1000); // Remove class after animation is complete
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

function applyFilters() {
    const versionFilter = document.getElementById("versionFilter").value;
    const tagFilter = document.getElementById("tagFilter").value;
    const searchInput = document.getElementById("searchInput").value;
    const activeCategory = document.querySelector('.category.active')?.textContent.trim() || 'All';
    loadGallery(activeCategory, searchInput, versionFilter, tagFilter);
}

function loadGallery(category = '', searchQuery = '', versionFilter = '', tagFilter = '') {
    const gallery = document.getElementById("gallery");
    const noItemsMessage = document.getElementById("noItemsMessage");
    gallery.innerHTML = "";
    const filteredItems = galleryData
        .filter(item => (category === 'All' || category === '' || item.category === category) &&
                        (searchQuery === '' || item.title.toLowerCase().includes(searchQuery.toLowerCase())) &&
                        (versionFilter === '' || item.version === versionFilter) &&
                        (tagFilter === '' || item.tags.includes(tagFilter)));
    
    if (filteredItems.length === 0) {
        noItemsMessage.style.display = "block";
    } else {
        noItemsMessage.style.display = "none";
    }

    filteredItems.forEach(item => {
        const galleryItem = document.createElement("div");
        galleryItem.className = "gallery-item";
        
        const img = document.createElement("img");
        img.src = item.image;
        img.alt = item.title;
        
        const galleryItemContent = document.createElement("div");
        galleryItemContent.className = "gallery-item-content";
        
        const header = document.createElement("div");
        header.className = "gallery-item-header";
        
        const title = document.createElement("h3");
        title.textContent = item.title;

        const titleContainer = document.createElement("div");
        titleContainer.style.display = "flex";
        titleContainer.style.justifyContent = "space-between";
        titleContainer.style.alignItems = "center";
        titleContainer.appendChild(title);
        
        const tags = document.createElement("div");
        tags.className = "tags";
        item.tags.forEach(tag => {
            const tagElement = document.createElement("div");
            tagElement.className = "tag";
            tagElement.textContent = tag;
            tags.appendChild(tagElement);
        });
        
        header.appendChild(titleContainer);
        header.appendChild(tags);
        
        const description = document.createElement("p");
        description.textContent = item.description.length > 40 ? item.description.slice(0, 40) + '...' : item.description;
        
        const buttonContainer = document.createElement("div");
        buttonContainer.style.display = "flex";
        buttonContainer.style.justifyContent = "space-between";
        buttonContainer.style.alignItems = "center";
        
        const button = document.createElement("button");
        button.className = "copy-btn";
        button.textContent = "Copy";
        button.onclick = () => {
            const isYAML = item.tags.includes('YAML');
            copyToClipboard(isYAML ? item.yamlFile : item.codeFile, galleryItem, isYAML);
        };
        
        const version = document.createElement("span");
        version.className = "version";
        version.textContent = item.version;

        buttonContainer.appendChild(button);
        buttonContainer.appendChild(version);
        
        galleryItemContent.appendChild(header);
        galleryItemContent.appendChild(description);
        galleryItemContent.appendChild(buttonContainer);
        
        galleryItem.appendChild(img);
        galleryItem.appendChild(galleryItemContent);
        
        gallery.appendChild(galleryItem);
    });

    document.getElementById("galleryTitle").textContent = category || 'Gallery';
}

function filterGallery(category) {
    const categories = document.querySelectorAll('.category, .subcategories a');
    categories.forEach(cat => cat.classList.remove('active'));
    const activeCategory = [...categories].find(cat => cat.textContent.trim() === category || (category === "SVGs" && cat.textContent.trim() === "SVG's"));
    if (activeCategory) activeCategory.classList.add('active');
    const searchInput = document.getElementById("searchInput").value;
    const versionFilter = document.getElementById("versionFilter").value;
    const tagFilter = document.getElementById("tagFilter").value;
    loadGallery(category, searchInput, versionFilter, tagFilter);
}

document.getElementById("searchInput").addEventListener("input", applyFilters);

document.addEventListener("DOMContentLoaded", () => loadGallery('All'));

async function fetchGalleryData() {
    const response = await fetch('items.json');
    const data = await response.json();
    galleryData = data;
    return data;
}

document.addEventListener("DOMContentLoaded", async () => {
    await fetchGalleryData();
    filterGallery('All');
});
