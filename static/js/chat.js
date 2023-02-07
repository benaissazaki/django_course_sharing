let url = window.location.pathname;
let user_id = url.split('/').pop();

let webSocketUrl = ''
if (!isNaN(user_id)) {
    webSocketUrl = `ws://${window.location.host}/chat/${user_id}`
} else {
    webSocketUrl = `ws://${window.location.host}/chat/0`
}

const socket = new WebSocket(webSocketUrl);

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    insertMessage(data);
};

socket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
};

function insertMessage(message) {
    const messages_list = document.getElementById('previous-messages-list');
    messages_list.insertAdjacentHTML('beforeend', `<li><b>${message.sender}:</b>${message.message}</li>`)
}

function sendMessage() {
    const message = document.getElementById("chat-message-input").value;
    socket.send(JSON.stringify({
        message: message
    }));
}
