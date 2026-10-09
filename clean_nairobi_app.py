import os
import json
from io import BytesIO
import streamlit as st
from google import genai
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text

# App Configuration
st.set_page_config(
    page_title="PyCode Bite - Learn Python", page_icon="🐍", layout="centered"
)

# Initialize Session States and Local Progress File
PROGRESS_FILE = "user_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"is_pro": False, "quiz_score": 0, "quiz_completed": False, "chapters_unlocked": 1, "student_name": "Dillan Mwadime"}

def save_progress(data):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(data, f)

if "user_data" not in st.session_state:
    st.session_state.user_data = load_progress()

# Sidebar Navigation Menu
st.sidebar.title("PyCode Bite Hub")
app_mode = st.sidebar.selectbox(
    "Navigation Menu",
    [
        "Home Dashboard",
        "Free Lessons",
        "Pro Lessons (Advanced)",
        "AI Teacher Assistant",
        "Certificate of Completion"
    ]
)

# 1. HOME DASHBOARD
if app_mode == "Home Dashboard":
    st.title("Welcome to PyCode Bite")
    st.write("Your pocket-sized interactive tutor to master Python programming, test your logic with quizzes, and build real development skills.")
    
    if st.session_state.user_data["is_pro"]:
        st.success("PRO TIER ACTIVE: All advanced automation modules and AI features are unlocked!")
    else:
        st.info("Free Tier Active. Upgrade to Pro for advanced modules and full AI access.")
        
    st.subheader("Learning Progress Overview")
    st.write(f"Latest Quiz Score")
    st.metric(label="Score", value=f"{st.session_state.user_data['quiz_score']}/3")
    
    progress_val = min(st.session_state.user_data['chapters_unlocked'] / 3.0, 1.0)
    st.write("Overall Curriculum Completion")
    st.progress(progress_val)
    
    st.subheader("App Curriculum Overview")
    st.write("- **Foundations (Free):** Master variables, strings, and syntax rules.")
    st.write("- **Control Flow & Loops (Free):** Learn how to build decisions and repeating routines.")
    st.write("- **Data Structures (Free):** Learn how to store collections using Lists and Dictionaries.")

# 2. FREE LESSONS
elif app_mode == "Free Lessons":
    st.header("Free Python Lessons")
    st.write("Master the basics of Python programming step-by-step.")
    
    lesson_tab = st.selectbox("Select Lesson", ["1. Variables & Strings", "2. Control Flow", "3. Data Structures"])
    
    if lesson_tab == "1. Variables & Strings":
        st.subheader("Lesson 1: Variables and Strings")
        st.write("A variable stores data. In Python, you create one by assigning a value using `=`: ")
        st.code('name = "Dillan"\nprint(name)', language="python")
    elif lesson_tab == "2. Control Flow":
        st.subheader("Lesson 2: Control Flow")
        st.write("Use `if`, `elif`, and `else` statements to make decisions in your code.")
        st.code('score = 85\nif score >= 50:\n    print("Pass")', language="python")
    else:
        st.subheader("Lesson 3: Data Structures")
        st.write("Lists let you store multiple items in a single variable ordered by index.")
        st.code('languages = ["Python", "JavaScript", "HTML"]\nprint(languages[0])', language="python")

# 3. PRO LESSONS
elif app_mode == "Pro Lessons (Advanced)":
    st.header("Pro Lessons (Advanced)")
    if not st.session_state.user_data["is_pro"]:
        st.warning("This section contains advanced modules. Unlock Pro to view content.")
        if st.button("Unlock Pro Access"):
            st.session_state.user_data["is_pro"] = True
            save_progress(st.session_state.user_data)
            st.success("Pro access unlocked successfully! Refreshing...")
            st.rerun()
    else:
        st.success("Welcome to Advanced Pro Modules!")
        st.write("- Object-Oriented Programming (OOP)")
        st.write("- File Handling and Automation Scripts")
        st.write("- Web Scraping with BeautifulSoup")

# 4. AI TEACHER ASSISTANT (TEXT, VOICE INPUT & VOICE OUTPUT)
elif app_mode == "AI Teacher Assistant":
    st.header("🤖 AI Python Teacher Assistant")
    st.write("Stuck on a tricky loop, a syntax bug, or a programming concept? Ask your AI tutor via typing or voice, and listen to spoken answers!")

    # Initialize Gemini Client using Streamlit secrets
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    client = None
    if api_key:
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            st.error(f"Failed to initialize Gemini client: {e}")

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Voice Input widget via mic recorder
    col1, col2 = st.columns([0.75, 0.25])
    with col2:
        spoken_text = speech_to_text(language="en", use_container_width=True, key="voice_input")

    # Standard Text Chat Input
    prompt = st.chat_input("Ask a Python question (e.g., How do functions work?)")

    # If voice input captured speech, override prompt
    if spoken_text:
        prompt = spoken_text

    if prompt:
        # Append and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI Response
        with st.chat_message("assistant"):
            with st.spinner("Thinking through your Python question..."):
                if client:
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=f"You are a friendly, encouraging Python programming teacher for beginners. Explain clearly and concisely: {prompt}"
                        )
                        ai_response = response.text
                    except Exception as e:
                        ai_response = f"⚠️ Error generating response: {e}"
                else:
                    ai_response = f"⚠️ Please configure your `GEMINI_API_KEY` in Streamlit secrets to enable live AI responses. (Your question was: {prompt})"
                
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

                # Text-to-Speech (gTTS) to let the AI talk back out loud
                try:
                    tts_file = BytesIO()
                    tts = gTTS(text=ai_response, lang="en", slow=False)
                    tts.write_to_fp(tts_file)
                    tts_file.seek(0)
                    st.audio(tts_file, format="audio/mp3", autoplay=True)
                except Exception as audio_err:
                    st.info(f"Audio playback note: {audio_err}")

# 5. CERTIFICATE OF COMPLETION
elif app_mode == "Certificate of Completion":
    st.header("Certificate of Completion")
    st.write("Generate and download your personalized PyCode Bite course completion certificate.")

    student_name_input = st.text_input("Enter your full name for the certificate:", st.session_state.user_data.get("student_name", "Dillan Mwadime"))
    st.session_state.user_data["student_name"] = student_name_input
    save_progress(st.session_state.user_data)

    if st.button("Mark Quiz Complete"):
        st.session_state.user_data["quiz_completed"] = True
        st.session_state.user_data["quiz_score"] = 3
        save_progress(st.session_state.user_data)
        st.success("Course requirements marked as complete!")

    if st.session_state.user_data["quiz_completed"]:
        st.success("🏆 Course Requirements Met! Your certificate is ready.")
        cert_text = f"""
==================================================
        PYCODE BITE LEARNING PLATFORM
          CERTIFICATE OF COMPLETION
==================================================

This certifies that

        {student_name_input}

has successfully completed the interactive Python curriculum and demonstrated core programming proficiency.

==================================================
"""
        st.text(cert_text)
        st.download_button(
            label="Download Certificate (TXT)",
            data=cert_text,
            file_name="PyCodeBite_Certificate.txt",
            mime="text/plain"
        )
    else:
        st.warning("Complete your quizzes and lessons to unlock your certificate generation.")