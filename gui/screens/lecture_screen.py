# gui/screens/lecture_screen.py
import customtkinter as ctk
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.constants import TEXT_ICONS # Import hằng số doanh nghiệp

class LectureScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.init_ui()

    def init_ui(self):
        # Top Bar
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.pack(fill="x", padx=35, pady=(30, 15))
        
        status_box = ctk.CTkFrame(header, fg_color=THEME_COLORS["record_bg"], corner_radius=8)
        status_box.pack(side="left")
        
        # Gọi TEXT_ICONS["record_dot"] 
        ctk.CTkLabel(status_box, text=f"{TEXT_ICONS['record_dot']} REC", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["danger"]).pack(padx=20, pady=10)
        
        ai_box = ctk.CTkFrame(header, fg_color=THEME_COLORS["ai_active_bg"], corner_radius=8)
        ai_box.pack(side="left", padx=15)
        
        # Gọi TEXT_ICONS["ai_lightning"] 
        ctk.CTkLabel(ai_box, text=f"{TEXT_ICONS['ai_lightning']} AI ACTIVE", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["primary_light"]).pack(padx=20, pady=10)

        # Layout chính (Video feed 70% - Data 30%)
        main_grid = ctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        main_grid.grid_columnconfigure(0, weight=7, uniform="grid") 
        main_grid.grid_columnconfigure(1, weight=3, uniform="grid") 
        
        # Camera Feed
        cam_panel = ctk.CTkFrame(main_grid, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        cam_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        cam_view = ctk.CTkFrame(cam_panel, fg_color=THEME_COLORS["black"], corner_radius=8)
        cam_view.pack(fill="both", expand=True, padx=15, pady=15)
        ctk.CTkLabel(cam_view, text="Live Classroom Feed", font=(FONT_FAMILY, 20), text_color=THEME_COLORS["border"]).place(relx=0.5, rely=0.5, anchor="center")
        
        # Right Side Data Panel
        right_panel = ctk.CTkFrame(main_grid, fg_color="transparent")
        right_panel.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        
        att_panel = ctk.CTkFrame(right_panel, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        att_panel.pack(fill="both", expand=True, pady=(0, 15))
        ctk.CTkLabel(att_panel, text="LIVE ATTENDANCE", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=25, pady=20)
        
        event_panel = ctk.CTkFrame(right_panel, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"], height=280)
        event_panel.pack(fill="x")
        event_panel.pack_propagate(False) 
        ctk.CTkLabel(event_panel, text="SYSTEM LOGS", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=25, pady=(20, 10))
        
        event_log = ctk.CTkTextbox(event_panel, fg_color=THEME_COLORS["bg_dark"], text_color=THEME_COLORS["success_text"], font=("Consolas", 13), corner_radius=8, border_width=1, border_color=THEME_COLORS["border"])
        event_log.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        event_log.insert("0.0", "[10:00:05] Session initialized.\n[10:00:06] Object Detection Model Loaded.\n")
        event_log.configure(state="disabled")