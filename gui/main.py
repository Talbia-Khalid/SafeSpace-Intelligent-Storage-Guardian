
import customtkinter as ctk

# Appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Main window
app = ctk.CTk()
app.title("SafeSpace - Intelligent Storage Guardian")
app.geometry("1200x750")
app.minsize(1000, 650)

# Main layout
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

logo_subtitle = ctk.CTkLabel(
    sidebar,
    text="Intelligent Storage Guardian",
    font=("Arial", 12)
)
logo_subtitle.pack(pady=(0, 30))

# ================= MAIN CONTENT =================

content = ctk.CTkFrame(app, corner_radius=0)
content.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)

content.grid_columnconfigure(0, weight=1)

# Dashboard heading
heading = ctk.CTkLabel(
    content,
    text="Dashboard",
    font=("Arial", 28, "bold")
)
heading.grid(row=0, column=0, sticky="w", padx=30, pady=(30, 5))

welcome = ctk.CTkLabel(
    content,
    text="Monitor and manage your storage from one place.",
    font=("Arial", 14)
)
welcome.grid(row=1, column=0, sticky="w", padx=30, pady=(0, 25))

# ================= STORAGE CARDS =================

cards_frame = ctk.CTkFrame(content, fg_color="transparent")
cards_frame.grid(row=2, column=0, sticky="ew", padx=25)

cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

# Card 1
total_card = ctk.CTkFrame(cards_frame, height=130)
total_card.grid(row=0, column=0, padx=8, sticky="ew")
total_card.grid_propagate(False)

ctk.CTkLabel(
    total_card,
    text="Total Storage",
    font=("Arial", 15)
).pack(pady=(20, 8))

ctk.CTkLabel(
    total_card,
    text="-- GB",
    font=("Arial", 26, "bold")
).pack()

# Card 2
used_card = ctk.CTkFrame(cards_frame, height=130)
used_card.grid(row=0, column=1, padx=8, sticky="ew")
used_card.grid_propagate(False)

ctk.CTkLabel(
    used_card,
    text="Used Storage",
    font=("Arial", 15)
).pack(pady=(20, 8))

ctk.CTkLabel(
    used_card,
    text="-- GB",
    font=("Arial", 26, "bold")
).pack()

# Card 3
free_card = ctk.CTkFrame(cards_frame, height=130)
free_card.grid(row=0, column=2, padx=8, sticky="ew")
free_card.grid_propagate(False)

ctk.CTkLabel(
    free_card,
    text="Available Storage",
    font=("Arial", 15)
).pack(pady=(20, 8))

ctk.CTkLabel(
    free_card,
    text="-- GB",
    font=("Arial", 26, "bold")
).pack()

# ================= HEALTH SECTION =================

health_frame = ctk.CTkFrame(content)
health_frame.grid(row=3, column=0, sticky="ew", padx=33, pady=30)

ctk.CTkLabel(
    health_frame,
    text="Storage Health",
    font=("Arial", 20, "bold")
).pack(anchor="w", padx=20, pady=(20, 10))

ctk.CTkLabel(
    health_frame,
    text="Health Score: -- / 100",
    font=("Arial", 18)
).pack(anchor="w", padx=20, pady=5)

ctk.CTkLabel(
    health_frame,
    text="Status: Waiting for storage analysis",
    font=("Arial", 14)
).pack(anchor="w", padx=20, pady=(5, 20))

# ================= NAVIGATION =================

navigation_title = ctk.CTkLabel(
    sidebar,
    text="NAVIGATION",
    font=("Arial", 13, "bold")
)
navigation_title.pack(pady=(10, 10))

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

def open_page(page_name):
    heading.configure(text=page_name)
    welcome.configure(text=f"{page_name} section of SafeSpace")

    if page_name == "Dashboard":
        welcome.configure(
            text="Monitor and manage your storage from one place."
        )

for page in pages:

    button = ctk.CTkButton(
        sidebar,
        text=page,
        height=38,
        corner_radius=8,
        anchor="w",
        command=lambda name=page: open_page(name)
    )

    button.pack(fill="x", padx=15, pady=4)

# Footer
footer = ctk.CTkLabel(
    sidebar,
    text="SafeSpace v1.0",
    font=("Arial", 11)
)
footer.pack(side="bottom", pady=20)

# Run
app.mainloop()

