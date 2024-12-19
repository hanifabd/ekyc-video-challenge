// Access the elements
const videoElement = document.getElementById('video');
const challengeTextElement = document.querySelector('.challenge-text');
const statusTextElement = document.querySelector('.status-text');

// Define the interval in seconds (change this value as needed)
const frameInterval = 5; // Example: send frames every 5 seconds
const stateInterval = 3;

// List of possible challenge texts
const challenges = [
    "Left Eye Closed",
    "Right Eye Closed",
    "Face Forward",
    "Face Left",
    "Face Right",
    "Face Down",
    "Face Up",
    "Mouth Open"
];

// Function to randomize the challenge text
function randomizeChallengeText() {
    const randomIndex = Math.floor(Math.random() * challenges.length);
    const randomChallenge = challenges[randomIndex];
    challengeTextElement.textContent = `Challenge: ${randomChallenge}`;
}

// Function to update the status text and color
function updateStatusText(text) {
    statusTextElement.textContent = text;

    // Change color based on the text content
    if (text === "Success") {
        statusTextElement.style.color = 'green';
    } else if (text === "Detecting..."){
        statusTextElement.style.color = 'grey';
    } else {
        statusTextElement.style.color = 'red';
    }
}

// Access the camera and start streaming
async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;

        // Call a function to stream frames to an API
        streamFramesToAPI(stream);
    } catch (err) {
        console.error("Error accessing camera: ", err);
    }
}

// Function to capture frames and send them to an API
function streamFramesToAPI(stream) {
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');

    // Set the canvas size to match the video dimensions
    videoElement.onloadedmetadata = () => {
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
    };

    // Capture and send frames every N seconds (frameInterval in seconds)
    setInterval(() => {
        // Draw the current frame onto the canvas
        context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

        // Convert the frame to a data URL (you can send this as an image)
        const frameData = canvas.toDataURL('image/jpeg');

        // Send the frame to the API
        sendFrameToAPI(frameData);
    }, frameInterval * 1000); // Send frame every frameInterval seconds
}

// Function to send the frame to an API
function sendFrameToAPI(frameData) {
    // Get the challenge-text from the DOM
    const challengeText = document.querySelector('.challenge-text').innerText;
    const challengeTextWithoutPrefix = challengeText.split('Challenge: ')[1];
    const request_body = {
        image: frameData, // Send the image data as a base64-encoded string
        challengeText: challengeTextWithoutPrefix, // Add the challenge-text without the "Challenge: " prefix
    }
    console.log("Request:", request_body)

    fetch('http://localhost:8000/facepose-challenge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request_body),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);
        if (data.status == "Success") {
            updateStatusText(data.status);
            setTimeout(() => {
                randomizeChallengeText();  // Call the randomizeChallengeText if the status is "Success"
                updateStatusText("Detecting...");
            }, stateInterval * 1000); // stateInterval seconds delay
        } else {
            updateStatusText(data.status);
            setTimeout(() => {
                updateStatusText("Detecting...");
            }, stateInterval * 1000); // stateInterval seconds delay
        }
    })
    .catch(error => {
        console.error("Error sending frame:", error);
    });
}

// Start the camera when the page loads
randomizeChallengeText();
startCamera();