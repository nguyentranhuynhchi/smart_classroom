# gui/screens/account_screen.py
import customtkinter as ctk
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.components.card import CustomCard

class AccountScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.init_ui()

    def init_ui(self):
        # Card sẽ tự co giãn ôm lấy nội dung nhờ pack và padding
        card = CustomCard(self)
        card.place(relx=0.5, rely=0.5, anchor="center")
        
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=50, pady=50) # Tạo không gian thở cho form
        
        ctk.CTkLabel(inner, text="Account", font=(FONT_FAMILY, 24, "bold"), text_color=THEME_COLORS["text_main"]).pack()
        ctk.CTkLabel(inner, text="Manage your classroom account", font=(FONT_FAMILY, 12), text_color=THEME_COLORS["text_muted"]).pack(pady=(5, 30))
        
        # Tabs
        tab_frame = ctk.CTkFrame(inner, fg_color=THEME_COLORS["bg_dark"], corner_radius=8)
        tab_frame.pack(fill="x", pady=(0, 20))
        ctk.CTkButton(tab_frame, text="Login", fg_color=THEME_COLORS["primary"], corner_radius=8, width=100).pack(side="left", expand=True, fill="both", padx=2, pady=2)
        ctk.CTkButton(tab_frame, text="Register", fg_color="transparent", text_color=THEME_COLORS["text_muted"], width=100).pack(side="left", expand=True, fill="both")

        # Form
        ctk.CTkLabel(inner, text="Username", font=(FONT_FAMILY, 12), text_color=THEME_COLORS["text_muted"]).pack(anchor="w")
        ctk.CTkEntry(inner, placeholder_text="Enter username", fg_color=THEME_COLORS["bg_dark"], border_color=THEME_COLORS["border"], height=40).pack(fill="x", pady=(5, 15))
        
        ctk.CTkLabel(inner, text="Password", font=(FONT_FAMILY, 12), text_color=THEME_COLORS["text_muted"]).pack(anchor="w")
        ctk.CTkEntry(inner, placeholder_text="Enter password", show="*", fg_color=THEME_COLORS["bg_dark"], border_color=THEME_COLORS["border"], height=40).pack(fill="x", pady=(5, 15))
        
        bot_form = ctk.CTkFrame(inner, fg_color="transparent")
        bot_form.pack(fill="x", pady=(0, 25))
        ctk.CTkCheckBox(bot_form, text="Remember me", font=(FONT_FAMILY, 11), fg_color=THEME_COLORS["primary"]).pack(side="left")
        ctk.CTkLabel(bot_form, text="Forgot password?", font=(FONT_FAMILY, 11), text_color=THEME_COLORS["primary_light"], cursor="hand2").pack(side="right")
        
        ctk.CTkButton(inner, text="Login", font=(FONT_FAMILY, 14, "bold"), fg_color=THEME_COLORS["primary"], height=45).pack(fill="x")