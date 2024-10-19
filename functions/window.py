import pygetwindow as gw

def get_focused_window_message():
    active_window = gw.getActiveWindow()
    
    if active_window:
        window_title = active_window.title
        # Customize the message within window.py
        return f"🖥️ **Active window:** `{window_title}`"
    else:
        return "**Error:** `No active window found.`"
