let mediaRecorder;
let audioChunks = [];

const recordButton = document.getElementById("record");
const stopButton = document.getElementById("stop");
const playback = document.getElementById("playback");
const status = document.getElementById("status");
const uploadForm = document.getElementById("uploadForm");

recordButton.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  mediaRecorder.start();
  audioChunks = [];
  status.innerText = "🎙️ Recording...";
  mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
};

stopButton.onclick = () => {
  mediaRecorder.stop();
  mediaRecorder.onstop = () => {
    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
    const audioUrl = URL.createObjectURL(audioBlob);
    playback.src = audioUrl;
    status.innerText = "✅ Recording stopped. Ready to upload.";

    // save blob to form
    uploadForm.onsubmit = async (e) => {
      e.preventDefault();
      const formData = new FormData();
      formData.append("audio", audioBlob, "recording.wav");
      status.innerText = "⏳ Sending to server...";
      const response = await fetch("/predict", { method: "POST", body: formData });
      const result = await response.json();
      status.innerText = "🔮 Prediction: " + result.prediction;
    };
  };
};
