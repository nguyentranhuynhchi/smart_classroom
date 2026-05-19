# gui/screens/enrollment_screen.py
import customtkinter as ctk
from gui.theme import THEME_COLORS, FONT_FAMILY
from gui.constants import TEXT_ICONS # Import hằng số doanh nghiệp

class EnrollmentScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.init_ui()

    def init_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))
        ctk.CTkLabel(header_frame, text="Student Enrollment", font=(FONT_FAMILY, 28, "bold"), text_color=THEME_COLORS["text_main"]).pack(side="left")

        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        content.grid_columnconfigure(0, weight=1, uniform="col")
        content.grid_columnconfigure(1, weight=1, uniform="col")

        # LEFT PANEL (Image & Camera)
        left_panel = ctk.CTkFrame(content, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10)
        
        ctk.CTkLabel(left_panel, text="Student Image Data", font=(FONT_FAMILY, 16, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=30, pady=(25, 20))
        
        upload_box = ctk.CTkFrame(left_panel, fg_color=THEME_COLORS["bg_input"], corner_radius=8, border_width=1, border_color=THEME_COLORS["border_dashed"])
        upload_box.pack(fill="x", padx=30, pady=(0, 20), ipady=35)
        
        # Thay đổi ký tự cloud cứng thành hằng số gọi từ constants
        ctk.CTkLabel(upload_box, text=TEXT_ICONS["upload_cloud"], font=(FONT_FAMILY, 40), text_color=THEME_COLORS["primary"]).pack(pady=(15, 5))
        ctk.CTkLabel(upload_box, text="Drag & drop image here or click to browse", font=(FONT_FAMILY, 13), text_color=THEME_COLORS["text_muted"]).pack()

        cam_box = ctk.CTkFrame(left_panel, fg_color=THEME_COLORS["black"], corner_radius=8, border_width=1, border_color=THEME_COLORS["border"])
        cam_box.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Thay đổi camera placeholder text bằng hằng số gọi từ constants
        ctk.CTkLabel(cam_box, text=TEXT_ICONS["camera_feed"], font=(FONT_FAMILY, 16), text_color=THEME_COLORS["text_muted"]).place(relx=0.5, rely=0.5, anchor="center")

        # RIGHT PANEL (Information Form)
        right_panel = ctk.CTkFrame(content, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        right_panel.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(right_panel, text="Student Profile", font=(FONT_FAMILY, 16, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=30, pady=(25, 10))

        form_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        form_container.pack(fill="both", expand=True, padx=30)

        fields = [("Student ID", "Ex: 23110000"), ("Full Name", "Ex: Nguyen Van A"), ("Class", "Ex: 23T1"), ("Email", "student@hcmute.edu.vn"), ("Phone", "09xx xxx xxx")]
        
        for label, placeholder in fields:
            ctk.CTkLabel(form_container, text=label, font=(FONT_FAMILY, 13, "bold"), text_color=THEME_COLORS["text_muted"]).pack(anchor="w", pady=(10, 5))
            ctk.CTkEntry(form_container, placeholder_text=placeholder, fg_color=THEME_COLORS["bg_input"], border_color=THEME_COLORS["border"], height=45, font=(FONT_FAMILY, 14)).pack(fill="x")

        # Buttons
        btn_container = ctk.CTkFrame(right_panel, fg_color="transparent")
        btn_container.pack(fill="x", padx=30, pady=25)

        ctk.CTkButton(btn_container, text="Save Student", font=(FONT_FAMILY, 15, "bold"), fg_color=THEME_COLORS["primary"], hover_color=THEME_COLORS["primary_hover"], height=50, corner_radius=8).pack(side="left", fill="x", expand=True, padx=(0, 15))
        ctk.CTkButton(btn_container, text="Reset", font=(FONT_FAMILY, 14), fg_color="transparent", border_color=THEME_COLORS["border"], border_width=1, text_color=THEME_COLORS["text_main"], hover_color=THEME_COLORS["bg_input"], height=50, width=120, corner_radius=8).pack(side="right")