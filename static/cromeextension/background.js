const API_URLS = "http://127.0.0.1:8000";

chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension installed");
});

async function fetchTasks() {
    try {
        let response = await fetch(`${API_URLS}/categories/`);
        console.log("reponse---------->")
        let data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching tasks:", error);
        return null;
    }
}

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    if (message.action === "fetchTasks") {
        const taskResponse = await fetchTasks();
        console.log("Fetched tasks:", taskResponse);

        if (taskResponse && taskResponse.data && taskResponse.data.length > 0) {
            chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
                if (tabs.length > 0) {
                    chrome.tabs.sendMessage(tabs[0].id, {
                        action: "updateTaskTable",
                        tasks: taskResponse.data
                    });
                }
            });
        } else {
            console.warn("No tasks found or error fetching tasks");
        }

        sendResponse({ status: "success", tasks: taskResponse });
        return true;
    }
});
