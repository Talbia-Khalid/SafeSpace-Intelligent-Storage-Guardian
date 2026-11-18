import customtkinter as ctk
import shutil

# ================= SETTINGS =================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("SafeSpace - Intelligent Storage Guardian")
app.geometry("1200x750")
app.minsize(1000, 650)

app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

# ================= SIDEBAR =================

sidebar = ctk.CTkFrame(app, width=220, corner_radius=0)
sidebar.grid(row=0, column=0, sticky="ns")
sidebar.grid_propagate(False)

logo = ctk.CTkLabel(
    sidebar,
    text="SafeSpace",
    font=("Arial", 28, "bold")
)
logo.pack(pady=(30, 5))

subtitle = ctk.CTkLabel(
    sidebar,
    text="Intelligent Storage Guardian",
    font=("Arial", 12)
)
subtitle.pack(pady=(0, 30))

nav_title = ctk.CTkLabel(
    sidebar,
    text="NAVIGATION",
    font=("Arial", 13, "bold")
)
nav_title.pack(pady=10)

# ================= MAIN CONTENT =================

content = ctk.CTkFrame(app, corner_radius=0)
content.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

content.grid_columnconfigure(0, weight=1)

# ================= PAGE FUNCTIONS =================

def clear_content():
    for widget in content.winfo_children():
        widget.destroy()


def show_dashboard():

    clear_content()

    # Get system storage information
    disk = shutil.disk_usage("/")

    total_gb = disk.total / (1024 ** 3)
    used_gb = disk.used / (1024 ** 3)
    free_gb = disk.free / (1024 ** 3)

    usage_percentage = (disk.used / disk.total) * 100

    # Calculate storage health score
    if usage_percentage < 70:
        health_score = 100
        health_status = "GOOD"
    elif usage_percentage < 85:
        health_score = 80
        health_status = "MODERATE"
    elif usage_percentage < 95:
        health_score = 60
        health_status = "HIGH STORAGE USAGE"
    else:
        health_score = 30
        health_status = "CRITICAL"

    # Dashboard heading
    heading = ctk.CTkLabel(
        content,
        text="Dashboard",
        font=("Arial", 28, "bold")
    )
    heading.pack(anchor="w", padx=30, pady=(30, 5))

    welcome = ctk.CTkLabel(
        content,
        text="Monitor and manage your storage from one place.",
        font=("Arial", 14)
    )
    welcome.pack(anchor="w", padx=30, pady=(0, 25))

    # Storage cards
    cards_frame = ctk.CTkFrame(content, fg_color="transparent")
    cards_frame.pack(fill="x", padx=25)

    cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

    card_names = [
        ("Total Storage", f"{total_gb:.2f} GB"),
        ("Used Storage", f"{used_gb:.2f} GB"),
        ("Available Storage", f"{free_gb:.2f} GB")
    ]

    for index, (name, value) in enumerate(card_names):

        card = ctk.CTkFrame(cards_frame, height=130)
        card.grid(row=0, column=index, padx=8, sticky="ew")
        card.grid_propagate(False)

        ctk.CTkLabel(
            card,
            text=name,
            font=("Arial", 15)
        ).pack(pady=(20, 8))

        ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 26, "bold")
        ).pack()

    # Storage health section
    health = ctk.CTkFrame(content)
    health.pack(fill="x", padx=33, pady=30)

    ctk.CTkLabel(
        health,
        text="Storage Health",
        font=("Arial", 20, "bold")
    ).pack(anchor="w", padx=20, pady=(20, 10))

    ctk.CTkLabel(
        health,
        text=f"Health Score: {health_score} / 100",
        font=("Arial", 18)
    ).pack(anchor="w", padx=20, pady=5)

    ctk.CTkLabel(
        health,
        text=f"Status: {health_status}",
        font=("Arial", 14)
    ).pack(anchor="w", padx=20, pady=5)

    # Storage usage percentage
    ctk.CTkLabel(
        health,
        text=f"Storage Used: {usage_percentage:.2f}%",
        font=("Arial", 14)
    ).pack(anchor="w", padx=20, pady=(10, 5))

    progress = ctk.CTkProgressBar(
        health,
        width=500
    )

    progress.pack(anchor="w", padx=20, pady=(5, 20))

    progress.set(usage_percentage / 100)


def show_page(page_name):

    if page_name == "Dashboard":
        show_dashboard()
        return

    clear_content()

    heading = ctk.CTkLabel(
        content,
        text=page_name,
        font=("Arial", 28, "bold")
    )
    heading.pack(anchor="w", padx=30, pady=(30, 10))

    description = ctk.CTkLabel(
        content,
        text=f"Welcome to the {page_name} section.",
        font=("Arial", 16)
    )
    description.pack(anchor="w", padx=30, pady=5)

    feature_frame = ctk.CTkFrame(content)
    feature_frame.pack(fill="x", padx=30, pady=30)

    ctk.CTkLabel(
        feature_frame,
        text=page_name,
        font=("Arial", 20, "bold")
    ).pack(anchor="w", padx=20, pady=(20, 10))

    ctk.CTkLabel(
        feature_frame,
        text="This feature will be connected to the SafeSpace backend.",
        font=("Arial", 14)
    ).pack(anchor="w", padx=20, pady=10)

    ctk.CTkLabel(
        feature_frame,
        text="Feature setup and integration will be added in upcoming stages.",
        font=("Arial", 13)
    ).pack(anchor="w", padx=20, pady=(5, 20))

# ================= NAVIGATION BUTTONS =================

pages = [
    "Dashboard",
    "Storage Analyzer",
    "Folder Analyzer",
    "Duplicate Detector",
    "Activity Monitor",
    "Cleanup Recommendations",
    "Emergency Mode",
    "Recovery Vault",
    "Storage Reports",
    "Storage History"
]

nav_buttons = []

def select_page(page_name):

    show_page(page_name)

    for button in nav_buttons:

        if button.cget("text") == page_name:
            button.configure(fg_color="#144870")
        else:
            button.configure(fg_color="#1F6AA5")

for page in pages:

    button = ctk.CTkButton(
        sidebar,
        text=page,
        height=38,
        corner_radius=8,
        anchor="w",
        fg_color="#1F6AA5",
        command=lambda name=page: select_page(name)
    )

    button.pack(fill="x", padx=15, pady=4)

    nav_buttons.append(button)

# ================= FOOTER =================

footer = ctk.CTkLabel(
    sidebar,
    text="SafeSpace v1.0",
    font=("Arial", 11)
)
footer.pack(side="bottom", pady=20)

# Open dashboard initially
select_page("Dashboard")

# Run application
app.mainloop()
