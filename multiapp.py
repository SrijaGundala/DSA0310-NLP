import streamlit as stm

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, name, func):
        self.apps.append((name, func))

    def run(self):
        app = stm.sidebar.radio(
            "Navigation",
            [name for name, _ in self.apps]
        )
        for name, func in self.apps:
            if app == name:
                func()
