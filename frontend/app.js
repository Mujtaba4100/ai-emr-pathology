const API_BASE = "http://127.0.0.1:8000/api";

// ============================================
// FILE UPLOAD
// ============================================

document.getElementById("upload-area").addEventListener("click", () => {
    document.getElementById("file-input").click();
});

document.getElementById("upload-area").addEventListener("dragover", (e) => {
    e.preventDefault();
    document.getElementById("upload-area").style.backgroundColor = "#e8f5e9";
});

document.getElementById("upload-area").addEventListener("dragleave", () => {
    document.getElementById("upload-area").style.backgroundColor = "#f9f9f9";
});

document.getElementById("upload-area").addEventListener("drop", (e) => {
    e.preventDefault();
    document.getElementById("upload-area").style.backgroundColor = "#f9f9f9";
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById("file-input").files = files;
    }
});

async function uploadFile() {
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];
    const statusDiv = document.getElementById("upload-status");

    if (!file) {
        statusDiv.innerHTML = '<span class="error">❌ Please select a file</span>';
        return;
    }

    statusDiv.innerHTML = '<span class="loading">⏳ Uploading...</span>';

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE}/upload/`, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status === "success") {
            statusDiv.innerHTML = `<span class="success">✅ File uploaded: ${data.filename}</span>`;
            fileInput.value = "";
        } else {
            statusDiv.innerHTML = `<span class="error">❌ Upload failed: ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error uploading file:", error);
        statusDiv.innerHTML = '<span class="error">❌ Error uploading file</span>';
    }
}

// ============================================
// SEMANTIC SEARCH
// ============================================

async function searchReports() {
    const query = document.getElementById("search-query").value;
    const statusDiv = document.getElementById("search-status");
    const resultsDiv = document.getElementById("results");

    if (!query) {
        statusDiv.innerHTML = '<span class="error">❌ Please enter search query</span>';
        return;
    }

    statusDiv.innerHTML = '<span class="loading">⏳ Searching...</span>';
    resultsDiv.innerHTML = "";

    try {
        const response = await fetch(`${API_BASE}/search/semantic`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query,
                top_k: 5
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            statusDiv.innerHTML = `<span class="success">✅ Found ${data.total_results} results</span>`;
            displayResults(data.results);
        } else {
            statusDiv.innerHTML = `<span class="error">❌ Search failed: ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error searching:", error);
        statusDiv.innerHTML = '<span class="error">❌ Error searching reports</span>';
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (results.length === 0) {
        resultsDiv.innerHTML = '<p style="grid-column: 1/-1;">No results found</p>';
        return;
    }

    results.forEach(result => {
        const resultDiv = document.createElement("div");
        resultDiv.className = "result-item";
        const similarity = (result.similarity_score * 100).toFixed(1);
        
        resultDiv.innerHTML = `
            <div class="result-header">
                <span class="test-type">${result.test_type || "Unknown"}</span>
                <span class="similarity-badge">${similarity}% match</span>
            </div>
            <div class="result-body">
                <p><strong>📋 Diagnosis:</strong> ${result.diagnosis || "Not specified"}</p>
                <p><strong>📄 Preview:</strong> ${result.text_preview || "No preview available"}</p>
                <p><strong>🆔 Document ID:</strong> ${result.document_id}</p>
            </div>
        `;
        resultsDiv.appendChild(resultDiv);
    });
}

// ============================================
// CHATBOT
// ============================================

let chatHistory = [];

async function askChatbot() {
    const question = document.getElementById("chat-question").value;
    const chatMessagesDiv = document.getElementById("chat-messages");

    if (!question) {
        alert("Please enter a question");
        return;
    }

    // Add user message to chat
    const userMsgDiv = document.createElement("div");
    userMsgDiv.className = "chat-message user-message";
    userMsgDiv.textContent = question;
    chatMessagesDiv.appendChild(userMsgDiv);

    // Add loading indicator
    const loadingDiv = document.createElement("div");
    loadingDiv.className = "chat-message bot-message loading";
    loadingDiv.textContent = "⏳ Thinking...";
    chatMessagesDiv.appendChild(loadingDiv);

    // Scroll to bottom
    chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

    try {
        const response = await fetch(`${API_BASE}/chat/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                conversation_history: chatHistory
            })
        });

        const data = await response.json();

        // Remove loading indicator
        chatMessagesDiv.removeChild(loadingDiv);

        // Add bot response
        const botMsgDiv = document.createElement("div");
        botMsgDiv.className = "chat-message bot-message";

        if (data.status === "success") {
            botMsgDiv.innerHTML = `
                <p>${data.answer}</p>
                <div class="sources">
                    <strong>📚 Sources:</strong> ${data.total_sources} documents
                </div>
            `;
        } else if (data.status === "no_results") {
            botMsgDiv.innerHTML = `<p>ℹ️ ${data.answer}</p>`;
        } else {
            botMsgDiv.innerHTML = `<p>❌ Error: ${data.message}</p>`;
        }

        chatMessagesDiv.appendChild(botMsgDiv);

        // Update chat history
        chatHistory.push({ role: "user", content: question });
        if (data.status === "success") {
            chatHistory.push({ role: "assistant", content: data.answer });
        }

        // Scroll to bottom
        chatMessagesDiv.scrollTop = chatMessagesDiv.scrollHeight;

        // Clear input
        document.getElementById("chat-question").value = "";
    } catch (error) {
        console.error("Error asking chatbot:", error);
        
        // Remove loading indicator
        if (chatMessagesDiv.contains(loadingDiv)) {
            chatMessagesDiv.removeChild(loadingDiv);
        }

        // Add error message
        const errorDiv = document.createElement("div");
        errorDiv.className = "chat-message bot-message";
        errorDiv.textContent = "❌ Error communicating with chatbot";
        chatMessagesDiv.appendChild(errorDiv);
    }
}

// ============================================
// KEYBOARD SHORTCUTS
// ============================================

document.getElementById("chat-question").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        askChatbot();
    }
});

document.getElementById("search-query").addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        searchReports();
    }
});

// ============================================
// PAGE LOAD
// ============================================

window.addEventListener("load", () => {
    console.log("✅ Frontend loaded successfully");
    console.log(`📡 API Base: ${API_BASE}`);
});
