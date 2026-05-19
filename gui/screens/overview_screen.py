# gui/screens/overview_screen.py
import customtkinter as ctk
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.constants import TEXT_ICONS # Import hằng số doanh nghiệp

class OverviewScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.init_ui()

    def init_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header, text="Overview Dashboard", font=(FONT_FAMILY, 28, "bold"), text_color=THEME_COLORS["text_main"]).pack(anchor="w")
        ctk.CTkLabel(header, text="Real-time classroom analytics and monitoring statistics", font=(FONT_FAMILY, 14), text_color=THEME_COLORS["text_muted"]).pack(anchor="w", pady=(5,0))

        # Stats Cards
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=30, pady=10)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        cards_data = [
            ("TOTAL STUDENTS", "42", "", THEME_COLORS["text_main"]),
            ("PRESENT", "38", "↑ 90%", THEME_COLORS["success_text"]),
            ("AVG FOCUS RATE", "84%", "↑ 2%", THEME_COLORS["text_title"]),
            ("AI ALERTS", "3", "Action Needed", THEME_COLORS["warning"])
        ]

        for i, (label, val, sub_val, val_color) in enumerate(cards_data):
            card = ctk.CTkFrame(stats_frame, fg_color=THEME_COLORS["bg_card"], border_color=THEME_COLORS["border"], border_width=1, corner_radius=12)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            
            ctk.CTkLabel(card, text=label, font=(FONT_FAMILY, 12, "bold"), text_color=THEME_COLORS["text_muted"]).pack(anchor="w", padx=20, pady=(20, 5))
            
            val_frame = ctk.CTkFrame(card, fg_color="transparent")
            val_frame.pack(fill="x", padx=20, pady=(0, 20))
            
            ctk.CTkLabel(val_frame, text=val, font=(FONT_FAMILY, 36, "bold"), text_color=val_color).pack(side="left")
            
            if sub_val:
                sub_color = THEME_COLORS["success_text"] if "↑" in sub_val else THEME_COLORS["warning"]
                ctk.CTkLabel(val_frame, text=sub_val, font=(FONT_FAMILY, 13, "bold"), text_color=sub_color).pack(side="left", padx=10, anchor="s", pady=(0, 5))

        # Bottom Section
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(fill="both", expand=True, padx=30, pady=(15, 30))
        bottom_frame.grid_columnconfigure(0, weight=6, uniform="b") # Chart chiếm 60%
        bottom_frame.grid_columnconfigure(1, weight=4, uniform="b") # Alerts chiếm 40%

        # Chart
        left_panel = ctk.CTkFrame(bottom_frame, fg_color=THEME_COLORS["bg_card"], border_color=THEME_COLORS["border"], border_width=1, corner_radius=12)
        left_panel.grid(row=0, column=0, padx=10, sticky="nsew")
        ctk.CTkLabel(left_panel, text="ATTENDANCE & FOCUS TRENDS", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=25, pady=20)
        
        chart_placeholder = ctk.CTkFrame(left_panel, fg_color=THEME_COLORS["bg_input"], border_color=THEME_COLORS["border_dashed"], border_width=1, corner_radius=8)
        chart_placeholder.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # Thay thế ký tự chart cứng bằng việc gọi cấu trúc map của TEXT_ICONS
        ctk.CTkLabel(chart_placeholder, text=f"{TEXT_ICONS['chart_bar']}\nChart Visualization Placeholder\n(Matplotlib Canvas)", font=(FONT_FAMILY, 13), text_color=THEME_COLORS["text_muted"]).place(relx=0.5, rely=0.5, anchor="center")

        # Alerts
        right_panel = ctk.CTkFrame(bottom_frame, fg_color=THEME_COLORS["bg_card"], border_color=THEME_COLORS["border"], border_width=1, corner_radius=12)
        right_panel.grid(row=0, column=1, padx=10, sticky="nsew")
        ctk.CTkLabel(right_panel, text="🔔 RECENT AI ALERTS", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=25, pady=20)
        
        alerts = [
            ("John Doe is sleeping", "2 mins ago", THEME_COLORS["danger"]),
            ("Low focus detected", "5 mins ago", THEME_COLORS["warning"]),
            ("Distraction at row 3", "15 mins ago", THEME_COLORS["warning"])
        ]
        
        for msg, time, color in alerts:
            al_frame = ctk.CTkFrame(right_panel, fg_color=THEME_COLORS["bg_input"], corner_radius=8)
            al_frame.pack(fill="x", padx=25, pady=8)
            
            # Gọi TEXT_ICONS["alert_dot"] thay cho ký tự chấm tròn cứng
            ctk.CTkLabel(al_frame, text=TEXT_ICONS["alert_dot"], text_color=color, font=(FONT_FAMILY, 16)).pack(side="left", padx=(15, 10), pady=15)
            ctk.CTkLabel(al_frame, text=msg, text_color=THEME_COLORS["text_main"], font=(FONT_FAMILY, 13, "bold")).pack(side="left")
            ctk.CTkLabel(al_frame, text=time, text_color=THEME_COLORS["text_muted"], font=(FONT_FAMILY, 12)).pack(side="right", padx=15)