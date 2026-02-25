import streamlit as st
import requests
import datetime

BASE_URL = "http://localhost:8000"  # Backend endpoint


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="🌍",
    layout="centered"
)


# ---------------- BASIC STYLES ----------------
st.markdown(
    """
    <style>
    body {
        background-color: #f4f9ff;
    }

    .card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }

    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}   # Stores users: {username: password}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# ---------------- NAVIGATION ----------------
def go_to(page):
    st.session_state.page = page


# ---------------- REGISTER PAGE ----------------
def register_page():

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📝 Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):

        if not username or not password or not confirm_password:
            st.warning("⚠️ All fields are required")

        elif password != confirm_password:
            st.error("❌ Passwords do not match")

        elif username in st.session_state.users:
            st.error("❌ Username already exists")

        else:
            st.session_state.users[username] = password
            st.success("✅ Registration successful")
            st.info("Please login now")
            go_to("login")

    if st.button("Go to Login"):
        go_to("login")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- LOGIN PAGE ----------------
def login_page():

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if not username or not password:
            st.warning("⚠️ Enter username and password")

        elif username not in st.session_state.users:
            st.error("❌ User not found")

        elif st.session_state.users[username] != password:
            st.error("❌ Invalid password")

        else:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.success("✅ Login successful")
            go_to("trip")

    if st.button("Go to Register"):
        go_to("register")

    st.markdown("</div>", unsafe_allow_html=True)


# ---------------- TRIP PLANNER PAGE ----------------
def trip_planner_page():

    st.title("🌍 AI Travel Planner")

    st.caption(f"Welcome, {st.session_state.current_user} 👋")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        go_to("login")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("✈️ Plan Your Trip")

    with st.form(key="trip_form", clear_on_submit=True):

        user_input = st.text_input(
            "Trip Request",
            placeholder="e.g. Plan a trip to Goa for 5 days with ₹50,000 budget"
        )

        submit_button = st.form_submit_button("Generate Plan")

    st.markdown("</div>", unsafe_allow_html=True)


    # ---------------- RESPONSE ----------------
    if submit_button and user_input.strip():

        try:
            with st.spinner("🤖 Planning your trip..."):

                payload = {"question": user_input}

                response = requests.post(
                    f"{BASE_URL}/query",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:

                answer = response.json().get("answer", "No answer returned.")

                st.markdown("<div class='card'>", unsafe_allow_html=True)

                st.markdown(
                    f"""
                    ## 🌍 Your Travel Plan

                    **Generated on:** {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}

                    ---

                    {answer}

                    ---

                    ⚠️ *AI-generated content. Verify details before booking.*
                    """
                )

                st.markdown("</div>", unsafe_allow_html=True)

            else:
                st.error("❌ Bot failed: " + response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# ---------------- MAIN ROUTER ----------------
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "register":
    register_page()

elif st.session_state.page == "trip":

    if st.session_state.logged_in:
        trip_planner_page()
    else:
        go_to("login")