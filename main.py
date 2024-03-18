import streamlit as stm
from PIL import Image
from editor import *
from viewer import *
im = Image.open(r"C:\Users\srija\OneDrive\Desktop\logo.png")
img = Image.open(r"C:\Users\srija\OneDrive\Desktop\Hyundai_verna_020.jpg")
imag = Image.open(r"C:\Users\srija\OneDrive\Desktop\download.png")
stm.set_page_config(
    page_title="Hyundai Motor India Limited",
    page_icon=im,
    layout="wide",
)

stm.title('Hyundai Motor India Limited (HMIL)')
stm.markdown('<style>h1{color: black; text-align: center;}</style>', unsafe_allow_html=True)
stm.subheader("RED FLAG / AUDIT EXCEPTIONS")
stm.markdown('<style>h3{color: BLACK; text-align: center;}</style>', unsafe_allow_html=True)
stm.image(imag, width=150) 
stm.image(img)

username = stm.text_input("Username")
password = stm.text_input("Password", type="password")

if stm.button("Login"):
    if username == "viewer" and password == "viewer_password":
        stm.session_state.login_status = "viewer"
    elif username == "editor" and password == "editor_password":
        stm.session_state.login_status = "editor"
    else:
        stm.error("Invalid username or password. Please try again.")

login_status = stm.session_state.get("login_status", False)

if login_status == "viewer":
    editor = Editor()
    viewer = Viewer(editor)
    viewer.display_entries()
elif login_status == "editor":
    # Instantiate Editor and run main function
    editor = Editor()
    editor.main()
    entries = editor.session_state.entries
    viewer = Viewer(entries)
    viewer.display_entries()