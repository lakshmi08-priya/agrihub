// ---------------- Soil Upload ----------------
function handleSoilFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  const resultDiv = document.getElementById("soilResult");
  resultDiv.innerHTML = `<div class="uploading-msg soil-loading">⏳ Uploading and analyzing...</div>`;

  const formData = new FormData();
  formData.append("soilFile", file);

  fetch("http://localhost:5000/api/soil-analyze", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    resultDiv.innerHTML = `
      <div>
        <h3>🌱 Soil Analysis Result</h3>
        <p>💧 <b>Moisture:</b> ${data.moisture || "N/A"}</p>
        <p>⚗️ <b>pH Level:</b> ${data.ph || "N/A"}</p>
        <p>🌿 <b>Nutrients:</b> ${data.nutrients || "N/A"}</p>
      </div>
    `;
  })
  .catch(err => {
    console.error(err);
    resultDiv.innerHTML = `<div class="uploading-msg error-msg">❌ Error analyzing soil. Try again!</div>`;
  });
}

// ---------------- Plant Upload ----------------
function handlePlantFile(event) {
  const file = event.target.files[0];
  if (!file) return;

  const resultDiv = document.getElementById("plantResult");
  resultDiv.innerHTML = `<div class="uploading-msg plant-loading">⏳ Uploading and detecting disease...</div>`;

  const formData = new FormData();
  formData.append("plantFile", file);

  fetch("http://localhost:5000/api/plant-detect", {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    const confidenceColor = data.confidence && data.confidence > 80 ? "#f44336" : "#4CAF50";
    resultDiv.innerHTML = `
      <div>
        <h3>🌿 Plant Disease Detection</h3>
        <p>🦠 <b>Disease:</b> ${data.disease || "No disease detected"}</p>
        <p>📊 <b>Confidence:</b> ${data.confidence ? data.confidence + "%" : "N/A"}</p>
      </div>
    `;
    resultDiv.style.borderLeftColor = confidenceColor;
  })
  .catch(err => {
    console.error(err);
    resultDiv.innerHTML = `<div class="uploading-msg error-msg">❌ Error detecting plant disease. Try again!</div>`;
  });
}

// ---------------- Chat Box ----------------
function sendMessage() {
  const input = document.getElementById('userInput') || document.getElementById('chatMessageInput');
  const message = input.value.trim();
  if (!message) return;

  const chatBody = document.getElementById('chatBody') || document.getElementById('chatMessages');

  // Display user message
  const userMsg = document.createElement('div');
  userMsg.className = "chat-bubble user-bubble";
  userMsg.innerHTML = `👩‍🌾 <b>You:</b> ${message}`;
  chatBody.appendChild(userMsg);
  chatBody.scrollTop = chatBody.scrollHeight;

  // Show loading message for bot
  const botMsg = document.createElement('div');
  botMsg.className = "chat-bubble bot-bubble";
  botMsg.textContent = "🤖 AgriBot is typing...";
  chatBody.appendChild(botMsg);
  chatBody.scrollTop = chatBody.scrollHeight;

  input.value = "";

  // Send to backend
  fetch("http://localhost:5000/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(res => res.json())
  .then(data => {
    botMsg.innerHTML = `🤖 <b>AgriBot:</b> ${data.reply || "Sorry, no response received."}`;
    chatBody.scrollTop = chatBody.scrollHeight;
  })
  .catch(err => {
    console.error(err);
    botMsg.textContent = "❌ Error connecting to server.";
  });
}

// ---------------- Press Enter to send ----------------
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById('userInput') || document.getElementById('chatMessageInput');
  if (input) {
    input.addEventListener("keypress", e => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
      }
    });
  }
});

// ---------------- Camera support for uploads ----------------
function openCamera(type) {
  const input = document.createElement('input');
  input.type = 'file';
  input.accept = 'image/*';
  input.capture = 'environment';
  input.onchange = event => {
    const file = event.target.files[0];
    if (file) {
      if (type === 'soil') handleSoilFile({ target: { files: [file] } });
      else handlePlantFile({ target: { files: [file] } });
    }
  };
  input.click();
}

// ---------------- Upload Buttons ----------------
const soilBtn = document.getElementById('soilBtn');
if (soilBtn) {
  soilBtn.onclick = () => {
    const useCamera = confirm("📸 Use camera? Cancel to choose from gallery.");
    if (useCamera) openCamera('soil');
    else document.getElementById('soilUpload').click();
  };
}

const plantBtn = document.getElementById('plantBtn');
if (plantBtn) {
  plantBtn.onclick = () => {
    const useCamera = confirm("📸 Use camera? Cancel to choose from gallery.");
    if (useCamera) openCamera('plant');
    else document.getElementById('plantUpload').click();
  };
}
