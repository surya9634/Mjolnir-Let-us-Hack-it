const socket = io('/stream');

const startButton = document.getElementById('startButton');
const videoElement = document.getElementById('videoElement');

startButton.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.srcObject = stream;

        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');

        // Set a smaller resolution for faster processing
        canvas.width = 320;
        canvas.height = 240;

        // Stream frames more frequently for real-time feel
        setInterval(() => {
            context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
            
            // Convert frame to JPEG format to reduce data size
            const frameData = canvas.toDataURL('image/jpeg', 0.5); // Adjust quality as needed
            socket.emit('video_stream', frameData);
        }, 100); // Capture and send frame every 100 ms

    } catch (error) {
        console.error('Error accessing camera:', error);
    }
});