const chatbotToggler = document.querySelector(".chatbot-toggler");
const closeBtn = document.querySelector(".close-btn");
const chatbox = document.querySelector(".chatbox");
const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const baseUrl = "https://dan-toys-jnx3xap2yq-uc.a.run.app"
let thread_id = "";
let isRequestPending = false;
let userMessage = null; // Variable to store user's 
const inputInitHeight = chatInput.scrollHeight;

const createChatLi = (message, className) => {
    // Create a chat <li> element with passed message and className
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", `${className}`);
    let chatContent = `<p></p>`;
    chatLi.innerHTML = chatContent;
    chatLi.querySelector("p").textContent = message;
    return chatLi; // return chat <li> element
}
const get_message_response = (messageID, messageElement) => {
    const API_URL = `${baseUrl}/retrieve_message_responses`;
    fetch(`${API_URL}/${thread_id}/${messageID}`).then(res => res.json()).then(res => {
        showMessage(messageElement, res.content, false)
        isRequestPending = false
    }).catch(() => {
        isRequestPending = false
        showMessage(messageElement, "Something went wrong", false)
    })
}

const checkStatus = async (runId, messageId, messageElement) => {
    const API_URL = `${baseUrl}/check_status`;
    try {
        let res = await fetch(`${API_URL}/${thread_id}/${runId}`)
        if (res.ok) {
            res = await res.json()
            console.log(res)
            if (res.status == "completed") {
                get_message_response(messageId, messageElement)
            } else if (["queued", "in_progress", "cancelling"].includes(res.status)) {
                // run check status again
                await new Promise(res => setTimeout(res, 1000))
                checkStatus(runId, messageId, messageElement)
            } else if (["failed", "expired", "cancelled"].includes(res.status)) {
                // show error message
                showMessage(messageElement, data.error_message, true)
            }
        } else {
            showMessage(messageElement, "Something went wrong.", true)
        }
    } catch (error) {
        isRequestPending = false
        showMessage(messageElement, "Something went wrong.", true)
    }
}
const showMessage = (messageElement, message, isError) => {
    if (isError) {
        messageElement.classList.add("error");
        messageElement.textContent = "Oops! Something went wrong. Please try again.";
    } else {
        messageElement.textContent = message
    }
}
const generateNewThread = async () => {
    const API_URL = `${baseUrl}/create_thread`;
    try {
        const res = await fetch(API_URL);
        if (res.ok) {
            const data = await res.json(); // Make sure to await the json() call
            console.log(data);
            return data.thread_id; // Return the thread_id
        }
    } catch (err) {
        isRequestPending = false
        // alert("Thread cannot be created! Something went wrong.");
    }
};

const add_new_message = async (chatElement) => {
    if (!thread_id) {
        thread_id = await generateNewThread(); // Update thread_id
        if (!thread_id) {
            alert("Thread cannot be created! Something went wrong.")
            return;
        }
    }
    console.log(thread_id);
    const API_URL = `${baseUrl}/send_message`;
    const messageElement = chatElement.querySelector("p");

    // Define the properties and message for the API request
    const requestOptions = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query: userMessage,
            thread_id: thread_id
        })
    }

    // Send POST request to API, get response and set the reponse as paragraph text
    fetch(API_URL, requestOptions).then(res => res.json()).then(data => {
        console.log(data)
        checkStatus(data.run_id, data.message_id, messageElement)
    }).catch(() => {
        isRequestPending = false
        showMessage(messageElement, "Oops! Something went wrong. Please try again.", true)
    }).finally(() => chatbox.scrollTo(0, chatbox.scrollHeight));
}

const handleChat = () => {
    userMessage = chatInput.value.trim(); // Get user entered message and remove extra whitespace
    if (!userMessage) return;
    if (isRequestPending) return;
    isRequestPending = true
    // Clear the input textarea and set its height to default
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Append the user's message to the chatbox
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatbox.scrollTo(0, chatbox.scrollHeight);

    setTimeout(() => {
        // Display "Thinking..." message while waiting for the response
        const incomingChatLi = createChatLi("...", "incoming");
        chatbox.appendChild(incomingChatLi);
        chatbox.scrollTo(0, chatbox.scrollHeight);
        add_new_message(incomingChatLi);
    }, 600);
}

chatInput.addEventListener("input", () => {
    // Adjust the height of the input textarea based on its content
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If Enter key is pressed without Shift key and the window 
    // width is greater than 800px, handle the chat
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleChat();
    }
});

sendChatBtn.addEventListener("click", handleChat);

// hanlde sidebar toggle

const sidebarBtn = document.querySelector("#sidebar-btn");
sidebarBtn.addEventListener("click", () => {
    document.querySelector(".sidebar").classList.toggle("active");
})