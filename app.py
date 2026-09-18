import streamlit as st
import datetime
import time
import os
import json
import hashlib

st.set_page_config(page_title="School Space Chat", page_icon="💬", layout="centered")

# Custom Sleek Interface CSS Styles
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

# --- 📁 PERMANENT DATABASE SECURITY FUNCTIONS ---
def load_user_database():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            try:
                db = json.load(f)
                # Overwrite or enforce your custom owner settings into the database file
                db["Billy"] = {
                    "password": hashlib.sha256("Rd129286".encode()).hexdigest(),
                    "role": "OWNER"
                }
                return db
            except:
                pass
                
    # Default master account configuration (Your username is Billy!)
    return {
        "Billy": {
            "password": hashlib.sha256("Rd129286".encode()).hexdigest(),
            "role": "OWNER"
        }
    }

def save_user_database(db_data):
    with open(USER_DB_FILE, "w") as f:
        json.dump(db_data, f)

def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Live Room History Memory
if "global_chat_history" not in st.session_state:
    st.session_state["global_chat_history"] = [{"user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": "Welcome back to the room. Persistent student accounts are now active."}]
if "banned_users" not in st.session_state:
    st.session_state["banned_users"] = []
if "timeout_users" not in st.session_state:
    st.session_state["timeout_users"] = {}

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
    
    with tab1:
        st.markdown("<p style='color: gray;'>Log in using your registered nickname.</p>", unsafe_allow_html=True)
        login_name = st.text_input("Username / Nickname:", key="login_user")
        login_pass = st.text_input("Your Account Password:", type="password", key="login_password")
        
        if st.button("Log In", use_container_width=True, type="primary"):
            name_clean = login_name.strip()
            if name_clean in st.session_state["banned_users"]:
                st.error("❌ This account is permanently banned.")
            elif name_clean in user_db and user_db[name_clean]["password"] == hash_pass(login_pass):
                st.session_state["nickname"] = name_clean
                st.session_state["is_owner"] = (user_db[name_clean]["role"] == "OWNER")
                st.session_state["gate_cleared"] = True
                st.success("Success! Logging in...")
                st.rerun()
            else:
                st.error("❌ Invalid username or account password.")
                
    with tab2:
        st.markdown("<p style='color: gray;'>Choose a permanent nickname. You will only have to do this once.</p>", unsafe_allow_html=True)
        reg_name = st.text_input("Choose Nickname (No Spaces):", max_chars=15, key="reg_user")
        reg_pass = st.text_input("Create Account Password:", type="password", key="reg_password")
        invite_code = st.text_input("Enter School Invite Code:", type="password", help="Ask the chat owner for the registration password.")
        
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
                user_db[name_clean] = {
                    "password": hash_pass(reg_pass),
                    "role": "STUDENT"
                }
                save_user_database(user_db)
                st.success("🎉 Account created successfully! Switch to the 'Log In' tab to join the room.")
    st.stop()

# --- 🏫 MAIN CHATROOM AREA ---
st.markdown("<h2 style='color: white; margin-bottom: 0px;'>🏫 Live School Room</h2>", unsafe_allow_html=True)
role_label = "👑 OWNER" if st.session_state["is_owner"] else "STUDENT"
st.markdown(f"<p style='color: #888888; font-size: 14px;'>Active Session: <b style='color:#ffffff;'>{st.session_state['nickname']}</b> ({role_label})</p>", unsafe_allow_html=True)

# Render logs
chat_container = st.container(height=400, border=True)
with chat_container:
    for message in st.session_state["global_chat_history"]:
        tag = message.get("tag", "STUDENT")
        time_stamp = f"<span style='color:#6b7280; font-size:11px; margin-left:8px;'>{message['time']}</span>"
        if tag == "OWNER":
            st.markdown(f"<div><span class='owner-badge'>👑 OWNER</span> <b style='color:#ffffff;'>{message['user']}</b>{time_stamp}</div><div style='color: #f3f4f6; padding: 2px 0px 12px 0px;'>{message['content']}</div>", unsafe_allow_html=True)
        elif tag == "OWNER ALERT":
            st.markdown(f"<div class='alert-box'><span class='owner-badge'>🚨 ALERT</span> <b style='color:#ffffff;'>{message['user']}</b>{time_stamp}<br><div style='color:#ff4b4b; padding-top:4px; font-weight:500;'>{message['content']}</div></div>", unsafe_allow_html=True)
        elif tag == "SYSTEM":
            st.markdown(f"<div><span class='system-badge'>🤖 SYSTEM</span>{time_stamp}</div><div style='color: #9ca3af; font-style: italic; padding: 2px 0px 12px 0px;'>{message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div><span class='student-badge'>👤 STUDENT</span> <b style='color:#d1d5db;'>{message['user']}</b>{time_stamp}</div><div style='color: #e5e7eb; padding: 2px 0px 12px 0px;'>{message['content']}</div>", unsafe_allow_html=True)

# Process Message Submission
if raw_input := st.chat_input("Type a message or owner command..."):
    current_time = time.time()
    my_name = st.session_state["nickname"]
    
    if my_name in st.session_state["banned_users"]:
        st.error("You are permanently banned.")
        st.stop()
        
    if my_name in st.session_state["timeout_users"]:
        expiry = st.session_state["timeout_users"][my_name]
        if current_time < expiry:
            remaining_minutes = int((expiry - current_time) / 60) + 1
            st.error(f"You have been timed out by the owner. Remaining time: ~{remaining_minutes} minute(s).")
            st.stop()
        else:
            del st.session_state["timeout_users"][my_name]

    if raw_input.strip():
        command_text = raw_input.strip()
        
        # --- 👑 OWNER COMMAND ENGINE ---
        if st.session_state["is_owner"] and command_text.startswith("/"):
            if command_text == "/clear":
                st.session_state["global_chat_history"] = [{"user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": "The chat view was wiped by the Owner."}]
                st.rerun()
                
            elif command_text.startswith("/ban "):
                target = command_text.replace("/ban ", "").strip()
                if target and target != my_name:
                    st.session_state["banned_users"].append(target)
                    st.session_state["global_chat_history"] = [m for m in st.session_state["global_chat_history"] if m["user"] != target]
                    st.session_state["global_chat_history"].append({"user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": f"User '{target}' was permanently banned."})
                    st.rerun()
                    
            elif command_text.startswith("/timeout "):
                try:
                    parts = command_text.replace("/timeout ", "").split()
                    target_user = parts
                    duration_minutes = int(parts)
                    if target_user != my_name:
                        st.session_state["timeout_users"][target_user] = time.time() + (duration_minutes * 60)
st.session_state["global_chat_history"].append({"user": "System", "tag": "SYSTEM", "time": datetime.datetime.now().strftime("%H:%M"), "content": f"User '{target_user}' has been placed in timeout for {duration_minutes} minute(s)."})st.rerun()except:st.error("Error! Use syntax: /timeout [Username] [minutes]")st.stop()elif command_text.startswith("/alert "):alert_msg = command_text.replace("/alert ", "").strip()st.session_state["global_chat_history"].append({"user": my_name, "tag": "OWNER ALERT", "time": datetime.datetime.now().strftime("%H:%M"), "content": alert_msg.upper()})st.rerun()else:user_tag = "OWNER" if st.session_state["is_owner"] else "STUDENT"st.session_state["global_chat_history"].append({"user": my_name, "tag": user_tag,"time": datetime.datetime.now().strftime("%H:%M"),"content": clean_text(raw_input)})st.rerun()
