# gui/screens/session_screen.py
import customtkinter as ctk
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.components.card import CustomCard

class SessionScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.init_ui()

    def init_ui(self):
        ctk.CTkLabel(self, text="Session Registration", font=(FONT_FAMILY, 24, "bold"), text_color=THEME_COLORS["text_main"]).pack(anchor="w", padx=30, pady=(30, 20))
        
        up_panel = ctk.CTkFrame(self, fg_color="transparent")
        up_panel.pack(fill="x", padx=25)
        
        btn_frame = ctk.CTkFrame(up_panel, fg_color="transparent")
        btn_frame.pack(fill="x")
        ctk.CTkButton(btn_frame, text="Upload PDF", fg_color=THEME_COLORS["btn_pdf_bg"], border_color=THEME_COLORS["btn_pdf_border"], border_width=1, hover_color=THEME_COLORS["btn_pdf_hover"], height=50).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(btn_frame, text="Upload TXT", fg_color=THEME_COLORS["bg_card"], border_color=THEME_COLORS["border"], border_width=1, height=50).pack(side="left", fill="x", expand=True)
        
        tr_panel = ctk.CTkFrame(self, fg_color="transparent")
        tr_panel.pack(fill="both", expand=True, padx=25, pady=20)
        
        opts = [("Enable attendance tracking", True), ("Enable focus tracking", True), ("Enable speaking detection", True)]
        for text, state in opts:
            row = CustomCard(tr_panel, corner_radius=8)
            row.pack(fill="x", pady=5)
            cb = ctk.CTkCheckBox(row, text=text, font=(FONT_FAMILY, 13, "bold"), fg_color=THEME_COLORS["primary"], text_color=THEME_COLORS["text_main"])
            if state: cb.select()
            cb.pack(anchor="w", padx=20, pady=15)
            
        bot = ctk.CTkFrame(self, fg_color="transparent")
        bot.pack(fill="x", padx=25, pady=20)
        ctk.CTkButton(bot, text="Confirm", fg_color=THEME_COLORS["primary"], font=(FONT_FAMILY, 14, "bold"), height=45).pack(side="right", fill="x", expand=True, padx=(10, 0))