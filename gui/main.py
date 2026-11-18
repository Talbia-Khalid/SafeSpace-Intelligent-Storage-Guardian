import customtkinter as ctk

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Create main application
app = ctk.CTk()

# Window settings
app.title("SafeSpace - Intelligent Storage Guardian")
app.geometry("1100x700")
app.minsize(900, 600)

# Main heading
title = ctk.CTkLabel(
    app,
    text="SafeSpace",
    font=("Arial", 32, "bold")
)

title.pack(pady=(40, 10))

subtitle = ctk.CTkLabel(
    app,
    text="Intelligent Storage Guardian",
    font=("Arial", 16)
)

subtitle.pack(pady=5)

# Welcome message
welcome = ctk.CTkLabel(
    app,
    text="Monitor, analyze and protect your storage.",
    font=("Arial", 18)
)

welcome.pack(pady=30)

# Start application
app.mainloop()
