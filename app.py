import streamlit as st
from groq import Groq
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="MindMate - Your Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "MindMate - Your AI-powered mental health companion"
    }
)

# -------------------------------------------------
# LOAD API KEY (SERVER SIDE ONLY)
# -------------------------------------------------
API_KEY = st.secrets.get("GROQ_API_KEY")

if not API_KEY:
    st.error("API key not found. Please add GROQ_API_KEY to Streamlit secrets.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)

# -------------------------------------------------
# CUSTOM CSS - FIXED FOR DARK MODE
# -------------------------------------------------
st.markdown("""
<style>
/* Chat message styling */
.chat-message {
    padding: 1.2rem;
    border-radius: 15px;
    margin-bottom: 1rem;
    color: #262730;
}

.user-message {
    background-color: #e3f2fd;
    border-left: 5px solid #2196f3;
}

.bot-message {
    background-color: #f1f8e9;
    border-left: 5px solid #8bc34a;
}

/* Dark mode fixes */
[data-testid="stAppViewContainer"][data-theme="dark"] .chat-message {
    color: #262730 !important;
}

[data-testid="stAppViewContainer"][data-theme="dark"] .user-message {
    background-color: #1e3a5f !important;
    border-left: 5px solid #2196f3;
    color: #ffffff !important;
}

[data-testid="stAppViewContainer"][data-theme="dark"] .bot-message {
    background-color: #2d4a2e !important;
    border-left: 5px solid #8bc34a;
    color: #ffffff !important;
}

[data-testid="stAppViewContainer"][data-theme="dark"] .chat-message strong {
    color: #ffffff !important;
}

/* Ensure timestamp is visible */
.chat-message div[style*="color:gray"] {
    opacity: 0.7;
}

[data-testid="stAppViewContainer"][data-theme="dark"] .chat-message div[style*="color:gray"] {
    color: #cccccc !important;
    opacity: 0.8;
}

/* Fix emoji and text alignment */
div[style*="font-size:64px"] {
    line-height: 1.2;
}

div[style*="text-align:center"][style*="font-weight:bold"] {
    margin-top: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mood_history" not in st.session_state:
    st.session_state.mood_history = []

# -------------------------------------------------
# MOOD DETECTION
# -------------------------------------------------
def detect_mood(text):
    text = text.lower()
    positive = ["happy", "good", "great", "excited", "love", "wonderful", "amazing", "joy", "fantastic", "excellent"]
    negative = ["sad", "anxious", "stressed", "angry", "worried", "depressed", "upset", "tired", "lonely", "hurt"]

    pos = sum(word in text for word in positive)
    neg = sum(word in text for word in negative)

    if neg > pos:
        return "negative", -0.5
    elif pos > neg:
        return "positive", 0.5
    return "neutral", 0.0

# -------------------------------------------------
# AI RESPONSE WITH GROQ
# -------------------------------------------------
def generate_response(user_text, mood):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are MindMate, a kind and supportive mental health companion for students.

Rules:
- Be empathetic and calm
- Never diagnose or provide medical advice
- Keep responses short (2-3 sentences)
- Suggest gentle coping strategies when appropriate
- Be warm, supportive, and understanding
- Validate their feelings"""
                },
                {
                    "role": "user",
                    "content": f"I'm feeling {mood}. {user_text}"
                }
            ],
            temperature=0.7,
            max_tokens=150,
        )
        
        return completion.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"Error: {e}")
        if "rate_limit" in str(e).lower():
            return "I'm experiencing high demand right now. Please try again in a moment. 💙"
        else:
            return "I hear you. Remember, you're doing your best, and that's enough. Would you like to try our breathing exercise? 💙"

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("<h1 style='text-align:center'>🌟 MindMate - Your Mental Health Companion</h1>", unsafe_allow_html=True)

# -------------------------------------------------
# LAYOUT
# -------------------------------------------------
col1, col2 = st.columns([2, 1])

# =================================================
# LEFT: CHAT
# =================================================
with col1:
    st.markdown("### 💬 Chat with MindMate")

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='chat-message user-message'>
            <strong>You:</strong><br>{msg["text"]}
            <div style="font-size:12px;color:gray">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='chat-message bot-message'>
            <strong>🌟 MindMate:</strong><br>{msg["text"]}
            <div style="font-size:12px;color:gray">{msg["time"]}</div>
            </div>
            """, unsafe_allow_html=True)

    user_input = st.chat_input("Share what's on your mind...")

    if user_input:
        mood, score = detect_mood(user_input)

        st.session_state.messages.append({
            "role": "user",
            "text": user_input,
            "mood": mood,
            "time": datetime.now().strftime("%H:%M")
        })

        st.session_state.mood_history.append(score)

        with st.spinner("MindMate is thinking..."):
            reply = generate_response(user_input, mood)

        st.session_state.messages.append({
            "role": "assistant",
            "text": reply,
            "time": datetime.now().strftime("%H:%M")
        })

        st.rerun()

# =================================================
# RIGHT: MOOD PANEL
# =================================================
with col2:
    st.markdown("### 🎭 Current Mood")

    if st.session_state.messages:
        last_user_msg = next(
            msg for msg in reversed(st.session_state.messages) if msg["role"] == "user"
        )

        mood = last_user_msg["mood"]

        emoji_map = {
            "positive": "😊",
            "neutral": "😐",
            "negative": "😟"
        }

        mood_value = {
            "negative": 20,
            "neutral": 50,
            "positive": 80
        }[mood]

        st.markdown(f"<div style='font-size:64px;text-align:center'>{emoji_map[mood]}</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;font-weight:bold'>{mood.title()}</p>", unsafe_allow_html=True)

        st.slider("Mood Level", 0, 100, mood_value, disabled=True)

        # -------- QUICK TIP --------
        st.markdown("### 💡 Quick Tip")

        tips = {
            "negative": "🌬️ Try slow breathing for one minute",
            "neutral": "🧘 Take a short mindful pause",
            "positive": "💖 Share your happiness with someone"
        }

        st.info(tips[mood])

        # -------- BREATHING --------
        with st.expander("🌬️ Breathing Exercise"):
            st.markdown("""
**4–4–6 Breathing Technique**

• Inhale for **4 seconds**  
• Hold for **4 seconds**  
• Exhale for **6 seconds**  

Repeat **3–4 times** to help your body relax 💙
""")
    else:
        st.info("Start chatting to see your mood insights")

# =================================================
# SIDEBAR: MOOD JOURNEY
# =================================================
with st.sidebar:
    st.markdown("### 📊 Your Mood Journey")

    if st.session_state.mood_history:
        avg_mood = sum(st.session_state.mood_history) / len(st.session_state.mood_history)
        st.metric("Average Mood", f"{avg_mood:.2f}")

        if avg_mood < -0.2:
            st.caption("Overall mood: Low 😟")
        elif avg_mood > 0.2:
            st.caption("Overall mood: Positive 🙂")
        else:
            st.caption("Overall mood: Neutral 😐")
    else:
        st.metric("Average Mood", "0.00")
        st.caption("Overall mood: Neutral 😐")

    st.markdown("---")
    st.markdown("### ℹ️ About MindMate")
    st.markdown("""
    MindMate provides:
    - 🎭 Real-time mood detection
    - 🤖 Empathetic AI responses
    - 💡 Relaxation techniques
    - 📈 Mood tracking over time
    
    ⚠️ **Important:** This is an educational tool, not a replacement for professional mental health care.
    """)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.mood_history = []
        st.rerun()
    
    st.markdown("---")

# =================================================
# HELP SECTION
# =================================================
with st.expander("🆘 Need Immediate Help?"):
    st.markdown("""
    **If you're in crisis, please reach out immediately:**
    
    **India:**
    - 🇮🇳 AASRA: 91-22-27546669 (24/7)
    - 🇮🇳 Vandrevala Foundation: 1860-2662-345
    - 🇮🇳 iCall: 9152987821 (Mon-Sat, 8am-10pm)
    
    **International:**
    - 🇺🇸 USA: 988 (Suicide & Crisis Lifeline)
    - 🇬🇧 UK: 116 123 (Samaritans)
    - 🌍 Global: [befrienders.org](https://www.befrienders.org)
    
    **Remember:** Professional help is available 24/7. You're not alone. 💚
    """)