# gui/components/sidebar.py
import os
import customtkinter as ctk
from PIL import Image
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.constants import TEXT_ICONS, IMAGE_ASSETS # Import hằng số doanh nghiệp

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, on_menu_select):
        super().__init__(
            parent, 
            fg_color=THEME_COLORS["bg_sidebar"], 
            border_color=THEME_COLORS["border"],
            border_width=1,
            corner_radius=0
        )
        self.on_menu_select = on_menu_select
        self.buttons = {}
        self.current_active = None
        self.init_ui()

    def _load_icon(self, filename, fallback_text):
        try:
            path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "icons", filename)
            return ctk.CTkImage(light_image=Image.open(path), size=(20, 20)), ""
        except:
            return None, f"{fallback_text}  "

    def init_ui(self):
        # Logo Section
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(pady=(30, 25), padx=20, fill="x")
        
        ctk.CTkLabel(
            logo_frame, text="Smart Classroom", 
            font=(FONT_FAMILY, 18, "bold"), text_color=THEME_COLORS["text_main"], justify="left"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            logo_frame, text="AI Engine v2.0", 
            font=(FONT_FAMILY, 12), text_color=THEME_COLORS["primary"], justify="left"
        ).pack(anchor="w", pady=(0, 10))

        # Menu Items - Gọi dữ liệu từ IMAGE_ASSETS và TEXT_ICONS
        menu_items = [
            ("overview", "Dashboard", IMAGE_ASSETS["icon_dashboard"], TEXT_ICONS["dashboard_fallback"]),
            ("enrollment", "Enrollment", IMAGE_ASSETS["icon_enrollment"], TEXT_ICONS["enrollment_fallback"]),
            ("session", "Session Setup", IMAGE_ASSETS["icon_session"], TEXT_ICONS["session_fallback"]),
            ("lecture", "Live Lecture", IMAGE_ASSETS["icon_lecture"], TEXT_ICONS["lecture_fallback"]),
            ("account", "Account", IMAGE_ASSETS["icon_account"], TEXT_ICONS["account_fallback"])
        ]
        
        for screen_id, text, icon_file, fallback in menu_items:
            img, prefix = self._load_icon(icon_file, fallback)
            btn = ctk.CTkButton(
                self, text=f"{prefix}{text}", image=img, font=(FONT_FAMILY, 14), anchor="w", height=45,
                fg_color="transparent", text_color=THEME_COLORS["text_muted"],
                hover_color=THEME_COLORS["bg_card_hover"], corner_radius=8,
                command=lambda sid=screen_id: self.handle_click(sid)
            )
            btn.pack(fill="x", padx=15, pady=4)
            self.buttons[screen_id] = btn

        # Footer User Profile
        footer_frame = ctk.CTkFrame(self, fg_color=THEME_COLORS["bg_card"], corner_radius=12)
        footer_frame.pack(side="bottom", fill="x", pady=25, padx=15)
        
        user_avatar = ctk.CTkLabel(
            footer_frame, text="AI", font=(FONT_FAMILY, 14, "bold"), 
            text_color="#FFFFFF", fg_color=THEME_COLORS["primary"], 
            width=38, height=38, corner_radius=19
        )
        user_avatar.pack(side="left", padx=12, pady=12)
        
        info_text = ctk.CTkLabel(
            footer_frame, text="Admin User\nadmin@hcmute.edu", 
            font=(FONT_FAMILY, 11), text_color=THEME_COLORS["text_muted"], justify="left"
        )
        info_text.pack(side="left", pady=12)

    def handle_click(self, screen_id):
        if self.current_active == screen_id:
            return
            
        self.current_active = screen_id
        for sid, btn in self.buttons.items():
            if sid == screen_id:
                btn.configure(fg_color=THEME_COLORS["bg_card_hover"], text_color=THEME_COLORS["text_main"])
            else:
                btn.configure(fg_color="transparent", text_color=THEME_COLORS["text_muted"])
                
        self.on_menu_select(screen_id)