from flask import Flask, render_template # Import Flask and render_template for web application
from flask_socketio import SocketIO # Import SocketIO for real-time communication 
import cv2 # Import OpenCV for video processing
import base64 # Import base64 for image encoding
import numpy as np # Import numpy for array manipulation
import threading # Import threading for running Flask app in a separate thread
import customtkinter as ctk # Import customtkinter for a sleek, high-tech look
from PIL import Image, ImageTk # Import ImageTk for Tkinter image handling
from pyngrok import ngrok  # Import ngrok for public URL management

ngrok_auth_token = input("Enter your ngrok API key: ")

# Set your ngrok API key
ngrok.set_auth_token(ngrok_auth_token)  # Replace with your actual ngrok API key

# Flask app and socket initialization
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize the customtkinter GUI
ctk.set_appearance_mode("dark")  # Dark mode for a sleek, high-tech look
ctk.set_default_color_theme("blue")  # High-tech blue theme

# Root window setup
root = ctk.CTk()
root.title("Mjonir")
root.geometry("900x650")
root.resizable(False, False)

# Main Frame with high-tech styling for video display
frame = ctk.CTkFrame(root, width=860, height=520, corner_radius=15, fg_color="#101826")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title Label with neon-inspired colors and font size adjustments
title_label = ctk.CTkLabel(root, text="Mjonir: Let's hack it!", 
                           font=ctk.CTkFont(size=26, weight="bold"), 
                           text_color="#1e90ff")  # Neon blue color for futuristic effect
title_label.pack(pady=20)

# Video display label with rounded corners
label = ctk.CTkLabel(frame, text="", width=860, height=520, 
                     fg_color="black", corner_radius=15)
label.pack()

# Status bar with futuristic styling, no unsupported arguments
status_bar = ctk.CTkLabel(root, text="Status: Waiting for video stream...", 
                          font=ctk.CTkFont(size=16, weight="normal"), 
                          text_color="#00ff00", fg_color="#101826", 
                          height=35)
status_bar.pack(side="bottom", fill="x")

# Function to update frame in Tkinter
def update_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    image_tk = ImageTk.PhotoImage(image)
    label.image = image_tk
    label.configure(image=image_tk)
    status_bar.configure(text="Status: Streaming video...", text_color="#00ff00")

# Flask route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Function to handle video stream through socket.io
@socketio.on('video_stream', namespace='/stream')
def handle_video_stream(data):
    try:
        # Decode the image data directly in JPEG format for faster processing
        encoded_data = data.split(',')[1] if ',' in data else data
        decoded_data = base64.b64decode(encoded_data)
        
        # Convert JPEG byte data to an image array
        nparr = np.frombuffer(decoded_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Only update the frame if it is valid
        if frame is not None and frame.size > 0:
            root.after(0, update_frame, frame)  # Process frame in Tkinter
        else:
            print("Invalid frame received: Frame could not be decoded or is empty")

    except Exception as e:
        print(f"Error processing video stream: {e}")

# Flask route, Tkinter setup, and threading remain the same as before

# Function to start ngrok and retrieve the public URL
def get_public_url():
    # Open a tunnel on port 5000 for Flask (ensure it matches the port Flask is running on)
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")
    return public_url

# Run Flask app in a separate thread with ngrok
def run_flask_app():
    # Start the ngrok tunnel
    public_url = get_public_url()
    
    # Print the ngrok URL to the Tkinter status bar
    status_bar.configure(text=f"Access the stream here: {public_url}", text_color="#00ff00")
    
    # Run the Flask-SocketIO app
    socketio.run(app, debug=True, use_reloader=False)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    root.mainloop()
