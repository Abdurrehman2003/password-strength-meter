import re
import random
import string
import streamlit as st
from typing import Tuple, List

# Constants
COMMON_PASSWORDS = ["password", "123456", "qwerty", "abc123", "password123"]
SPECIAL_CHARS = "!@#$%^&*"
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 20
DEFAULT_PASSWORD_LENGTH = 12

# Utility Functions
def generate_strong_password(length: int = DEFAULT_PASSWORD_LENGTH) -> str:
    """Generate a strong password with a mix of letters, numbers, and special characters."""
    characters = string.ascii_letters + string.digits + SPECIAL_CHARS
    return ''.join(random.choice(characters) for _ in range(length))

def check_password_strength(password: str) -> Tuple[str, int, List[str]]:
    """Evaluate the strength of a password and provide feedback."""
    score = 0
    feedback = []

    # Check for common passwords
    if password.lower() in COMMON_PASSWORDS:
        return "❌ This password is too common. Choose a unique one.", 0, feedback

    # Length Check
    if len(password) >= MIN_PASSWORD_LENGTH:
        score += 1
    else:
        feedback.append("🔴 Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("🔤 Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("🔢 Add at least one number (0-9).")

    # Special Character Check
    if re.search(f"[{re.escape(SPECIAL_CHARS)}]", password):
        score += 1
    else:
        feedback.append(f"✨ Include at least one special character ({SPECIAL_CHARS}).")

    # Strength Rating
    if score == 4:
        return "✅ Strong Password!", score, feedback
    elif score == 3:
        return "🟡 Moderate Password", score, feedback
    else:
        return "🔴 Weak Password", score, feedback

# Streamlit App Configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔑",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Styling
st.markdown("""
    <style>
        .main {
            background-color: #f5f5f5;
            padding: 2rem;
        }
        .stTextInput > div > div > input {
            border-radius: 10px;
            padding: 10px;
        }
        .stButton > button {
            border-radius: 8px;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #333333;
        }
        .stMarkdown h4 {
            color: #555555;
        }
        .stAlert {
            border-radius: 10px;
        }
        .stSuccess {
            background-color: #d4edda;
            color: #155724;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# App Layout
st.title("🔒 Password Strength Meter")
st.markdown("""
    <h4 style='color: #555555;'>
        🔑 Type your password below to analyze its strength:
    </h4>
""", unsafe_allow_html=True)

# Password Input and Strength Check
password = st.text_input("Enter Password:", type="password", placeholder="Type your password here...")

if st.button("🔍 Check Strength", key="check_strength_btn"):
    if password:
        result, score, suggestions = check_password_strength(password)
        
        # Display Password Length
        st.write(f"**Password Length:** {len(password)} characters")
        
        # Display Strength Result with Styling
        if "Strong" in result:
            st.markdown(f"""
                <div style='background-color: #d4edda; padding: 10px; border-radius: 10px;'>
                    <font size='4'>**{result}**</font>
                </div>
            """, unsafe_allow_html=True)
        elif "Moderate" in result:
            st.markdown(f"""
                <div style='background-color: #fff3cd; padding: 10px; border-radius: 10px;'>
                    <font size='4'>**{result}**</font>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color: #f8d7da; padding: 10px; border-radius: 10px;'>
                    <font size='4'>**{result}**</font>
                </div>
            """, unsafe_allow_html=True)
        
        # Display Improvement Suggestions
        if score < 4:
            st.markdown("### 💡 **Suggestions to Improve Your Password:**")
            for tip in suggestions:
                st.markdown(f"- {tip}")
    else:
        st.warning("⚠️ Please enter a password to check its strength.")

# Password Generator Section
st.markdown("---")
st.subheader("🔑 Need a Strong Password? Click Below!")
password_length = st.slider(
    "Choose password length:",
    min_value=MIN_PASSWORD_LENGTH,
    max_value=MAX_PASSWORD_LENGTH,
    value=DEFAULT_PASSWORD_LENGTH
)

if st.button("🔒 Generate Strong Password", key="generate_btn"):
    strong_password = generate_strong_password(password_length)
    st.markdown(f"""
        <div class='stSuccess'>
            <strong>Generated Password:</strong> {strong_password}
        </div>
    """, unsafe_allow_html=True)