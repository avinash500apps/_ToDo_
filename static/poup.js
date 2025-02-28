const API_URLS = "http://127.0.0.1:8000";
const API_URL = "http://127.0.0.1:8000"

document.addEventListener("DOMContentLoaded", function () {
    fetchCategories();
    document.getElementById("datee").value = new Date().toISOString().split('T')[0]
})

document.getElementById("submitBtn").addEventListener('click', submitData);


async function submitData() {
    console.log("Submitting Task...");
    const date = document.getElementById("datee").value;
    const startTime = document.getElementById("start_time").value;
    const endTime = document.getElementById("end_time").value;
    const category = document.getElementById("category").value;
    const taskName = document.getElementById("task_name").value;
    const notes = document.getElementById("notes").value;

    console.log("WWWWWWWWWWWw", date)
    if (!date || !startTime || !endTime || !category || !taskName || !notes) {
        alert("Please fill out all fields.");
        return;
    }



    const payload = {
        date: new Date(date).toISOString(),
        start_time: startTime,
        end_time: endTime,
        category: category,
        task_name: taskName,
        notes: notes
    };
    console.log("payload", payload)

    try {
        const response = await fetch(`${API_URLS}/create-document/categories`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await response.json();
        if (response.ok) {
            alert("Task Created Successfully!");
            fetchCategories();
            resetData();

            // Request updated tasks from background.js
            chrome.runtime.sendMessage({ action: "fetchTasks" }, (response) => {
                console.log("🔄 Updated tasks requested after new task submission", response);
            });
        } else {
            alert("Error: " + data.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Failed to create task.");
    }
}

document.getElementById("resetBtn").addEventListener("click", resetData);

function resetData() {
    document.getElementById("datee").value = new Date().toISOString().split('T')[0];
    document.getElementById("start_time").value = "";
    document.getElementById("end_time").value = "";
    document.getElementById("category").value = "";
    document.getElementById("task_name").value = "";
    document.getElementById("notes").value = "";
    fetchCategories();
}

function fetchCategories() {
    fetch(`${API_URLS}/tasks/`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched categories:", data);
            const categorySelect = document.getElementById('category');
            categorySelect.innerHTML = '';

            data.data.forEach(task => {
                if (task.name) {
                    const option = document.createElement('option');
                    option.value = task.name;
                    option.textContent = task.name;
                    categorySelect.appendChild(option);
                }
            });
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
        });
}

// function fetchCategories() {
//     fetch(`${API_URL}/tasks/`)
//         .then(response => response.json())
//         .then(data => {
//             console.log("Fetched categories:", data);
//             const categoryList = document.getElementById('categoryList');
//             categoryList.innerHTML = ''; // Clear previous options

//             data.data.forEach(task => {
//                 if (task.name) {
//                     const option = document.createElement('option');
//                     option.value = task.name;
//                     categoryList.appendChild(option);
//                 }
//             });
//         })
//         .catch(error => {
//             console.error('Error fetching categories:', error);
//         });
// }

// // Load categories on page load
// fetchCategories();

// document.getElementById("addCategoryBtn").addEventListener("click", createCategory)


// async function createCategory() {
//     try {
//         const response = await fetch(`${API_URL}/create-document/tasks`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(payload),
//         });

//         if (response.ok) {
//             inputField.value = "";
//              fetchCategories()
//              console.log("categorySelect",document.getElementById('category'))
//         } else {
//             alert("Error creating list");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         alert("An error occurred while creating the list");
//     }
// }

// document.getElementById("addCategoryBtn").addEventListener("click", createCategory);

// async function createCategory() {
//     const categoryInput = document.getElementById("categoryInput").value.trim();

//     if (!categoryInput) {
//         alert("Please enter a category name");
//         return;
//     }

//     const payload = { name: categoryInput };

//     try {
//         const response = await fetch(`${API_URL}/create-document/tasks`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(payload),
//         });

//         if (response.ok) {
//             document.getElementById("categoryInput").value = "";
//             fetchCategories(); // Refresh category list
//         } else {
//             alert("Error creating category");
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         alert("An error occurred while creating the category");
//     }
// }