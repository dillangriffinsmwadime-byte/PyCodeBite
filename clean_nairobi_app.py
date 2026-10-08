import sys
import io
import contextlib
import os
import shutil
import json
import streamlit as st

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
        "Live Code Playground",
        "Python Quiz Engine",
        "AI Teacher Assistant",
        "Certificate of Completion",
        "Upgrade to Pro",
    ],
)

# 1. HOME DASHBOARD
if app_mode == "Home Dashboard":
    st.title("Welcome to PyCode Bite")
    st.write(
        "Your pocket-sized interactive tutor to master Python programming, test "
        "your logic with quizzes, and build real development skills."
    )

    if st.session_state.user_data["is_pro"]:
        st.success(
            "**PRO TIER ACTIVE**: All advanced automation modules and AI "
            "features are unlocked!"
        )
    else:
        st.info(
            "**Free Tier Active**: Upgrade to Pro anytime to unlock unlimited AI "
            "tutoring and advanced modules."
        )

    st.markdown("### Learning Progress Overview")
    score_val = st.session_state.user_data["quiz_score"]
    st.metric(label="Latest Quiz Score", value=f"{score_val} / 3")
    
    progress_val = 1.0 if st.session_state.user_data["quiz_completed"] else 0.5
    st.progress(progress_val, text="Overall Curriculum Completion")

    st.markdown("### App Curriculum Overview")
    st.markdown("• **Foundations (Free):** Master variables, strings, and syntax rules.")
    st.markdown("• **Control Flow & Loops (Free):** Learn how to build decisions and repeating routines.")
    st.markdown("• **Data Structures (Free):** Learn how to store collections using Lists and Dictionaries.")
    st.markdown("• **Automation & Lists (Pro):** Handle files, organize folders, and process data.")
    st.markdown("• **AI Python Teacher (Pro):** Get instant conversational help when debugging code.")

# 2. FREE LESSONS
elif app_mode == "Free Lessons":
    st.header("Free Lessons")
    st.subheader("Chapter 1: Variables & Core Syntax")
    st.write(
        "A variable is a container used to store data values. In Python, you "
        "create a variable simply by assigning a value using the '=' operator."
    )
    st.code(
        '# Example: Storing text and numbers\n'
        'app_name = "PyCode"\n'
        'base_version = 1.0\n'
        'print(f"Welcome to {app_name} v{base_version}!")',
        language="python",
    )

    st.subheader("Test It Out Link")
    user_input = st.text_input(
        "Enter a custom name for your script output:", st.session_state.user_data.get("student_name", "Dillan")
    )
    if st.button("Run Lesson Script"):
        st.success(f"Output: Hello {user_input}! Your variable was read successfully.")

    st.markdown("---")
    st.subheader("Chapter 2: Conditional Logic (If / Else)")
    st.write(
        "Programs make decisions using conditional statements. If a condition "
        "evaluates to True, the block runs; otherwise, it skips."
    )
    st.code(
        'score = 75\n'
        'if score >= 50:\n'
        '    print("Pass!")\n'
        'else:\n'
        '    print("Fail!")',
        language="python",
    )

    st.markdown("---")
    st.subheader("Chapter 3: Lists & Dictionaries")
    st.write(
        "Lists allow you to store multiple items in a single variable using square brackets `[]`. "
        "Dictionaries store key-value pairs using curly braces `{}`."
    )
    st.code(
        '# List of favorite tools\n'
        'tools = ["Photoshop", "Python", "VS Code"]\n'
        'print(tools[0])  # Output: Photoshop\n\n'
        '# Dictionary of user info\n'
        'user = {"name": "Dillan", "role": "Developer"}\n'
        'print(user["role"])  # Output: Developer',
        language="python",
    )
    
    st.write("💡 **Mini Challenge:** Try typing a python list assignment below (e.g., `my_list = [1, 2, 3]`) and click Validate.")
    challenge_input = st.text_input("Type your list code here:", "fruits = ['apple', 'banana', 'orange']")
    if st.button("Validate Challenge"):
        if "[" in challenge_input and "]" in challenge_input:
            st.success("Great job! Your code properly uses list brackets `[]`.")
        else:
            st.warning("Make sure to include square brackets `[]` to declare a valid list in Python.")

# 3. PRO LESSONS (ADVANCED)
elif app_mode == "Pro Lessons (Advanced)":
    st.header("Pro Chapter: Automation & File Handling")

    if not st.session_state.user_data["is_pro"]:
        st.warning(
            "**Locked Content:** This advanced module covers writing Python "
            "scripts that automate file organization and system tasks. Upgrade to "
            "Pro to unlock!"
        )
        if st.button("Unlock Pro Module Now"):
            st.session_state.user_data["is_pro"] = True
            save_progress(st.session_state.user_data)
            st.rerun()
    else:
        st.success("**Welcome to Pro Lessons: Advanced Script Unlocked!**")
        st.write(
            "In this module, you use Python's 'os' and 'shutil' libraries to scan directories, "
            "filter file extensions, and automate cleanups using raw string path handlers."
        )
        st.code(
            'import os\n'
            'import shutil\n\n'
            '# Define target directory safely using raw strings\n'
            'target_dir = r"C:\\Users\\dilla\\OneDrive\\Desktop\\PyCodeBite"\n'
            'backup_folder = os.path.join(target_dir, "TextBackups")\n\n'
            'if not os.path.exists(backup_folder):\n'
            '    os.makedirs(backup_folder)\n\n'
            'for filename in os.listdir(target_dir):\n'
            '    if filename.endswith(".txt"):\n'
            '        src = os.path.join(target_dir, filename)\n'
            '        dst = os.path.join(backup_folder, filename)\n'
            '        shutil.move(src, dst)',
            language="python",
        )

        st.markdown("---")
        st.subheader("Interactive Batch Renaming Tool")
        st.write("Run the batch renaming utility directly against your workspace directory.")
        prefix_input = st.text_input("Enter prefix for batch renaming:", "clean_")
        
        if st.button("Run Batch Rename Automation"):
            target_dir = r"C:\Users\dilla\OneDrive\Desktop\PyCodeBite"
            renamed_count = 0
            
            for filename in os.listdir(target_dir):
                if os.path.isfile(os.path.join(target_dir, filename)) and not filename.startswith(prefix_input) and filename != "app.py":
                    old_path = os.path.join(target_dir, filename)
                    new_filename = prefix_input + filename
                    new_path = os.path.join(target_dir, new_filename)
                    os.rename(old_path, new_path)
                    renamed_count += 1
            
            st.success(f"Automation Complete! Successfully renamed {renamed_count} files using prefix: '{prefix_input}'")

        st.markdown("---")
        st.subheader("Direct Script Export")
        st.write("Package and download your file organization automation script as a standalone `.py` file.")
        
        export_script_code = '''import os
import shutil

target_dir = r"C:\\Users\\dilla\\OneDrive\\Desktop\\PyCodeBite"
backup_folder = os.path.join(target_dir, "TextBackups")

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)
    print("Created 'TextBackups' folder.")

for filename in os.listdir(target_dir):
    if filename.endswith(".txt"):
        src = os.path.join(target_dir, filename)
        dst = os.path.join(backup_folder, filename)
        shutil.move(src, dst)
        print(f"Moved: {filename} -> TextBackups/")
'''
        st.download_button(
            label="Download Automation Script (.py)",
            data=export_script_code,
            file_name="auto_organizer.py",
            mime="text/plain",
        )

# 4. LIVE CODE PLAYGROUND
elif app_mode == "Live Code Playground":
    st.subheader("Live Python Playground")
    st.write(
        "Write custom Python code below and click 'Execute Script' to run it "
        "safely inside your environment sandbox."
    )

    default_code = 'print("Welcome to PyCodeBite!")\n\n# Try writing a loop:\nfor i in range(3):\n    print(f"Count: {i}")'
    user_code = st.text_area("Code Editor", value=default_code, height=180)

    if st.button("Execute Script"):
        output_buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(output_buffer):
                exec(user_code)
            execution_output = output_buffer.getvalue()

            st.success("Execution Complete:")
            st.code(
                execution_output
                if execution_output
                else "Code ran with no printed output.",
                language="python",
            )
        except Exception as err:
            st.error(f"Runtime Error: {err}")

# 5. PYTHON QUIZ ENGINE
elif app_mode == "Python Quiz Engine":
    st.header("Python Knowledge Quiz")
    st.write(
        "Test your understanding of Python fundamentals with this interactive 3-question quiz."
    )

    q1 = "1. Which keyword is used to define a function in Python?"
    ans1 = st.radio(
        q1,
        ["def", "function", "fun", "define"],
        key="q1",
    )

    q2 = "2. Which symbol is used to write single-line comments in Python?"
    ans2 = st.radio(q2, ["//", "/", "*", "#"], key="q2")

    q3 = "3. What data type is the result of: x = 10 / 2 in Python 3?"
    ans3 = st.radio(
        q3,
        ["Integer (int)", "Float (float)", "String", "Boolean"],
        key="q3",
    )

    if st.button("Submit All Answers"):
        score = 0
        if ans1 == "def":
            score += 1
        if ans2 == "#":
            score += 1
        if ans3 == "Float (float)":
            score += 1

        st.session_state.user_data["quiz_score"] = score
        st.session_state.user_data["quiz_completed"] = True
        save_progress(st.session_state.user_data)

        if score == 3:
            st.success(
                f"Flawless Victory! Score: {score}/3 correct. Outstanding work!"
            )
            st.balloons()
        elif score >= 1:
            st.info(
                f"Good effort! Score: {score}/3 correct. Review the lesson tabs "
                "to master the missed concepts."
            )
        else:
            st.error(
                f"❌ Score: {score}/3. Don't worry! Jump over to the **AI Teacher** "
                "tab to get step-by-step guidance."
            )

# 6. AI TEACHER ASSISTANT
elif app_mode == "AI Teacher Assistant":
    st.header("AI Python Teacher Chat")

    if not st.session_state.user_data["is_pro"]:
        st.warning(
            "**Pro Feature Locked:** The conversational AI Teacher assistant is "
            "restricted to Pro members. Upgrade to get unlimited debugging "
            "support!"
        )
        if st.button("Instant Pro Unlock"):
            st.session_state.user_data["is_pro"] = True
            save_progress(st.session_state.user_data)
            st.rerun()
    else:
        st.write(
            "Stuck on a tricky loop, a syntax bug, or a quiz question? Ask your AI "
            "tutor right here!"
        )

        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an encouraging, friendly Python programming instructor."
                    ),
                }
            ]

        for message in st.session_state.messages:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        if user_prompt := st.chat_input(
            "Ask a question (e.g., 'How do for loops work?')"
        ):
            st.session_state.messages.append(
                {"role": "user", "content": user_prompt}
            )
            with st.chat_message("user"):
                st.markdown(user_prompt)

            if "loop" in user_prompt.lower():
                ai_response = (
                    "A for loop iterates over a sequence. Here is a quick example:\n"
                    "```python\nfor i in range(3):\n    print(f'Item index: {i}')\n```"
                )
            elif "function" in user_prompt.lower():
                ai_response = (
                    "Functions group code blocks together using 'def'. Example:\n"
                    "```python\ndef calculate_sum(a, b):\n    return a + b\n```"
                )
            else:
                ai_response = (
                    f"That's a great question about '{user_prompt}'! In Python, breaking "
                    "your logic down line-by-line helps isolate errors. What specific "
                    "part of your script are you testing right now?"
                )

            with st.chat_message("assistant"):
                st.markdown(ai_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )

# 7. CERTIFICATE OF COMPLETION
elif app_mode == "Certificate of Completion":
    st.header("Certificate of Completion")
    st.write("Generate and download your personalized PyCode Bite course completion certificate.")

    student_name_input = st.text_input("Enter your full name for the certificate:", st.session_state.user_data.get("student_name", "Dillan Mwadime"))
    st.session_state.user_data["student_name"] = student_name_input
    save_progress(st.session_state.user_data)

    if st.session_state.user_data["quiz_completed"]:
        st.success("🎉 Course Requirements Met! Your certificate is ready for generation.")
        
        cert_text = f"""==================================================
           PYCODE BITE LEARNING PLATFORM
            CERTIFICATE OF COMPLETION
==================================================

  This certifies that
  
      {student_name_input}
      
  has successfully completed the interactive Python 
  programming curriculum, core modules, and assessments.
  
  Score Achieved: {st.session_state.user_data['quiz_score']} / 3
  Platform: PyCode Bite Hub (Streamlit Edition)
==================================================="""
        
        st.code(cert_text, language="text")
        st.download_button(
            label="Download Official Certificate (.txt)",
            data=cert_text,
            file_name="PyCodeBite_Certificate.txt",
            mime="text/plain",
        )
    else:
        st.warning("⚠️ You must complete the **Python Quiz Engine** test at least once before generating your certificate.")

# 8. UPGRADE TO PRO
elif app_mode == "Upgrade to Pro":
    st.title("Unlock PyCode Bite Pro")
    st.write(
        "Take your coding journey further with lifetime access to advanced "
        "automation modules, an ad-free workspace, and unlimited AI tutoring."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Free Tier")
        st.markdown("- Core Syntax Lessons")
        st.markdown("- Standard Quiz Engine")
        st.markdown("- Interactive Playground")
    with col2:
        st.markdown("### Pro Tier")
        st.markdown("- Unlimited AI Tutor")
        st.markdown("- Advanced Automation Modules")
        st.markdown("- Priority Updates & Badges")

    st.markdown("---")
    if not st.session_state.user_data["is_pro"]:
        if st.button("Upgrade to Pro Now ($2.99)"):
            st.session_state.user_data["is_pro"] = True
            save_progress(st.session_state.user_data)
            st.success(
                "Payment simulation successful! Pro features are now unlocked!"
            )
            st.balloons()
    else:
        st.info("You are currently a verified Pro subscriber. Enjoy your full app!")