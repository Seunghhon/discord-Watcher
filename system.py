def latency_color(latency):
    if latency < 200:
        return 0x00CC22
    elif latency < 400:
        return 0xFFD400
    else:
        return 0xcc0000

def zapcollor(latency):
    global zap
    Green = "🟢"
    Yellow = "🟡"
    Red = "🔴"
    zap = "⚡"
    if latency < 200:
        zap = Green
        return zap
    elif latency < 400:
        zap = Yellow
        return zap
    else:
        zap = Red
        return zap
    
def favicon(status):
    try:
        if status.favicon:
            return True
        else:
            return False
    except:
        return None
