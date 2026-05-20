# gui/screens/lecture_screen.py
import customtkinter as ctk
import threading
import cv2
import os
from PIL import Image, ImageTk
from gui.theme import THEME_COLORS, FONT_FAMILY
from core.vision_engine import VisionEngine
from db_helper import DatabaseHelper

class LectureScreen(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        self.engine = VisionEngine()
        self.db = DatabaseHelper()
        self.session_id = None
        self.grid_cards = {}
        self.init_ui()

    def init_ui(self):
        # Header Control Bar
        header = ctk.CTkFrame(self, fg_color="transparent", height=60)
        header.pack(fill="x", padx=35, pady=(25, 10))
        
        self.btn_start = ctk.CTkButton(
            header, text="Bắt Đầu Phiên Học (30s)", font=(FONT_FAMILY, 13, "bold"),
            fg_color=THEME_COLORS["primary"], hover_color=THEME_COLORS["primary_hover"],
            height=40, command=self.activate_lecture_session
        )
        self.btn_start.pack(side="left")

        self.status_label = ctk.CTkLabel(header, text="Trạng thái: Sẵn sàng", font=(FONT_FAMILY, 13), text_color=THEME_COLORS["text_muted"])
        self.status_label.pack(side="left", padx=20)

        # Main Layout
        main_grid = ctk.CTkFrame(self, fg_color="transparent")
        main_grid.pack(fill="both", expand=True, padx=35, pady=(0, 25))
        main_grid.grid_columnconfigure(0, weight=65, uniform="main_layout")
        main_grid.grid_columnconfigure(1, weight=35, uniform="main_layout")
        main_grid.grid_rowconfigure(0, weight=1)

        # LEFT PANEL (Camera + Realtime grid)
        left_area = ctk.CTkFrame(main_grid, fg_color="transparent")
        left_area.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left_area.grid_rowconfigure(0, weight=55)
        left_area.grid_rowconfigure(1, weight=45)
        left_area.grid_columnconfigure(0, weight=1)

        # Camera Frame (Fixed square-ish proportion)
        cam_panel = ctk.CTkFrame(left_area, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        cam_panel.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        
        self.cam_view = ctk.CTkLabel(cam_panel, text="[ Camera Feed Chưa Bật ]", font=(FONT_FAMILY, 15), text_color=THEME_COLORS["text_muted"])
        self.cam_view.pack(fill="both", expand=True, padx=12, pady=12)

        # Real-time Students Grid List
        list_title = ctk.CTkLabel(left_area, text="REAL-TIME LEARNING STATUS", font=(FONT_FAMILY, 13, "bold"), text_color=THEME_COLORS["text_title"])
        list_title.grid(row=1, column=0, sticky="w", pady=(0, 5))

        self.student_grid_scroll = ctk.CTkScrollableFrame(left_area, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        self.student_grid_scroll.grid(row=1, column=0, sticky="nsew")
        self.student_grid_scroll.grid_columnconfigure((0, 1, 2), weight=1, uniform="student_col")

        # RIGHT PANEL (Selected Info Confirmation)
        right_panel = ctk.CTkFrame(main_grid, fg_color=THEME_COLORS["bg_card"], corner_radius=12, border_width=1, border_color=THEME_COLORS["border"])
        right_panel.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        ctk.CTkLabel(right_panel, text="ATTENDANCE CONFIRMATION", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["text_title"]).pack(anchor="w", padx=25, pady=20)
        
        self.confirm_img_box = ctk.CTkFrame(right_panel, fg_color=THEME_COLORS["bg_input"], border_width=1, border_color=THEME_COLORS["border_dashed"], width=200, height=240)
        self.confirm_img_box.pack(pady=15)
        self.confirm_img_box.pack_propagate(False)

        self.confirm_avatar_label = ctk.CTkLabel(self.confirm_img_box, text="👤", font=(FONT_FAMILY, 72), text_color=THEME_COLORS["border"])
        self.confirm_avatar_label.place(relx=0.5, rely=0.5, anchor="center")

        self.lbl_confirm_name = ctk.CTkLabel(right_panel, text="Họ và tên: --", font=(FONT_FAMILY, 16, "bold"), text_color=THEME_COLORS["text_main"])
        self.lbl_confirm_name.pack(pady=5, padx=25, anchor="w")

        self.lbl_confirm_student_id = ctk.CTkLabel(right_panel, text="MSSV: --", font=(FONT_FAMILY, 14), text_color=THEME_COLORS["text_muted"])
        self.lbl_confirm_student_id.pack(pady=2, padx=25, anchor="w")

        self.lbl_confirm_status = ctk.CTkLabel(right_panel, text="Trạng thái: --", font=(FONT_FAMILY, 14, "bold"), text_color=THEME_COLORS["warning"])
        self.lbl_confirm_status.pack(pady=10, padx=25, anchor="w")

    def activate_lecture_session(self):
        self.session_id = self.db.create_new_lecture_session("Môn học Thử Nghiệm AI")
        self.btn_start.configure(state="disabled")
        self.status_label.configure(text="Trạng thái: Đang quét...", text_color=THEME_COLORS["primary_light"])
        
        # Clear UI Grid cũ
        for widget in self.student_grid_scroll.winfo_children():
            widget.destroy()
        self.grid_cards.clear()

        # Tạo luồng xử lý Camera Thread an toàn
        threading.Thread(   
            target=self.engine.start_stream,
            args=(
                self.session_id,
                self.update_camera_feed,
                self.update_student_card,
                self.lecture_session_end_callback,
                print
            ),
            daemon=True
        ).start()

    def update_camera_feed(self, cv_frame):
        """Hiển thị nguồn cấp dữ liệu camera an toàn đa luồng thông qua Hàng đợi vòng lặp giao diện người dùng chính"""
        def _render():
            try:
                cv_frame_resized = cv2.resize(cv_frame, (560, 400))
                cv_img = cv2.cvtColor(cv_frame_resized, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(cv_img)
                ctk_img = ctk.CTkImage(light_image=pil_img, size=(560, 400))
                self.cam_view.configure(image=ctk_img, text="")
            except Exception as e:
                print(f"[X] UI Render Error: {e}")
        
        self.after(0, _render)

    def update_student_card(self, student_id, student_name, attendance_status, avatar_path):
        """Trình xử lý thời gian thực an toàn luồng để ánh xạ các sự kiện cơ sở dữ liệu vào các phần tử giao diện người dùng dạng lưới."""
        def _render_student():
            # Cập nhật thông tin chi tiết bảng bên phải
            self.lbl_confirm_name.configure(text=f"Họ và tên: {student_name}")
            self.lbl_confirm_student_id.configure(text=f"MSSV: {student_id}")
            self.lbl_confirm_status.configure(
                text=f"Trạng thái: {attendance_status}",
                text_color=THEME_COLORS["success_text"] if attendance_status == "Có mặt" else (255, 165, 0)
            )
            
            if avatar_path and os.path.exists(avatar_path):
                try:
                    img_pil = Image.open(avatar_path)
                    ctk_avatar = ctk.CTkImage(light_image=img_pil, size=(180, 220))
                    self.confirm_avatar_label.configure(image=ctk_avatar, text="")
                except Exception:
                    self.confirm_avatar_label.configure(image=None, text="👤")

            current_behavior = self.engine.session_attendance.get(student_id, {}).get("behavior", "Focusing")
            
            # Tạo mới thẻ SV ở danh sách bên dưới nếu chưa tồn tại
            if student_id not in self.grid_cards:
                row_idx = len(self.grid_cards) // 3
                col_idx = len(self.grid_cards) % 3
                
                card = ctk.CTkFrame(self.student_grid_scroll, fg_color=THEME_COLORS["bg_input"], corner_radius=8, border_width=1, border_color=THEME_COLORS["border"])
                card.grid(row=row_idx, column=col_idx, padx=8, pady=8, sticky="nsew")
                
                lbl_name = ctk.CTkLabel(card, text=student_name, font=(FONT_FAMILY, 12, "bold"), text_color=THEME_COLORS["text_main"])
                lbl_name.pack(pady=(8, 2), padx=10, anchor="w")
                
                lbl_info = ctk.CTkLabel(card, text=f"{student_id} | {attendance_status}", font=(FONT_FAMILY, 11), text_color=THEME_COLORS["text_muted"])
                lbl_info.pack(padx=10, anchor="w")
                
                lbl_behavior = ctk.CTkLabel(card, text=current_behavior, font=(FONT_FAMILY, 11, "bold"), text_color=THEME_COLORS["success_text"])
                lbl_behavior.pack(pady=(5, 8), padx=10, anchor="w")
                
                self.grid_cards[student_id] = {"card": card, "lbl_behavior": lbl_behavior}
            else:
                # Cập nhật hành vi lớp học thời gian thực
                behavior_label = self.grid_cards[student_id]["lbl_behavior"]
                behavior_label.configure(
                    text=current_behavior,
                    text_color=THEME_COLORS["success_text"] if current_behavior == "Focusing" else THEME_COLORS["warning"]
                )
        
        self.after(0, _render_student)

    def lecture_session_end_callback(self):
        def _render_end():
            self.btn_start.configure(state="normal")
            self.status_label.configure(text="Trạng thái: Hoàn thành phiên học 30s", text_color=THEME_COLORS["success_text"])
            self.cam_view.configure(image=None, text="[ Phiên Học Đã Kết Thúc - Camera Tắt ]")
        self.after(0, _render_end)

    def pack_forget(self):
        self.engine.stop_stream()
        super().pack_forget()