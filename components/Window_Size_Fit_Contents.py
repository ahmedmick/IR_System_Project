import Table_Adjustment

def set_window_size_to_fit_contents(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    content_width = sum(entry.winfo_width() for entry in window.winfo_children())
    content_height = sum(entry.winfo_height() for entry in window.winfo_children())

    window_width = min(width, content_width)
    window_height = min(height, content_height)
    Table_Adjustment.TABLE_WINDOW_X_AXIS = window_width
    Table_Adjustment.TABLE_WINDOW_Y_AXIS = window_height