import customtkinter as ctk
from tkinter import ttk


class Dashboard(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("AI Face Attendance System")

        self.geometry("1400x800")

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("blue")

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
        )

        self.sidebar.pack(side="left", fill="y")

        title = ctk.CTkLabel(
            self.sidebar,
            text="AI Attendance",
            font=("Poppins", 30, "bold"),
        )

        title.pack(pady=30)

        self.counter = ctk.CTkLabel(
            self.sidebar,
            text="0",
            font=("Poppins", 40, "bold"),
        )

        self.counter.pack(pady=20)

        # Main Frame
        self.main_frame = ctk.CTkFrame(self)

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True,
        )

        self.video_label = ctk.CTkLabel(
            self.main_frame,
            text="",
        )

        self.video_label.pack(pady=20)

        # Attendance Table
        self.tree = ttk.Treeview(
            self.main_frame,
            columns=(
                "Name",
                "Emotion",
                "Date",
                "Time",
            ),
            show="headings",
            height=12,
        )

        self.tree.heading("Name", text="Name")

        self.tree.heading("Emotion", text="Emotion")

        self.tree.heading("Date", text="Date")

        self.tree.heading("Time", text="Time")

        self.tree.pack(fill="x", padx=20)