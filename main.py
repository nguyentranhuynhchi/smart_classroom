# main.py
import customtkinter as ctk
from gui.theme import THEME_COLORS
from gui.components.sidebar import Sidebar
from gui.screens.overview_screen import OverviewScreen
from gui.screens.enrollment_screen import EnrollmentScreen
from gui.screens.session_screen import SessionScreen
from gui.screens.lecture_screen import LectureScreen
from gui.screens.account_screen import AccountScreen

class SmartClassroomApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Smart Classroom AI")
        self.geometry("1280x720")
        self.minsize(1024, 768)
        
        self.configure(fg_color=THEME_COLORS["bg_main"])
        ctk.set_appearance_mode("dark")
        
        try:
            self.state("zoomed")
        except:
            self.attributes("-zoomed", True)
            
        self.grid_columnconfigure(0, weight=0, minsize=260) 
        self.grid_columnconfigure(1, weight=1)              
        self.grid_rowconfigure(0, weight=1)
        
        self.current_screen = None
        self.screens = {}
        self.init_ui()

    def init_ui(self):
        self.sidebar = Sidebar(self, on_menu_select=self.switch_screen)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        
        self.screens["overview"] = OverviewScreen(self.content_container)
        self.screens["enrollment"] = EnrollmentScreen(self.content_container)
        self.screens["session"] = SessionScreen(self.content_container)
        self.screens["lecture"] = LectureScreen(self.content_container)
        self.screens["account"] = AccountScreen(self.content_container)
        
        # Mở màn hình enrollment lên trước để xem thành quả
        self.switch_screen("enrollment")

    def switch_screen(self, screen_id):
        if self.current_screen:
            self.current_screen.pack_forget()
            
        target_screen = self.screens.get(screen_id)
        if target_screen:
            target_screen.pack(fill="both", expand=True)
            self.current_screen = target_screen

if __name__ == "__main__":
    app = SmartClassroomApp()
    app.mainloop()