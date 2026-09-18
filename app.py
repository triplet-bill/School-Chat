import streamlit as st
import datetime
import time
import os
import json
import hashlib

st.set_page_config(page_title="School Space Chat", page_icon="💬", layout="centered")

# Custom Sleek Dark Theme Styles
st.markdown("""
    <style>
        .stApp { background-color: #121214; }
        input {
            border-radius: 8px !important;
            border: 1px solid #2d2d34 !important;
            background-color: #1a1a1e !important;
            color: #ffffff !important;
        }
        .system-badge { background-color: #202024; color: #9ca3af; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; }
        .owner-badge { background-color: #ff4b4b22; color: #ff4b4b; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; border: 1px solid #ff4b4b44; }
        .student-badge { background-color: #2f2f35; color: #a78bfa; padding: 4px 8px; border-radius: 6px; font-size: 11px; font-weight: bold; }
        .alert-box { background: linear-gradient(90deg, #ff4b4b11, #ff767611); border-left: 4px solid #ff4b4b; padding: 12px; border-radius: 0px 8px 8px 0px; margin: 5px 0px; }
    </style>
""", unsafe_allow_html=True)

PROFANITY_LIST = ["badword1", "badword2"]
USER_DB_FILE = "users_database.json"
CHAT_DB_FILE = "chat_database.json"
MOD_DB_FILE = "mod_database.json"
PRESENCE_FILE = "presence_database.json"

# --- 📁 SYSTEM FILE READ/WRITE ACTIONS ---
def load_user_database():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            try:
                db = json.load(f)
                db["Billy"] = {"password": hashlib.sha256("Rd129286".encode()).hexdigest(), "role": "OWNER"}
                return db
            except:
                pass
    return {"Billy": {"password": hashlib.sha256("Rd129286".encode()).hexdigest(), "role": "OWNER"}}

def save_user_database(db_data):
    with open(USER_DB_FILE, "w") as f:
        json.dump(db_data, f)

def load_chat_database():
    if os.path.exists(CHAT_DB_FILE):
        with open(CHAT_DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return [{"id": 0, "user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": "Welcome back to the room. Real-time persistent sync is active."}]

def save_chat_database(chat_data):
    with open(CHAT_DB_FILE, "w") as f:
        json.dump(chat_data, f)

def load_mod_database():
    if os.path.exists(MOD_DB_FILE):
        with open(MOD_DB_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {"banned": [], "timeouts": {}}

def save_mod_database(mod_data):
    with open(MOD_DB_FILE, "w") as f:
        json.dump(mod_data, f)

def load_presence_database():
    if os.path.exists(PRESENCE_FILE):
        with open(PRESENCE_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                pass
    return {}

def save_presence_database(presence_data):
    with open(PRESENCE_FILE, "w") as f:
        json.dump(presence_data, f)

def update_user_presence(username):
    presence = load_presence_database()
    presence[username] = time.time()
    save_presence_database(presence)

def get_active_users():
    presence = load_presence_database()
    now = time.time()
    active = []
    for user, last_seen in list(presence.items()):
        if now - last_seen < 300:
            active.append(user)
    return active

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

def clean_text(text):
    words = text.split()
    return " ".join(["*" * len(w) if w.strip(".,!?\"'").lower() in PROFANITY_LIST else w for w in words])

# --- 🔓 SIGN IN & SIGN UP GATEWAY ---
if "gate_cleared" not in st.session_state:
    st.session_state["gate_cleared"] = False
    st.session_state["nickname"] = ""
    st.session_state["is_owner"] = False

if not st.session_state["gate_cleared"]:
    st.markdown("<h2 style='text-align: center; color: white;'>🏫 School Space Gateway</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔒 Returning Log In", "📝 First-Time Sign Up"])
    user_db = load_user_database()
    mod_db = load_mod_database()
    
    with tab1:
        st.markdown("<p style='color: gray;'>Log in using your registered nickname.</p>", unsafe_allow_html=True)
        login_name = st.text_input("Username / Nickname:", key="login_user")
        login_pass = st.text_input("Your Account Password:", type="password", key="login_password")
        
        if st.button("Log In", use_container_width=True, type="primary"):
            name_clean = login_name.strip()
            if name_clean in mod_db.get("banned", []):
                st.error("❌ This account is permanently banned.")
            elif name_clean in user_db and user_db[name_clean]["password"] == hash_pass(login_pass):
                st.session_state["nickname"] = name_clean
                st.session_state["is_owner"] = (user_db[name_clean]["role"] == "OWNER")
                st.session_state["gate_cleared"] = True
                update_user_presence(name_clean)
                st.rerun()
            else:
                st.error("❌ Invalid username or account password.")
                
    with tab2:
        st.markdown("<p style='color: gray;'>Choose a permanent nickname. You will only have to do this once.</p>", unsafe_allow_html=True)
        reg_name = st.text_input("Choose Nickname (No Spaces):", max_chars=15, key="reg_user")
        reg_pass = st.text_input("Create Account Password:", type="password", key="reg_password")
        invite_code = st.text_input("Enter School Invite Code:", type="password")
        
        if st.button("Create Permanent Account", use_container_width=True):
            name_clean = reg_name.strip()
            if not name_clean or " " in name_clean:
                st.error("❌ Nickname cannot be blank and cannot contain spaces.")
            elif name_clean in user_db or name_clean == "Billy":
                st.error("❌ That username is already taken or reserved.")
            elif invite_code != "School123":
                st.error("❌ Incorrect school registration invite code.")
            elif len(reg_pass) < 4:
                st.error("❌ Your password must be at least 4 characters long.")
            else:
                user_db[name_clean] = { "password": hash_pass(reg_pass), "role": "STUDENT" }
                save_user_database(user_db)
                st.success("🎉 Account created successfully! Switch to the 'Log In' tab to join.")
    st.stop()

# Track active presence
update_user_presence(st.session_state["nickname"])

# --- 👥 SIDEBAR SIDE MEMBER LIST PANEL ---
with st.sidebar:
    st.markdown("<h2 style='color: white;'>👥 Active Members</h2>", unsafe_allow_html=True)
    online_users = get_active_users()
    for user in online_users:
        if user == "Billy":
            st.markdown("👑 **Billy** *(Owner)*")
        else:
            st.markdown(f"👤 {user}")
    st.markdown("---")
    if st.button("🔄 Refresh Members/Messages", use_container_width=True):
        st.rerun()

# --- 🏫 MAIN CHATROOM AREA ---
st.markdown("<h2 style='color: white; margin-bottom: 0px;'>🏫 Live School Room</h2>", unsafe_allow_html=True)
role_label = "👑 OWNER" if st.session_state["is_owner"] else "STUDENT"
st.markdown(f"<p style='color: #888888; font-size: 14px;'>Active Session: <b style='color:#ffffff;'>{st.session_state['nickname']}</b> ({role_label})</p>", unsafe_allow_html=True)

# Load layout parameters
global_history = load_chat_database()
mod_db = load_mod_database()

# --- 🛠️ MODERATION POP-UP MODAL ENGINE ---
@st.dialog("🛡️ Message Action Toolkit")
def open_mod_menu(msg_id, target_user):
    st.markdown(f"What action do you want to take against user **{target_user}**?")
    current_chat = load_chat_database()
    current_mod = load_mod_database()
    
    if st.button("🗑️ Delete Single Message", use_container_width=True):
        updated_chat = [m for m in current_chat if m.get("id") != msg_id]
        save_chat_database(updated_chat)
        st.success("Message removed!")
        time.sleep(0.5)
        st.rerun()
        
    timeout_mins = st.number_input("Timeout Duration (Minutes):", min_value=1, max_value=1440, value=5)
    if st.button(f"⏱️ Timeout {target_user}", use_container_width=True):
        current_mod["timeouts"][target_user] = time.time() + (timeout_mins * 60)
        save_mod_database(current_mod)
        current_chat.append({"id": int(time.time()), "user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": f"User '{target_user}' has been placed in timeout for {timeout_mins} minute(s)."})
        save_chat_database(current_chat)
        st.success(f"{target_user} timed out!")
        time.sleep(0.5)
        st.rerun()

# --- 💬 RENDERING LIVE TEXT LOGS ---
chat_container = st.container(height=420, border=True)
with chat_container:
    for item in global_history:
        tag = item.get("tag", "STUDENT")
        time_stamp = f"<span style='color:#6b7280; font-size:11px; margin-left:8px;'>{item['time']}</span>"
        
        if st.session_state["is_owner"] and item["user"] != "System" and item["user"] != st.session_state["nickname"]:
            c_msg, c_btn = st.columns([0.85, 0.15])
            with c_msg:
                if tag == "OWNER":
                    st.markdown(f"<div><span class='owner-badge'>👑 OWNER</span> <b style='color:#ffffff;'>{item['user']}</b>{time_stamp}</div><div style='color: #f3f4f6; padding: 2px 0px 8px 0px;'>{item['content']}</div>", unsafe_allow_html=True)
                elif tag == "OWNER ALERT":
                    st.markdown(f"<div class='alert-box'><span class='owner-badge'>🚨 ALERT</span> <b style='color:#ffffff;'>{item['user']}</b>{time_stamp}<br><div style='color:#ff4b4b; padding-top:4px;'>{item['content']}</div></div>", unsafe_allow_html=True)
