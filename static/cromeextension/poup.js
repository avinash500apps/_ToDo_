

// const API_URLS = "http://127.0.0.1:8000";
// const API_URL = "http://127.0.0.1:8000"

// document.addEventListener("DOMContentLoaded", function () {
//     fetchCategories();
//     document.getElementById("datee").value = new Date().toISOString().split('T')[0]
// })

// document.getElementById("submitBtn").addEventListener('click', submitData);


// async function submitData() {
//     console.log("Submitting Task...");
//     const date = document.getElementById("datee").value;
//     const startTime = document.getElementById("start_time").value;
//     const endTime = document.getElementById("end_time").value;
//     const category = document.getElementById("category").value;
//     const taskName = document.getElementById("task_name").value;
//     const notes = document.getElementById("notes").value;

//     console.log("WWWWWWWWWWWw", date)
//     if (!date || !startTime || !endTime || !category || !taskName || !notes) {
//         alert("Please fill out all fields.");
//         return;
//     }

//     const payload = {
//         date: new Date(date).toISOString(),
//         start_time: startTime,
//         end_time: endTime,
//         category: category,
//         task_name: taskName,
//         notes: notes
//     };
//     console.log("payload", payload)

//     try {
//         const response = await fetch(`${API_URLS}/create-document/categories`, {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             body: JSON.stringify(payload)
//         });

//         const data = await response.json();
//         if (response.ok) {
//             alert("Task Created Successfully!");
//             fetchCategories();
//             resetData();

//             // Request updated tasks from background.js
//             chrome.runtime.sendMessage({ action: "fetchTasks" }, (response) => {
//                 console.log("🔄 Updated tasks requested after new task submission", response);
//             });
//         } else {
//             alert("Error: " + data.detail);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//         alert("Failed to create task.");
//     }

//     addCategoryBtn.addEventListener("click", async () => {
//         const categoryName = categoryInput.value.trim();
//         if (categoryName) {
//             await addCategory(categoryName);
//             categoryInput.value = ""; // Clear input after adding
//         }
//     })

//     fetchCategories();
// }

// document.getElementById("resetBtn").addEventListener("click", resetData);

// function resetData() {
//     document.getElementById("datee").value = new Date().toISOString().split('T')[0];
//     document.getElementById("start_time").value = "";
//     document.getElementById("end_time").value = "";
//     document.getElementById("category").value = "";
//     document.getElementById("task_name").value = "";
//     document.getElementById("notes").value = "";
//     fetchCategories();
// }

// function fetchCategories() {
//     fetch(`${API_URLS}/tasks/`)
//         .then(response => response.json())
//         .then(data => {
//             console.log("Fetched categories:", data);
//             const categoryList = document.getElementById("categoryList");
//             categoryList.innerHTML = ''; // Clear previous options

//             data.data.forEach(task => {
//                 if (task.name) {
//                     const option = document.createElement("option");
//                     option.value = task.name;
//                     categoryList.appendChild(option);
//                 }
//             });
//         })
//         .catch(error => {
//             console.error("Error fetching categories:", error);
//         });
// }



const API_URL = "http://127.0.0.1:8000";

document.addEventListener("DOMContentLoaded", function () {
    fetchCategories();
    document.getElementById("datee").value = new Date().toISOString().split('T')[0];
});

document.getElementById("submitBtn").addEventListener("click", submitData);
document.getElementById("resetBtn").addEventListener("click", resetData);
document.getElementById("addCategoryBtn").addEventListener("click", async () => {
    const categoryInput = document.getElementById("category");
    const categoryName = categoryInput.value.trim();
    if (categoryName) {
        await addCategory(categoryName);
        categoryInput.value = ""; // Clear input after adding
    }
});

// Function to submit task
async function submitData() {
    console.log("Submitting Task...");
    const date = document.getElementById("datee").value;
    const startTime = document.getElementById("start_time").value;
    const endTime = document.getElementById("end_time").value;
    const category = document.getElementById("category").value;
    const taskName = document.getElementById("task_name").value;
    const notes = document.getElementById("notes").value;

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

    console.log("Payload:", payload);

    try {
        const response = await fetch(`${API_URL}/tasks/`, {
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

// Function to reset input fields
function resetData() {
    document.getElementById("datee").value = new Date().toISOString().split('T')[0];
    document.getElementById("start_time").value = "";
    document.getElementById("end_time").value = "";
    document.getElementById("category").value = "";
    document.getElementById("task_name").value = "";
    document.getElementById("notes").value = "";
    fetchCategories();
}

// Function to fetch and populate categories
function fetchCategories() {
    fetch(`${API_URL}/categories/`)
        .then(response => response.json())
        .then(data => {
            console.log("Fetched categories:", data);
            const categoryList = document.getElementById("categoryList");
            categoryList.innerHTML = ""; // Clear previous options

            data.forEach(category => {
                if (category.name) {
                    const option = document.createElement("option");
                    option.value = category.name;
                    categoryList.appendChild(option);
                }
            });
        })
        .catch(error => {
            console.error("Error fetching categories:", error);
        });
}

// Function to add a new category
async function addCategory(categoryName) {
    try {
        const response = await fetch(`${API_URL}/categories/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: categoryName }),
        });

        if (!response.ok) throw new Error("Failed to add category");

        fetchCategories(); // Refresh category list after adding
    } catch (error) {
        console.error("Error adding category:", error);
    }
}



