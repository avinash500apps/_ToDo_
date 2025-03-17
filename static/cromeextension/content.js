

// Listen for messages from `background.js`
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    console.log("Message received in content.js:", message);

    if (message.action === "updateTaskTable") {
        console.log("🎯 Forwarding message to body.html");

        // Send message to the web page using `window.postMessage()`
        window.postMessage({ action: "updateTaskTable", tasks: message.tasks }, "*");

        sendResponse({ status: "success", forwarded: true });
    }
});
