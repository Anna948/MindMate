MindMate - Mental Health Companion 🌟
A supportive AI-powered mental health chatbot built with Streamlit and Groq API.
Features

💬 Empathetic AI conversations
🎭 Mood detection and tracking
📊 Mood journey analytics
🌬️ Breathing exercises
💡 Personalized tips based on mood
🆘 Crisis helpline information

Setup Instructions
1. Get Groq API Key

Go to console.groq.com
Sign up for a free account
Navigate to API Keys section
Create a new API key
Copy the key (starts with gsk_)

2. Install Dependencies
bashpip install -r requirements.txt
3. Configure API Key
Create a file .streamlit/secrets.toml in your project directory:
tomlGROQ_API_KEY = "gsk_your_api_key_here"
Replace gsk_your_api_key_here with your actual Groq API key.
4. Run the App
bashstreamlit run app.py
The app will open in your browser at http://localhost:8502
Project Structure
MindMate/
├── app.py                      # Main application file
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── secrets.toml           # API key configuration (don't commit!)
└── README.md                  # This file
Usage

Open the app in your browser
Type your message in the chat input
MindMate will respond with supportive messages
View your mood tracking on the right panel
Check the sidebar for mood journey analytics
Use breathing exercises when needed

Technologies Used

Streamlit - Web framework
Groq - Fast AI inference (Llama 3.3 70B)
Python - Backend logic

Important Notes

This is a supportive tool, NOT a replacement for professional mental health care
In crisis situations, please contact emergency services or helplines
All conversations are private and not stored permanently

Helplines
India

AASRA: 91-22-27546669
iCall: 9152987821

Global

https://www.befrienders.org

License
MIT License - Feel free to use and modify for your projects!
Contributing
Contributions are welcome! Feel free to submit issues or pull requests.