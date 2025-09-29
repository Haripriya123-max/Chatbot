from flask import Flask, request, jsonify

app = Flask(__name__)

# Simple AI logic
def chatbot_response(user_input):
    user_input = user_input.lower()
    if "hello" in user_input:
        return "Hi there! How can I help you?"
    elif "your name" in user_input:
        return "I am Azure Chatbot 🤖"
    elif "bye" in user_input:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I didn’t understand that. Try asking something else!"

# Home route with simple HTML embedded
@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Azure Chatbot</title>
        <style>
            body { font-family: Arial; text-align: center; margin-top: 50px; }
            input { padding: 10px; width: 300px; }
            button { padding: 10px; }
            #chatbox { margin-top: 20px; max-width: 500px; margin-left: auto;
                       margin-right: auto; text-align: left; }
            .user { color: blue; }
            .bot { color: green; }
        </style>
    </head>
    <body>
        <h1>Azure Chatbot 🤖</h1>
        <input type="text" id="user_input" placeholder="Type your message..." />
        <button onclick="sendMessage()">Send</button>
        <div id="chatbox"></div>
        <script>
            function sendMessage() {
                var msg = document.getElementById("user_input").value;
                if(msg.trim() === "") return;
                var chatbox = document.getElementById("chatbox");
                chatbox.innerHTML += "<p class='user'><b>You:</b> " + msg + "</p>";

                fetch("/get", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: "msg=" + encodeURIComponent(msg)
                })
                .then(response => response.json())
                .then(data => {
                    chatbox.innerHTML += "<p class='bot'><b>Bot:</b> " + data.reply + "</p>";
                    chatbox.scrollTop = chatbox.scrollHeight;
                });
                document.getElementById("user_input").value = "";
            }
        </script>
    </body>
    </html>
    """

# Endpoint for chatbot response
@app.route("/get", methods=["POST"])
def get_response():
    user_message = request.form["msg"]
    bot_reply = chatbot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
