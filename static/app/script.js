const API_BASE = "/api";
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function loadConversations() {
    try {
        let response = await fetch(`${API_BASE}/conversations/`);
        let data = await response.json();
        console.log("DATA", data)

        let list = document.getElementById("conversation-list");
        list.innerHTML = "";
        
        data.forEach(conv => {
            let item = document.createElement("a");
            item.href = `/conversation/?id=${conv.id}`;
            item.className = "list-group-item list-group-item-action";

            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <strong>${conv.id}</strong>
                    <span class="badge bg-${conv.state === "OPEN" ? "success" : "secondary"}">
                        ${conv.state}
                    </span>
                </div>
            `;

            list.appendChild(item);
        });

    } catch (error) {
        console.error("Erro ao carregar conversas", error);
    }
}


async function loadConversationDetails() {
    let params = new URLSearchParams(window.location.search);
    let convId = params.get("id");

        console.log("ÀSI CHEGOU AQUI")
    let response = await fetch(`${API_BASE}/conversation/${convId}/`);
    let data = await response.json();
    console.log(data)

    let container = document.getElementById("messages");
    container.innerHTML = "";

    

    data.messages.forEach(msg => {
        let div = document.createElement("div");
        div.className = `alert message ${msg.direction}`;
        console.log("MSG", msg.timestamp)
        div.innerHTML = `
            <div>${msg.content}</div>
            <small class="text-muted">${new Date(msg.timestamp).toLocaleString()}</small>
        `;

        container.appendChild(div);
    });


    
    document.getElementById("close-btn").onclick = () => closeConversation(convId);
    if(data.state === "CLOSED"){
        let closeBtn = document.getElementById("close-btn");
        closeBtn.style.display = "none";
    }
}


async function closeConversation(id) {
    const csrfToken = getCookie('csrftoken');
    await fetch(`${API_BASE}/webhook/`, {
        method: "POST",
        headers: {"Content-Type": "application/json", "X-CSRFToken": csrfToken},
        body: JSON.stringify({
            type: "CLOSE_CONVERSATION",
            data: { id }
        })
    });

    alert("Conversa fechada!");
    window.location.reload();
}
