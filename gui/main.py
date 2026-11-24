import customtkinter as ctk
import tkinter as tk
import shutil
import subprocess
import os
from datetime import datetime
from tkinter import filedialog

# ==========================================================
# SAFESPACE - ROUNDED CYBERSECURITY INTERFACE
# ==========================================================

ctk.set_appearance_mode("dark")

# ---------------- COLORS ----------------

BG = "#0B1018"
SIDEBAR = "#101722"
CARD = "#171F2D"
CARD_ALT = "#1C2635"
BORDER = "#283549"

BLUE = "#5B91FF"
CYAN = "#42D5E8"
PURPLE = "#A58BFF"
GREEN = "#3DDBA0"
ORANGE = "#FFB45E"
RED = "#FF6174"

TEXT = "#EDF3FA"
MUTED = "#91A0B5"

# ---------------- TYPOGRAPHY ----------------

FONT = "Inter"
MONO = "IBM Plex Mono"

FONT_TITLE = (FONT, 23, "bold")
FONT_SECTION = (FONT, 15, "bold")
FONT_BODY = (FONT, 12)
FONT_SMALL = (FONT, 10)
FONT_STAT = (FONT, 29, "bold")
FONT_TECH = (MONO, 10)


class SafeSpaceApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("SafeSpace | Storage Intelligence")

        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        window_w = min(1200, screen_w - 100)
        window_h = min(800, screen_h - 100)

        self.geometry(f"{window_w}x{window_h}+70+35")
        self.minsize(850, 600)

        self.configure(fg_color=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.pages = [
            ("Dashboard", BLUE),
            ("Storage Analyzer", BLUE),
            ("Folder Analyzer", CYAN),
            ("Duplicate Detector", PURPLE),
            ("Activity Monitor", GREEN),
            ("Emergency Mode", RED),
            ("Recovery Vault", PURPLE),
            ("Cleanup Recommendations", ORANGE),
            ("Storage Reports", CYAN),
            ("Storage History", BLUE),
        ]

        self.nav_buttons = {}

        self.create_sidebar()
        self.create_workspace()
        self.open_page("Dashboard")

    # ==========================================================
    # SIDEBAR
    # ==========================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=205,
            fg_color=SIDEBAR,
            corner_radius=0
        )

        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        logo_frame.pack(fill="x", padx=17, pady=(25, 4))

        ctk.CTkLabel(
            logo_frame,
            text="⬡",
            font=(FONT, 30, "bold"),
            text_color=CYAN
        ).pack(side="left")

        ctk.CTkLabel(
            logo_frame,
            text="SafeSpace",
            font=(FONT, 20, "bold"),
            text_color=TEXT
        ).pack(side="left", padx=7)

        ctk.CTkLabel(
            self.sidebar,
            text="INTELLIGENT STORAGE GUARDIAN",
            font=(MONO, 8),
            text_color=MUTED
        ).pack(anchor="w", padx=22, pady=(0, 25))

        self.add_section("WORKSPACE")
        self.add_nav("Dashboard", "◈", BLUE)

        self.add_section("STORAGE INTELLIGENCE")
        self.add_nav("Storage Analyzer", "▤", BLUE)
        self.add_nav("Folder Analyzer", "▣", CYAN)
        self.add_nav("Duplicate Detector", "◉", PURPLE)

        self.add_section("MONITORING")
        self.add_nav("Activity Monitor", "⌁", GREEN)
        self.add_nav("Emergency Mode", "⚠", RED)

        self.add_section("FILE PROTECTION")
        self.add_nav("Recovery Vault", "⬡", PURPLE)
        self.add_nav("Cleanup Recommendations", "✦", ORANGE)

        self.add_section("REPORTING")
        self.add_nav("Storage Reports", "▧", CYAN)
        self.add_nav("Storage History", "↗", BLUE)

        # Bottom system status
        status_card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#172332",
            corner_radius=16,
            border_width=1,
            border_color="#26394A"
        )
        status_card.pack(side="bottom", fill="x", padx=12, pady=14)

        ctk.CTkLabel(
            status_card,
            text="●  SYSTEM ONLINE",
            font=(FONT, 11, "bold"),
            text_color=GREEN
        ).pack(anchor="w", padx=12, pady=(11, 3))

        ctk.CTkLabel(
            status_card,
            text="Storage monitoring ready",
            font=(FONT, 10),
            text_color=MUTED
        ).pack(anchor="w", padx=12, pady=(0, 11))

    def add_section(self, title):

        ctk.CTkLabel(
            self.sidebar,
            text=title,
            font=(MONO, 9, "bold"),
            text_color="#66768B"
        ).pack(anchor="w", padx=21, pady=(10, 5))

    def add_nav(self, name, icon, color):

        button = ctk.CTkButton(
            self.sidebar,
            text=f"{icon}   {name}",
            height=37,
            corner_radius=10,
            fg_color="transparent",
            hover_color="#202C3D",
            text_color="#A8B5C7",
            font=(FONT, 11),
            anchor="w",
            command=lambda: self.open_page(name)
        )

        button.pack(fill="x", padx=9, pady=2)

        self.nav_buttons[name] = {
            "button": button,
            "color": color
        }

    # ==========================================================
    # WORKSPACE
    # ==========================================================

    def create_workspace(self):

        self.workspace = ctk.CTkFrame(
            self,
            fg_color=BG,
            corner_radius=0
        )

        self.workspace.grid(row=0, column=1, sticky="nsew")
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(1, weight=1)

        # Top bar
        self.topbar = ctk.CTkFrame(
            self.workspace,
            fg_color=BG,
            height=62,
            corner_radius=0
        )

        self.topbar.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(12, 0)
        )
        self.topbar.grid_columnconfigure(0, weight=1)

        self.page_heading = ctk.CTkLabel(
            self.topbar,
            text="DASHBOARD",
            font=FONT_TITLE,
            text_color=TEXT
        )
        self.page_heading.grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.topbar,
            text="● SYSTEM ONLINE",
            text_color=GREEN,
            font=FONT_TECH
        ).grid(row=0, column=1, padx=10)

        self.time_label = ctk.CTkLabel(
            self.topbar,
            text=datetime.now().strftime("%d %b %Y"),
            text_color=MUTED,
            font=FONT_TECH
        )
        self.time_label.grid(row=0, column=2, padx=5)

        # Scrollable workspace
        self.content = ctk.CTkScrollableFrame(
            self.workspace,
            fg_color=BG,
            corner_radius=0,
            scrollbar_button_color="#34445B",
            scrollbar_button_hover_color=BLUE
        )

        self.content.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=13,
            pady=(5, 12)
        )

    # ==========================================================
    # NAVIGATION
    # ==========================================================

    def open_page(self, name):

        self.page_heading.configure(text=name.upper())

        for page, data in self.nav_buttons.items():

            if page == name:
                data["button"].configure(
                    fg_color="#1C2A3D",
                    text_color=data["color"]
                )
            else:
                data["button"].configure(
                    fg_color="transparent",
                    text_color="#A8B5C7"
                )

        # CORRECTED ROUTING
        if name == "Dashboard":
            self.show_dashboard()

        elif name == "Storage Analyzer":
            self.show_storage_analyzer()

        elif name == "Folder Analyzer":
           self.show_folder_analyzer()

        elif name == "Duplicate Detector":
            self.show_duplicate_detector()
 
        else:
            self.show_tool_page(name)

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================================================
    # DASHBOARD
    # ==========================================================

    def show_dashboard(self):

        self.clear_content()

        disk = shutil.disk_usage("/")

        total = disk.total / (1024 ** 3)
        used = disk.used / (1024 ** 3)
        free = disk.free / (1024 ** 3)

        percentage = (disk.used / disk.total) * 100

        if percentage < 70:
            health = 100
            health_status = "OPTIMAL"
            health_color = GREEN
        elif percentage < 85:
            health = 80
            health_status = "STABLE"
            health_color = CYAN
        elif percentage < 95:
            health = 60
            health_status = "WARNING"
            health_color = ORANGE
        else:
            health = 30
            health_status = "CRITICAL"
            health_color = RED

        # Intro
        ctk.CTkLabel(
            self.content,
            text="STORAGE INTELLIGENCE",
            font=FONT_TECH,
            text_color=CYAN
        ).pack(anchor="w", pady=(8, 4))

        ctk.CTkLabel(
            self.content,
            text="Your files. Your control.",
            font=(FONT, 25, "bold"),
            text_color=TEXT
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.content,
            text="Monitor storage health, analyze files and manage your storage environment.",
            font=FONT_BODY,
            text_color=MUTED
        ).pack(anchor="w", pady=(4, 18))

        # ---------------- STAT MODULES ----------------

        stats = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        stats.pack(fill="x", pady=(0, 12))

        for i in range(3):
            stats.grid_columnconfigure(i, weight=1, uniform="stats")

        self.create_stat(
            stats, 0,
            "STORAGE USED",
            f"{percentage:.1f}%",
            f"{used:.2f} GB occupied",
            BLUE,
            "#18263B"
        )

        self.create_stat(
            stats, 1,
            "STORAGE HEALTH",
            f"{health}/100",
            health_status,
            health_color,
            "#172D2A"
        )

        self.create_stat(
            stats, 2,
            "FREE CAPACITY",
            f"{free:.2f} GB",
            f"Out of {total:.1f} GB total",
            CYAN,
            "#172A35"
        )

        # ---------------- MAIN MODULES ----------------

        main_row = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        main_row.pack(fill="x", pady=4)

        main_row.grid_columnconfigure(0, weight=1, uniform="main")
        main_row.grid_columnconfigure(1, weight=1, uniform="main")

        # Storage visualization
        storage_card = self.create_card(main_row)
        storage_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        ctk.CTkLabel(
            storage_card,
            text="Storage Overview",
            font=FONT_SECTION,
            text_color=TEXT
        ).pack(anchor="w", padx=17, pady=(16, 3))

        ctk.CTkLabel(
            storage_card,
            text="SYSTEM DISK",
            font=FONT_TECH,
            text_color=MUTED
        ).pack(anchor="w", padx=17)

        ring = tk.Canvas(
            storage_card,
            width=190,
            height=190,
            bg=CARD,
            highlightthickness=0
        )
        ring.pack(pady=7)

        ring.create_oval(
            22, 22, 168, 168,
            outline="#29374B",
            width=18
        )

        ring.create_arc(
            22, 22, 168, 168,
            start=90,
            extent=-percentage * 3.6,
            style="arc",
            outline=BLUE,
            width=18
        )

        ring.create_text(
            95, 86,
            text=f"{percentage:.1f}%",
            fill=TEXT,
            font=(FONT, 23, "bold")
        )

        ring.create_text(
            95, 111,
            text="USED",
            fill=MUTED,
            font=(MONO, 10)
        )

        # Storage legend
        legend = ctk.CTkFrame(
            storage_card,
            fg_color="transparent"
        )
        legend.pack(fill="x", padx=17, pady=(4, 2))

        ctk.CTkLabel(
            legend,
            text="● USED",
            text_color=BLUE,
            font=FONT_TECH
        ).pack(side="left")

        ctk.CTkLabel(
            legend,
            text=f"{used:.2f} GB",
            text_color=TEXT,
            font=FONT_TECH
        ).pack(side="right")

        progress = ctk.CTkProgressBar(
            storage_card,
            height=9,
            corner_radius=10,
            progress_color=BLUE,
            fg_color="#29374B"
        )
        progress.pack(fill="x", padx=17, pady=7)
        progress.set(percentage / 100)

        legend2 = ctk.CTkFrame(
            storage_card,
            fg_color="transparent"
        )
        legend2.pack(fill="x", padx=17, pady=(2, 14))

        ctk.CTkLabel(
            legend2,
            text="● FREE",
            text_color=CYAN,
            font=FONT_TECH
        ).pack(side="left")

        ctk.CTkLabel(
            legend2,
            text=f"{free:.2f} GB",
            text_color=TEXT,
            font=FONT_TECH
        ).pack(side="right")

        # Health module
        health_card = self.create_card(main_row)
        health_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )

        ctk.CTkLabel(
            health_card,
            text="System Health",
            font=FONT_SECTION,
            text_color=TEXT
        ).pack(anchor="w", padx=17, pady=(16, 3))

        ctk.CTkLabel(
            health_card,
            text="CAPACITY CONDITION",
            font=FONT_TECH,
            text_color=MUTED
        ).pack(anchor="w", padx=17)

        health_visual = ctk.CTkFrame(
            health_card,
            fg_color="#172B29",
            corner_radius=22,
            width=150,
            height=150
        )
        health_visual.pack(pady=27)
        health_visual.pack_propagate(False)

        ctk.CTkLabel(
            health_visual,
            text=str(health),
            font=(FONT, 43, "bold"),
            text_color=health_color
        ).pack(pady=(29, 0))

        ctk.CTkLabel(
            health_visual,
            text="OUT OF 100",
            font=FONT_TECH,
            text_color=MUTED
        ).pack(pady=(0, 3))

        ctk.CTkLabel(
            health_card,
            text=health_status,
            font=(FONT, 12, "bold"),
            text_color=health_color
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            health_card,
            text="Based on system storage capacity",
            font=FONT_SMALL,
            text_color=MUTED
        ).pack(pady=(0, 18))

        # ---------------- LOWER MODULES ----------------

        lower_row = ctk.CTkFrame(
            self.content,
            fg_color="transparent"
        )
        lower_row.pack(fill="x", pady=(12, 4))

        lower_row.grid_columnconfigure(0, weight=1, uniform="lower")
        lower_row.grid_columnconfigure(1, weight=1, uniform="lower")

        # Activity module
        activity_card = self.create_card(lower_row)
        activity_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 6)
        )

        ctk.CTkLabel(
            activity_card,
            text="Activity Monitor",
            font=FONT_SECTION,
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(15, 3))

        ctk.CTkLabel(
            activity_card,
            text="STORAGE EVENTS",
            font=FONT_TECH,
            text_color=MUTED
        ).pack(anchor="w", padx=16, pady=(0, 8))

        self.create_event(
            activity_card,
            GREEN,
            "System initialized",
            "Storage information loaded"
        )

        self.create_event(
            activity_card,
            BLUE,
            "Disk usage analyzed",
            f"Current usage: {percentage:.1f}%"
        )

        self.create_event(
            activity_card,
            CYAN,
            "SafeSpace is ready",
            "Monitoring modules available"
        )

        # Quick tools module
        tools_card = self.create_card(lower_row)
        tools_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(6, 0)
        )

        ctk.CTkLabel(
            tools_card,
            text="Quick Access",
            font=FONT_SECTION,
            text_color=TEXT
        ).pack(anchor="w", padx=16, pady=(15, 3))

        ctk.CTkLabel(
            tools_card,
            text="STORAGE TOOLS",
            font=FONT_TECH,
            text_color=MUTED
        ).pack(anchor="w", padx=16, pady=(0, 8))

        self.create_operation(
            tools_card, "Storage Analyzer", BLUE, "Storage Analyzer"
        )

        self.create_operation(
            tools_card, "Duplicate Detection", PURPLE, "Duplicate Detector"
        )

        self.create_operation(
            tools_card, "Cleanup Recommendations", ORANGE, "Cleanup Recommendations"
        )

        self.create_operation(
            tools_card, "Emergency Mode", RED, "Emergency Mode"
        )

        # Footer
        footer = ctk.CTkFrame(
            self.content,
            fg_color="#131D29",
            corner_radius=14
        )
        footer.pack(fill="x", pady=(12, 6))

        ctk.CTkLabel(
            footer,
            text="◈  SAFESPACE STORAGE GUARDIAN",
            font=FONT_TECH,
            text_color=CYAN
        ).pack(side="left", padx=14, pady=11)

        ctk.CTkLabel(
            footer,
            text="SYSTEM OPERATIONAL",
            font=FONT_TECH,
            text_color=GREEN
        ).pack(side="right", padx=14)

    # ==========================================================
    # ROUNDED COMPONENTS
    # ==========================================================

    def create_card(self, parent):

        return ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=20,
            border_width=1,
            border_color=BORDER
        )

    def create_stat(
        self, parent, column, title, value, detail, color, card_color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color=card_color,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=4
        )

        ctk.CTkLabel(
            card,
            text=title,
            font=FONT_TECH,
            text_color=MUTED
        ).pack(anchor="w", padx=15, pady=(14, 5))

        ctk.CTkLabel(
            card,
            text=value,
            font=FONT_STAT,
            text_color=color
        ).pack(anchor="w", padx=15, pady=3)

        ctk.CTkLabel(
            card,
            text=detail,
            font=(MONO, 9),
            text_color=color
        ).pack(anchor="w", padx=15, pady=(2, 14))

    def create_event(self, parent, color, title, description):

        row = ctk.CTkFrame(
            parent,
            fg_color=CARD_ALT,
            corner_radius=12
        )
        row.pack(fill="x", padx=10, pady=4)

        ctk.CTkLabel(
            row,
            text="●",
            text_color=color,
            font=(FONT, 14)
        ).pack(side="left", padx=10, pady=8)

        text_frame = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )
        text_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            text_frame,
            text=title,
            text_color=TEXT,
            font=(FONT, 11, "bold")
        ).pack(anchor="w", pady=(6, 0))

        ctk.CTkLabel(
            text_frame,
            text=description,
            text_color=MUTED,
            font=(FONT, 10)
        ).pack(anchor="w", pady=(0, 6))

    def create_operation(self, parent, title, color, page):

        button = ctk.CTkButton(
            parent,
            text=f"   ◈   {title}",
            height=36,
            corner_radius=11,
            fg_color=CARD_ALT,
            hover_color="#2A374B",
            text_color=color,
            font=(FONT, 11, "bold"),
            anchor="w",
            command=lambda: self.open_page(page)
        )

        button.pack(fill="x", padx=10, pady=4)

    # ==========================================================
    # TOOL PAGES
    # ==========================================================

    def show_tool_page(self, name):

        self.clear_content()

        colors = dict(self.pages)
        color = colors.get(name, BLUE)

        panel = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        panel.pack(fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(
            panel,
            text="SAFESPACE MODULE",
            font=FONT_TECH,
            text_color=color
        ).pack(pady=(65, 8))

        ctk.CTkLabel(
            panel,
            text=name,
            font=(FONT, 27, "bold"),
            text_color=TEXT
        ).pack(pady=8)

        ctk.CTkLabel(
            panel,
            text="● MODULE READY",
            font=(MONO, 11, "bold"),
            text_color=GREEN
        ).pack(pady=5)

        ctk.CTkLabel(
            panel,
            text="This module will be connected to its corresponding backend.",
            font=FONT_BODY,
            text_color=MUTED
        ).pack(pady=8)

        ctk.CTkButton(
            panel,
            text="←  BACK TO DASHBOARD",
            height=42,
            corner_radius=14,
            fg_color=color,
            hover_color=color,
            text_color="#FFFFFF",
            font=(FONT, 12, "bold"),
            command=lambda: self.open_page("Dashboard")
        ).pack(pady=25)

    # ==========================================================
    # FOLDER ANALYZER
    # ==========================================================

    def show_folder_analyzer(self):

        self.clear_content()

        panel = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        panel.pack(fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(
            panel,
            text="FOLDER STORAGE ANALYSIS",
            font=FONT_TECH,
            text_color=CYAN
        ).pack(pady=(30, 8))

        ctk.CTkLabel(
            panel,
            text="Folder Analyzer",
            font=(FONT, 27, "bold"),
            text_color=TEXT
        ).pack(pady=8)

        ctk.CTkLabel(
            panel,
            text="Select a folder to analyze its files, subfolders and storage size.",
            font=FONT_BODY,
            text_color=MUTED
        ).pack(pady=5)

        # Selected folder display

        folder_label = ctk.CTkLabel(
            panel,
            text="No folder selected",
            font=FONT_TECH,
            text_color=MUTED,
            wraplength=650
        )

        folder_label.pack(pady=15)

        # Results box

        result_box = ctk.CTkTextbox(
            panel,
            width=700,
            height=250,
            corner_radius=16,
            fg_color=BG,
            text_color=CYAN,
            font=(MONO, 13),
            border_width=1,
            border_color=BORDER
        )

        result_box.pack(fill="x", padx=35, pady=15)

        result_box.insert(
            "1.0",
            "Select a folder to begin analysis."
        )

        result_box.configure(state="disabled")

        # Store selected folder

        selected_folder = {"path": ""}

        # --------------------------------------------------
        # SELECT FOLDER
        # --------------------------------------------------

        def select_folder():

            folder_path = filedialog.askdirectory(
                title="Select Folder to Analyze"
            )

            if folder_path:

                selected_folder["path"] = folder_path

                folder_label.configure(
                    text=folder_path,
                    text_color=CYAN
                )

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Folder selected successfully.\n\n"
                    "Click RUN FOLDER ANALYSIS to continue."
                )

                result_box.configure(state="disabled")

        # --------------------------------------------------
        # RUN FOLDER ANALYSIS
        # --------------------------------------------------

        def run_analysis():

            folder_path = selected_folder["path"]

            if not folder_path:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Please select a folder first."
                )

                result_box.configure(state="disabled")
                return

            result_box.configure(state="normal")
            result_box.delete("1.0", "end")

            result_box.insert(
                "1.0",
                "Analyzing selected folder...\nPlease wait."
            )

            result_box.configure(state="disabled")

            project_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

            try:

                result = subprocess.run(
                    [
                        "./backend/safespace",
                        "--folder",
                        folder_path
                    ],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                if result.returncode == 0:

                    result_box.insert(
                        "1.0",
                        result.stdout
                    )

                    if result.stderr:
                        result_box.insert(
                            "end",
                            "\nWarnings:\n" + result.stderr
                        )

                else:

                    result_box.insert(
                        "1.0",
                        "Folder analysis failed.\n\n"
                        + result.stderr
                        + result.stdout
                    )

                result_box.configure(state="disabled")

            except subprocess.TimeoutExpired:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Error: Folder analysis took too long."
                )

                result_box.configure(state="disabled")

            except Exception as error:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    f"Error: {error}"
                )

                result_box.configure(state="disabled")

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        ctk.CTkButton(
            panel,
            text="SELECT FOLDER",
            height=45,
            corner_radius=14,
            fg_color="#26374C",
            hover_color="#344A63",
            text_color=CYAN,
            font=(FONT, 12, "bold"),
            command=select_folder
        ).pack(pady=8)

        ctk.CTkButton(
            panel,
            text="RUN FOLDER ANALYSIS",
            height=48,
            corner_radius=14,
            fg_color=BLUE,
            hover_color="#4779D8",
            text_color="#FFFFFF",
            font=(FONT, 13, "bold"),
            command=run_analysis
        ).pack(pady=8)

        ctk.CTkButton(
            panel,
            text="←  BACK TO DASHBOARD",
            height=42,
            corner_radius=14,
            fg_color=CARD_ALT,
            hover_color=BORDER,
            text_color=TEXT,
            font=(FONT, 12, "bold"),
            command=lambda: self.open_page("Dashboard")
        ).pack(pady=(10, 25))
    # ==========================================================
    # STORAGE ANALYZER
    # ==========================================================

    def show_storage_analyzer(self):

        self.clear_content()

        panel = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        panel.pack(fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(
            panel,
            text="SYSTEM STORAGE ANALYSIS",
            font=FONT_TECH,
            text_color=CYAN
        ).pack(pady=(30, 8))

        ctk.CTkLabel(
            panel,
            text="Storage Analyzer",
            font=(FONT, 27, "bold"),
            text_color=TEXT
        ).pack(pady=8)

        ctk.CTkLabel(
            panel,
            text="Analyze real-time storage usage of your system.",
            font=FONT_BODY,
            text_color=MUTED
        ).pack(pady=5)

        result_box = ctk.CTkTextbox(
            panel,
            width=700,
            height=250,
            corner_radius=16,
            fg_color=BG,
            text_color=CYAN,
            font=(MONO, 13),
            border_width=1,
            border_color=BORDER
        )

        result_box.pack(fill="x", padx=35, pady=25)

        result_box.insert(
            "1.0",
            "Storage analysis results will appear here."
        )

        result_box.configure(state="disabled")

        # --------------------------------------------------
        # RUN STORAGE ANALYSIS
        # --------------------------------------------------

        def run_analysis():

            result_box.configure(state="normal")
            result_box.delete("1.0", "end")

            result_box.insert(
                "1.0",
                "Analyzing system storage...\n"
            )

            result_box.configure(state="disabled")

            project_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

            try:

                result = subprocess.run(
                    ["./backend/safespace", "--storage"],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=20
                )

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                if result.returncode == 0:

                    result_box.insert(
                        "1.0",
                        result.stdout
                    )

                    if result.stderr:
                        result_box.insert(
                            "end",
                            "\nWarnings:\n" + result.stderr
                        )

                else:

                    result_box.insert(
                        "1.0",
                        "Storage analysis failed.\n\n"
                        + result.stderr
                        + result.stdout
                    )

                result_box.configure(state="disabled")

            except subprocess.TimeoutExpired:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Error: Storage analysis took too long."
                )

                result_box.configure(state="disabled")

            except Exception as error:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    f"Error: {error}"
                )

                result_box.configure(state="disabled")

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        ctk.CTkButton(
            panel,
            text="RUN STORAGE ANALYSIS",
            height=48,
            corner_radius=14,
            fg_color=BLUE,
            hover_color="#4779D8",
            text_color="#FFFFFF",
            font=(FONT, 13, "bold"),
            command=run_analysis
        ).pack(pady=10)

        ctk.CTkButton(
            panel,
            text="←  BACK TO DASHBOARD",
            height=42,
            corner_radius=14,
            fg_color=CARD_ALT,
            hover_color=BORDER,
            text_color=TEXT,
            font=(FONT, 12, "bold"),
            command=lambda: self.open_page("Dashboard")
        ).pack(pady=(10, 25))

    # ==========================================================
    # DUPLICATE DETECTOR
    # ==========================================================

    def show_duplicate_detector(self):

        self.clear_content()

        panel = ctk.CTkFrame(
            self.content,
            fg_color=CARD,
            corner_radius=22,
            border_width=1,
            border_color=BORDER
        )

        panel.pack(fill="both", expand=True, padx=5, pady=10)

        ctk.CTkLabel(
            panel,
            text="DUPLICATE FILE DETECTION",
            font=FONT_TECH,
            text_color=PURPLE
        ).pack(pady=(30, 8))

        ctk.CTkLabel(
            panel,
            text="Duplicate Detector",
            font=(FONT, 27, "bold"),
            text_color=TEXT
        ).pack(pady=8)

        ctk.CTkLabel(
            panel,
            text="Find identical files and identify potential storage savings.",
            font=FONT_BODY,
            text_color=MUTED
        ).pack(pady=5)

        # Selected folder display

        folder_label = ctk.CTkLabel(
            panel,
            text="No folder selected",
            font=FONT_TECH,
            text_color=MUTED,
            wraplength=650
        )

        folder_label.pack(pady=15)

        # Results box

        result_box = ctk.CTkTextbox(
            panel,
            width=700,
            height=250,
            corner_radius=16,
            fg_color=BG,
            text_color=PURPLE,
            font=(MONO, 13),
            border_width=1,
            border_color=BORDER
        )

        result_box.pack(fill="x", padx=35, pady=15)

        result_box.insert(
            "1.0",
            "Select a folder to search for duplicate files."
        )

        result_box.configure(state="disabled")

        # Store selected folder

        selected_folder = {"path": ""}

        # --------------------------------------------------
        # SELECT FOLDER
        # --------------------------------------------------

        def select_folder():

            folder_path = filedialog.askdirectory(
                title="Select Folder for Duplicate Detection"
            )

            if folder_path:

                selected_folder["path"] = folder_path

                folder_label.configure(
                    text=folder_path,
                    text_color=PURPLE
                )

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Folder selected successfully.\n\n"
                    "Click SCAN DUPLICATES to begin."
                )

                result_box.configure(state="disabled")

        # --------------------------------------------------
        # RUN DUPLICATE SCAN
        # --------------------------------------------------

        def run_duplicate_scan():

            folder_path = selected_folder["path"]

            if not folder_path:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Please select a folder first."
                )

                result_box.configure(state="disabled")
                return

            result_box.configure(state="normal")
            result_box.delete("1.0", "end")

            result_box.insert(
                "1.0",
                "Scanning for duplicate files...\n"
                "Please wait."
            )

            result_box.configure(state="disabled")

            project_path = os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )

            try:

                result = subprocess.run(
                    [
                        "./backend/safespace",
                        "--duplicates",
                        folder_path
                    ],
                    cwd=project_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                if result.returncode == 0:

                    result_box.insert(
                        "1.0",
                        result.stdout
                    )

                    if result.stderr:
                        result_box.insert(
                            "end",
                            "\nWarnings:\n" + result.stderr
                        )

                else:

                    result_box.insert(
                        "1.0",
                        "Duplicate detection failed.\n\n"
                        + result.stderr
                        + result.stdout
                    )

                result_box.configure(state="disabled")

            except subprocess.TimeoutExpired:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    "Error: Duplicate scanning took too long."
                )

                result_box.configure(state="disabled")

            except Exception as error:

                result_box.configure(state="normal")
                result_box.delete("1.0", "end")

                result_box.insert(
                    "1.0",
                    f"Error: {error}"
                )

                result_box.configure(state="disabled")

        # --------------------------------------------------
        # BUTTONS
        # --------------------------------------------------

        ctk.CTkButton(
            panel,
            text="SELECT FOLDER",
            height=45,
            corner_radius=14,
            fg_color="#302747",
            hover_color="#453663",
            text_color=PURPLE,
            font=(FONT, 12, "bold"),
            command=select_folder
        ).pack(pady=8)

        ctk.CTkButton(
            panel,
            text="SCAN DUPLICATES",
            height=48,
            corner_radius=14,
            fg_color=PURPLE,
            hover_color="#8872DB",
            text_color="#FFFFFF",
            font=(FONT, 13, "bold"),
            command=run_duplicate_scan
        ).pack(pady=8)

        ctk.CTkButton(
            panel,
            text="←  BACK TO DASHBOARD",
            height=42,
            corner_radius=14,
            fg_color=CARD_ALT,
            hover_color=BORDER,
            text_color=TEXT,
            font=(FONT, 12, "bold"),
            command=lambda: self.open_page("Dashboard")
        ).pack(pady=(10, 25))


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    app = SafeSpaceApp()
    app.mainloop()
