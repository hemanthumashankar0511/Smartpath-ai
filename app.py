import streamlit as st
from data import db
from chains import assessment_chain, curriculum_chain, progress_chain
from prompts.assessment_questions import get_questions, DOMAINS
from utils import resource_finder, logger
import json
import base64
from streamlit_extras.let_it_rain import rain
import random
import hashlib
from streamlit_echarts import st_echarts
# from streamlit_calendar_heatmap import calendar_heatmap
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from langchain_community.llms import Ollama
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

# Load environment variables from .env
load_dotenv()

st.set_page_config(page_title="SmartPath AI", layout="centered")

pages = [
    "Home",
    "Register/Login",
    "Assessment",
    "Learning Path",
    "Progress",
    "My Learning Paths",
    "Profile",
    "Ask the AI Agent"
]
page = st.sidebar.radio("Navigate", pages)

if 'user' not in st.session_state:
    st.session_state['user'] = None

def register_user():
    st.subheader("Register or Login")
    name = st.text_input("Name", help="Enter your full name.")
    email = st.text_input("Email", help="We'll never share your email. Must be a valid email address.")
    def is_valid_email(email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
    if st.button("Register/Login"):
        if not name.strip() or not email.strip():
            st.error("Name and email cannot be empty.")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        try:
            user = db.get_user_by_email(email)
            if not user:
                user_id = db.add_user(name, email)
                st.session_state['user'] = {'id': user_id, 'name': name, 'email': email}
                st.success(f"Registered as {name}")
            else:
                st.session_state['user'] = {'id': user[0], 'name': user[1], 'email': user[2]}
                st.success(f"Logged in as {user[1]}")
        except Exception as e:
            st.error(f"Registration/Login failed: {e}")

def get_llama_model():
    """Return a small Ollama model instance for LLM calls."""
    from langchain_community.llms import Ollama
    return Ollama(model="llama3.2:3b")

def get_llava_model():
    """Return a LLaVA Ollama model instance for multimodal LLM calls."""
    from langchain_community.llms import Ollama
    return Ollama(model="llava")

def assessment_page():
    st.subheader("Skill Assessment")
    st.markdown("Select your domain and answer the questions below. Your answers help us personalize your learning path.")
    domain = st.selectbox("Choose a domain", list(DOMAINS.keys()), help="Pick the subject you want to learn.")
    if 'assessment_questions' not in st.session_state or st.session_state.get('assessment_domain') != domain:
        st.session_state['assessment_questions'] = get_questions(domain, seed=random.randint(0, 999999))
        st.session_state['assessment_domain'] = domain
    questions = st.session_state['assessment_questions']
    user_answers = []
    st.markdown("#### Domain Questions")
    for i, q in enumerate(questions[:10]):
        ans = st.radio(f"Q{i+1}: {q['question']}", q['choices'], key=f"q_{i}", help="Choose the best answer.")
        user_answers.append(ans)
    if st.button("Submit Assessment"):
        if any(a is None or a == '' for a in user_answers):
            st.error("Please answer all questions before submitting.")
            return
        with st.spinner("Analyzing your answers..."):
            try:
                result = assessment_chain.run_assessment(
                    user_id=st.session_state['user']['id'],
                    domain=domain,
                    user_answers=user_answers,
                    questions=questions,
                    style_answers=[]
                )
                st.session_state['assessment_result'] = result
                # Show score summary at the top
                st.success(f"Assessment complete!")
                st.markdown(f"### Score: **{result['correct_count']} / {result['total']}** ({int(result['score']*100)}%)")
                st.markdown(f"### Skill Level: **{result['skill_level']}**")
                # Show detailed results
                st.markdown("### Your Answers vs Correct Answers")
                llm = get_llama_model()
                for i, qres in enumerate(result['questions']):
                    st.markdown(f"**Q{i+1}: {qres['question']}")
                    st.write(f"Your answer: {qres['user_answer']}")
                    st.write(f"Correct answer: {qres['correct_answer']}")
                    prompt = f"Question: {qres['question']}\nCorrect answer: {qres['correct_answer']}\nExplain simply why this is the correct answer."
                    with st.spinner("AI is explaining..."):
                        try:
                            explanation = llm(prompt)
                            st.info(f"AI Explanation: {explanation}")
                        except Exception as e:
                            st.warning(f"AI explanation failed: {e}")
                    st.markdown("---")
                del st.session_state['assessment_questions']
                del st.session_state['assessment_domain']
                logger.log_action(st.session_state['user']['id'], 'Assessment Submitted', f'domain={domain}, skill={result["skill_level"]}')
            except Exception as e:
                st.error(f"Assessment failed: {e}")
                logger.log_error(st.session_state['user']['id'], 'Assessment Failed', str(e))

def get_pdf_resources(query):
    """Search for up-to-date PDF resources for a given query using a simple Google search link."""
    # This is a simple approach; for more advanced, use a PDF search API
    google_query = f"{query} filetype:pdf"
    google_url = f"https://www.google.com/search?q={google_query.replace(' ', '+')}"
    return f"[Search for PDFs on Google]({google_url})"

def learning_path_page():
    st.subheader("Your Learning Path")
    st.markdown("Generate a personalized curriculum based on your assessment and preferences.")
    if 'assessment_result' not in st.session_state:
        st.info("Please complete an assessment first.")
        return
    result = st.session_state['assessment_result']
    study_time = st.selectbox("How much time can you study per week?", ["<2 hours", "2-5 hours", "5-10 hours", ">10 hours"], help="This helps us set a realistic timeline.")
    show_resources = False
    if st.button("Generate Learning Path"):
        user_id = st.session_state['user']['id']
        db_paths = db.get_learning_paths_by_user(user_id)
        for p in db_paths:
            if p['title'] == result['domain'] and p['milestones'] == json.dumps(result.get('milestones', [])):
                st.warning("You already have a learning path for this domain and skill level.")
                return
        with st.spinner("Building your learning path..."):
            try:
                path = curriculum_chain.plan_learning_path(
                    user_id=user_id,
                    assessment_result=result,
                    study_time=study_time
                )
                st.session_state['learning_path'] = path
                st.success("Learning path generated!")
                st.json(path)
                logger.log_action(user_id, 'Learning Path Generated', f'title={path["title"]}')
                show_resources = True
            except Exception as e:
                st.error(f"Failed to generate learning path: {e}")
                logger.log_error(user_id, 'Learning Path Generation Failed', str(e))
    # Always show resources if learning_path is in session or just generated
    if 'learning_path' in st.session_state or show_resources:
        path = st.session_state['learning_path']
        st.markdown(f"### {path['title']}")
        st.write(f"**Timeline:** {path['timeline_weeks']} weeks")
        milestones = path['milestones']
        path_id = f"completed_milestones_{path['title']}"
        if path_id not in st.session_state:
            st.session_state[path_id] = []
        completed = st.session_state[path_id]
        st.session_state['completed_milestones'] = completed  # ensure global progress page uses this
        st.markdown("#### Milestones & Resources")
        user_id = st.session_state['user']['id']
        db_paths = db.get_learning_paths_by_user(user_id)
        learning_path_id = None
        for p in db_paths:
            if p['title'] == path['title'] and json.loads(p['milestones']) == milestones:
                learning_path_id = p['id']
                break
        for i, m in enumerate(milestones):
            with st.expander(f"{i+1}. {m['title']}  ", expanded=(i==0)):
                col1, col2 = st.columns([3, 2])
                with col1:
                    checked = st.checkbox(f"Mark as completed", value=m['title'] in completed, key=f"milestone_{path['title']}_{i}")
                    if checked and m['title'] not in completed:
                        completed.append(m['title'])
                        st.session_state[path_id] = completed
                        st.session_state['completed_milestones'] = completed
                    elif not checked and m['title'] in completed:
                        completed.remove(m['title'])
                        st.session_state[path_id] = completed
                        st.session_state['completed_milestones'] = completed
                    st.write(f"{m['description']}")
                    note_key = f"note_{learning_path_id}_{m['title']}"
                    if learning_path_id:
                        if note_key not in st.session_state:
                            try:
                                st.session_state[note_key] = db.get_note(user_id, learning_path_id, m['title'])
                            except Exception as e:
                                st.session_state[note_key] = ""
                                st.warning(f"Could not load note: {e}")
                        note = st.text_area("Your Notes", value=st.session_state[note_key], key=note_key, help="Add your notes for this milestone. Empty notes will not be saved.")
                        if st.button(f"Save Note {i}"):
                            if note.strip() == "":
                                st.warning("Note is empty. Not saved.")
                            else:
                                try:
                                    db.save_note(user_id, learning_path_id, m['title'], note)
                                    st.success("Note saved!")
                                    logger.log_action(user_id, 'Note Saved', f'path_id={learning_path_id}, milestone={m["title"]}')
                                except Exception as e:
                                    st.error(f"Failed to save note: {e}")
                with col2:
                    domain = path.get('domain')
                    if not domain:
                        domain = path['title'].split()[0].lower()
                    yt_results = resource_finder.search_youtube(m['title'] + ' ' + domain)
                    if yt_results:
                        for vid in yt_results:
                            st.video(vid['url'])
                            st.caption(f"{vid['title']}")
                    pdf_link = get_pdf_resources(m['title'] + ' ' + domain)
                    st.markdown("**PDF Resources:**")
                    st.markdown(pdf_link)
        progress = len(completed) / len(milestones) if milestones else 0
        capped_progress = min(progress, 1.0)
        st.progress(capped_progress, text=f"{len(completed)}/{len(milestones)} milestones completed")
        st.markdown("#### Export Your Learning Path")
        if st.button("Download as JSON"):
            json_str = json.dumps(path, indent=2)
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:file/json;base64,{b64}" download="learning_path.json">Download learning_path.json</a>'
            st.markdown(href, unsafe_allow_html=True)

def progress_page():
    st.subheader("Progress Tracker")
    st.markdown("Track your progress and see your achievements.")
    if 'learning_path' not in st.session_state:
        st.info("Generate a learning path first.")
        return
    path = st.session_state['learning_path']
    milestones = [m['title'] for m in path['milestones']]
    completed = st.session_state.get('completed_milestones', [])
    st.markdown("#### Progress Overview")
    progress = len(completed) / len(milestones) if milestones else 0
    st.progress(progress, text=f"{len(completed)}/{len(milestones)} milestones completed")
    if progress == 1.0:
        st.success("Congratulations! You completed your learning path!")
    elif progress >= 0.5:
        st.info("Great job! You're more than halfway there.")
    st.markdown("#### Study Progress Chart")
    st.line_chart([i/len(milestones) for i in range(1, len(completed)+1)])
    st.markdown("#### Recommendations")
    if progress < 1.0:
        st.write("Keep a steady pace. Try to complete your milestones!")
    else:
        st.write("Consider exploring advanced topics or new domains.")
    if st.button("Save Progress"):
        with st.spinner("Saving your progress..."):
            try:
                progress_chain.record_progress(st.session_state['user']['id'], completed)
                st.success("Progress saved!")
                logger.log_action(st.session_state['user']['id'], 'Progress Saved', f'completed={completed}')
            except Exception as e:
                st.error(f"Failed to save progress: {e}")
                logger.log_error(st.session_state['user']['id'], 'Progress Save Failed', str(e))
    progress_data = progress_chain.get_progress(st.session_state['user']['id'])
    st.write(f"Last updated: {progress_data['last_updated']}")

def my_learning_paths_page():
    st.subheader("My Learning Paths")
    user_id = st.session_state['user']['id']
    paths = db.get_learning_paths_by_user(user_id)
    if not paths:
        st.info("No previous learning paths found. Complete an assessment to generate your first path!")
        return
    path_titles = [f"{p['title']} (ID: {p['id']})" for p in paths]
    selected = st.selectbox("Select a learning path to view/resume:", path_titles, help="View or resume any of your previous learning paths.")
    idx = path_titles.index(selected)
    path = paths[idx]
    milestones = json.loads(path['milestones'])
    st.markdown(f"### {path['title']}")
    st.write(f"**Timeline:** {path['timeline']} weeks")
    progress_data = db.get_progress_by_user(user_id)
    completed = []
    if progress_data:
        completed = progress_data[0]['completed_items']
    st.markdown("#### Milestones & Resources")
    for i, m in enumerate(milestones):
        st.markdown(f"- {'Completed' if m['title'] in completed else 'Not completed'} {m['title']}")
    progress = len(completed) / len(milestones) if milestones else 0
    st.progress(progress, text=f"{len(completed)}/{len(milestones)} milestones completed")
    if st.button("Resume this path"):
        st.session_state['learning_path'] = {
            'title': path['title'],
            'milestones': milestones,
            'timeline_weeks': path['timeline']
        }
        st.session_state['completed_milestones'] = completed
        # Try to fetch the actual assessment result if available
        st.session_state['assessment_result'] = {
            'domain': path['title'].split()[0].lower(),
            'skill_level': '',
            'learning_style': {},
        }
        st.success("Learning path loaded! Go to the Learning Path or Progress page to continue.")

def profile_page():
    st.subheader("Profile")
    user = st.session_state['user']
    email_hash = hashlib.md5(user['email'].strip().lower().encode()).hexdigest()
    gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?d=identicon&s=120"
    st.image(gravatar_url, width=80)
    st.markdown(f"**Name:** {user['name']}")
    st.markdown(f"**Email:** {user['email']}")
    paths = db.get_learning_paths_by_user(user['id'])
    total_paths = len(paths)
    total_milestones = sum(len(json.loads(p['milestones'])) for p in paths)
    progress_data = db.get_progress_by_user(user['id'])
    completed_milestones = sum(len(p['completed_items']) for p in progress_data)
    st.markdown(f"**Learning Paths:** {total_paths}", help="Total number of learning paths you've created.")
    st.markdown(f"**Total Milestones:** {total_milestones}", help="Sum of all milestones across your learning paths.")
    st.markdown(f"**Milestones Completed:** {completed_milestones}", help="How many milestones you've finished.")
    badges = []
    if total_paths >= 1:
        badges.append('Path Starter')
    if completed_milestones >= 10:
        badges.append('10+ Milestones')
    if completed_milestones >= 25:
        badges.append('25+ Milestones')
    if completed_milestones >= total_milestones and total_milestones > 0:
        badges.append('All Milestones Complete!')
    if badges:
        st.markdown("**Achievements:** " + ' '.join([f"{b} (hover for info)" for b in badges]))
    else:
        st.info("No badges yet. Start learning to earn achievements!")
    domain_counts = {}
    for p in paths:
        milestones = json.loads(p['milestones'])
        for m in milestones:
            domain = p['title'].split()[0].capitalize()
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
    radar_data = [
        {"value": [domain_counts.get(d, 0) for d in domain_counts], "name": "Milestones"}
    ]
    radar_ind = [{"name": d, "max": max(domain_counts.values()) or 1} for d in domain_counts]
    if domain_counts:
        st.markdown("#### Skill Profile")
        st_echarts({
            "tooltip": {},
            "radar": {"indicator": radar_ind},
            "series": [{"type": "radar", "data": radar_data}]
        }, height="350px")
    if progress_data:
        st.markdown("#### Milestone Completion Calendar")
        date_counts = {}
        for p in progress_data:
            if p['last_updated']:
                date = p['last_updated'][:10]
                date_counts[date] = date_counts.get(date, 0) + len(p['completed_items'])
        if date_counts:
            dates = sorted(date_counts.keys())
            values = [date_counts[d] for d in dates]
            days = [datetime.strptime(d, "%Y-%m-%d").timetuple().tm_yday for d in dates]
            arr = np.zeros(366)
            for d, v in zip(days, values):
                arr[d-1] = v
            fig, ax = plt.subplots(figsize=(10, 1))
            ax.imshow([arr], cmap="YlGn", aspect="auto")
            ax.set_yticks([])
            ax.set_xticks(np.linspace(0, 365, 13))
            ax.set_xticklabels([datetime(2000, m, 1).strftime('%b') for m in range(1, 13)] + [''])
            ax.set_title("Milestone Completion Heatmap (by day of year)")
            st.pyplot(fig)
        else:
            st.info("No milestone completion data yet.")

def ai_agent_page():
    st.subheader("Ask the AI Agent")
    st.markdown("This is your GenAI-powered assistant. Ask anything! Optionally, upload an image for multimodal Q&A.")
    user_input = st.text_area("Your question:", key="ai_agent_input")
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"], key="ai_agent_image")
    if st.button("Ask AI"):
        if not user_input.strip() and not uploaded_image:
            st.warning("Please enter a question or upload an image.")
        else:
            with st.spinner("Thinking..."):
                try:
                    if uploaded_image:
                        import tempfile
                        import google.generativeai as genai
                        from PIL import Image
                        import io
                        import os
                        # Get Gemini API key
                        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
                        if not GEMINI_API_KEY:
                            st.error("GEMINI_API_KEY not set in environment.")
                            return
                        genai.configure(api_key=GEMINI_API_KEY)
                        # Load image
                        image_bytes = uploaded_image.read()
                        image = Image.open(io.BytesIO(image_bytes))
                        # Use Gemini multimodal model
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = user_input.strip() or "Describe this image in detail. List all visible objects, people, text, and actions. Be as specific as possible."
                        response = model.generate_content([
                            prompt,
                            image
                        ])
                        st.markdown(f"**AI Agent:** {response.text}")
                    else:
                        llm = get_llama_model()
                        response = llm(user_input)
                        st.markdown(f"**AI Agent:** {response}")
                except Exception as e:
                    st.error(f"AI Agent failed: {e}")

if page == "Home":
    st.title("Welcome to SmartPath AI")
    st.markdown("""
    **SmartPath AI** is your personalized, AI-powered learning path generator. Whether you're starting a new subject or advancing your skills, SmartPath AI helps you:
    
    - Assess your current knowledge and learning style
    - Get a custom curriculum tailored to your needs
    - Discover high-quality resources for every milestone
    - Track your progress and celebrate your achievements
    
    **How it works:**
    1. **Register or log in** to create your personal account
    2. **Take a skill assessment** to help us understand your strengths and goals
    3. **Get your personalized learning path** with a clear timeline and milestones
    4. **Track your progress** and add notes as you learn
    5. **Resume or review** your learning paths anytime
    
    Ready to begin? Use the navigation menu on the left to get started!
    """)
elif page == "Register/Login":
    register_user()
elif page == "Assessment":
    if st.session_state['user']:
        assessment_page()
    else:
        st.info("Please register or log in first.")
elif page == "Learning Path":
    if st.session_state['user']:
        learning_path_page()
    else:
        st.info("Please register or log in first.")
elif page == "Progress":
    if st.session_state['user']:
        progress_page()
    else:
        st.info("Please register or log in first.")
elif page == "My Learning Paths":
    if st.session_state['user']:
        my_learning_paths_page()
    else:
        st.info("Please register or log in first.")
elif page == "Profile":
    if st.session_state['user']:
        profile_page()
    else:
        st.info("Please register or log in first.")
elif page == "Ask the AI Agent":
    ai_agent_page() 