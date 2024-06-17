function showLoading() {
    if (window.innerWidth > 768) {
        document.getElementById('loading-circle').style.display = 'block';
    }
}
function hideLoading() {
    document.getElementById('loading-circle').style.display = 'none';
}
function toggleSelection(element) {
    element.classList.toggle('selected');
    const checkbox = element.querySelector('input[type="checkbox"]');
    checkbox.checked = !checkbox.checked;
    var selectedTweaks = [];
    const tweakElements = document.querySelectorAll('.tweak.selected');
    tweakElements.forEach(tweak => {
        const labelElement = tweak.querySelector('.tweak-info .tweak-title');
        selectedTweaks.push("**" + tweak.dataset.category)
        selectedTweaks.push(labelElement.textContent);
    });
    selectedTweaks = [...new Set(selectedTweaks)];
    document.getElementById('selected-tweaks').innerHTML = ''; // Clear the container
    selectedTweaks.forEach(tweak => {
        const tweakItem = document.createElement('div');
        if (tweak.includes("**")) {
            // tweakItem.className = ("tweakListCategory")
            var label = document.createElement('label')
            tweak = tweak.substring(2)
            label.textContent = tweak
            label.className = 'tweak-list-category'
            tweakItem.append(label);
        }
        else {
            tweakItem.className='tweak-list-pack'
            tweakItem.textContent = tweak;
        }
        document.getElementById('selected-tweaks').appendChild(tweakItem);
    });
    console.log(selectedTweaks.length)
    if (selectedTweaks.length == 0) document.getElementById('selected-tweaks').style.display = "none"
    else document.getElementById('selected-tweaks').style.display = "block"
}

function toggleCategory(label) {
    const tweaksContainer = label.nextElementSibling;
    tweaksContainer.style.display = tweaksContainer.style.display != 'grid' ? 'grid' : 'none';
}

function downloadSelectedTweaks() {
    var packName = document.getElementById('fileNameInput').value;
    if (!packName) {
        packName = `BTRP-${String(Math.floor(Math.random() * 1000000)).padStart(6, "0")}`
    }
    packName = packName.replaceAll('/', '-')
        const selectedTweaks = [];
    const tweakElements = document.querySelectorAll('.tweak.selected');
    tweakElements.forEach(tweak => {
        selectedTweaks.push({
            category: tweak.dataset.category,
            name: tweak.dataset.name,
            index: parseInt(tweak.dataset.index)
        });
    });

    const tweaksByCategory = {
        "Aesthetic": [],
        "Colorful Slime": [],
        "Fixes and Consistency": [],
        "Fun": [],
        "HUD and GUI": [],
        "Lower and Sides": [],
        "Menu Panoramas": [],
        "More Zombies": [],
        "Parity": [],
        "Peace and Quiet": [],
        "Retro": [],
        "Terrain": [],
        "Unobtrusive": [],
        "Utility": [],
        "Variation": []
    };

    const indicesByCategory = {
        "Aesthetic": [],
        "Colorful Slime": [],
        "Fixes and Consistency": [],
        "Fun": [],
        "HUD and GUI": [],
        "Lower and Sides": [],
        "Menu Panoramas": [],
        "More Zombies": [],
        "Parity": [],
        "Peace and Quiet": [],
        "Retro": [],
        "Terrain": [],
        "Unobtrusive": [],
        "Utility": [],
        "Variation": []
    };

    selectedTweaks.forEach(tweak => {
        tweaksByCategory[tweak.category].push(tweak.name);
        indicesByCategory[tweak.category].push(tweak.index);
    });

    const jsonData = {
        "Aesthetic": {
            "packs": tweaksByCategory["Aesthetic"],
            "index": indicesByCategory["Aesthetic"]
        },
        "Colorful Slime": {
            "packs": tweaksByCategory["Colorful Slime"],
            "index": indicesByCategory["Colorful Slime"]
        },
        "Fixes and Consistency": {
            "packs": tweaksByCategory["Fixes and Consistency"],
            "index": indicesByCategory["Fixes and Consistency"]
        },
        "Fun": {
            "packs": tweaksByCategory["Fun"],
            "index": indicesByCategory["Fun"]
        },
        "HUD and GUI": {
            "packs": tweaksByCategory["HUD and GUI"],
            "index": indicesByCategory["HUD and GUI"]
        },
        "Lower and Sides": {
            "packs": tweaksByCategory["Lower and Sides"],
            "index": indicesByCategory["Lower and Sides"]
        },
        "Menu Panoramas": {
            "packs": tweaksByCategory["Menu Panoramas"],
            "index": indicesByCategory["Menu Panoramas"]
        },
        "More Zombies": {
            "packs": tweaksByCategory["More Zombies"],
            "index": indicesByCategory["More Zombies"]
        },
        "Parity": {
            "packs": tweaksByCategory["Parity"],
            "index": indicesByCategory["Parity"]
        },
        "Peace and Quiet": {
            "packs": tweaksByCategory["Peace and Quiet"],
            "index": indicesByCategory["Peace and Quiet"]
        },
        "Retro": {
            "packs": tweaksByCategory["Retro"],
            "index": indicesByCategory["Retro"]
        },
        "Terrain": {
            "packs": tweaksByCategory["Terrain"],
            "index": indicesByCategory["Terrain"]
        },
        "Unobtrusive": {
            "packs": tweaksByCategory["Unobtrusive"],
            "index": indicesByCategory["Unobtrusive"]
        },
        "Utility": {
            "packs": tweaksByCategory["Utility"],
            "index": indicesByCategory["Utility"]
        },
        "Variation": {
            "packs": tweaksByCategory["Variation"],
            "index": indicesByCategory["Variation"]
        },
        "raw": selectedTweaks.map(tweak => tweak.name)
    };
    fetchPack('https', jsonData, packName)
}
const serverip = '104.179.112.200';

function fetchPack(protocol, jsonData, packName) {
    showLoading();
    fetch(`${protocol}://${serverip}/exportResourcePack`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'packName': packName
        },
        body: JSON.stringify(jsonData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        hideLoading();
        return response.blob();
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `${packName}.mcpack`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        if (protocol === 'https') {
            console.error('HTTPS error, trying HTTP:', error);
            fetchPack('http', jsonData, packName); // Retry with HTTP
        } else {
            console.error('Error:', error);
        }
    });
}
