# gui/theme.py

THEME_COLORS = {
    # 1. Backgrounds (Tạo chiều sâu từ ngoài vào trong)
    "bg_main": "#0F172A",       # Nền tổng thể (Slate 900)
    "bg_sidebar": "#0B1120",    # Nền Sidebar (Tối hơn nền chính để tạo tách biệt)
    "bg_card": "#1E293B",       # Nền các Panel/Card (Sáng hơn nền chính)
    "bg_card_hover": "#334155", # Khi hover vào menu
    "bg_input": "#0B1120",      # Nền ô nhập liệu (Đậm lại để lõm xuống)
    "bg_dark": "#020617",       # Đen sâu cho Terminal/Logs
    "black": "#000000",         # Đen tuyệt đối cho Camera
    
    # 2. Borders (Viền)
    "border": "#334155",        # Viền card mềm mại
    "border_dashed": "#475569", # Viền đứt nét sáng hơn
    
    # 3. Typography (Chữ)
    "text_main": "#F8FAFC",     # Trắng bạc (dịu mắt hơn trắng tinh)
    "text_muted": "#94A3B8",    # Xám nhạt cho sub-text
    "text_title": "#38BDF8",    # Xanh Cyan (Nhấn mạnh tiêu đề)
    
    # 4. Brand & Actions (Nút bấm, tương tác)
    "primary": "#3B82F6",       # Xanh dương chủ đạo
    "primary_hover": "#2563EB", 
    "primary_light": "#93C5FD", # Xanh dương nhạt cho các text highlight
    
    # 5. Semantic / Status (Trạng thái)
    "success_bg": "#064E3B",    # Xanh lá nền tối
    "success_text": "#34D399",  # Xanh lá chữ sáng
    "warning": "#F59E0B",       # Vàng cam cảnh báo
    "danger": "#EF4444",        # Đỏ lỗi/cảnh báo
    
    # 6. Specific Components
    "record_bg": "#450A0A",     # Nền đỏ tối cho Record
    "ai_active_bg": "#1E3A8A",  # Nền xanh tối cho AI Active
    "btn_pdf_bg": "#7F1D1D",    # Nút upload PDF (Tone đỏ)
    "btn_pdf_border": "#991B1B",
    "btn_pdf_hover": "#B91C1C"
}

# Sử dụng Inter hoặc Roboto nếu máy có cài, mặc định fallback về Segoe UI
FONT_FAMILY = "Segoe UI"