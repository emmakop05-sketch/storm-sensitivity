# sensitivity_engine.py


# ==========================================
# LIMIT VALUE
# ==========================================

def clamp(value, minimum=0, maximum=200):
    return max(minimum, min(maximum, round(value)))


# ==========================================
# GENERATE INITIAL SENSITIVITY
# ==========================================

def calculate_sensitivity(
    device,
    dpi=None,
    ram=4,
    refresh_rate=60,
    finger_layout="2 Finger",
    play_style="Balanced",
    use_dpi=True
):

    performance = device.get("performance", 5)

    # --------------------------------------
    # BASE
    # --------------------------------------

    base = 145

    # --------------------------------------
    # DEVICE PERFORMANCE
    # --------------------------------------

    base += (performance - 5) * 3

    # --------------------------------------
    # DPI
    # --------------------------------------

    if use_dpi and dpi is not None:

        if dpi < 400:
            base -= 15

        elif dpi < 450:
            base -= 8

        elif dpi <= 550:
            base += 3

        elif dpi <= 650:
            base += 7

        else:
            base += 10

    # --------------------------------------
    # REFRESH RATE
    # --------------------------------------

    if refresh_rate <= 60:
        base -= 8

    elif refresh_rate <= 90:
        base -= 2

    elif refresh_rate <= 120:
        base += 5

    else:
        base += 8

    # --------------------------------------
    # RAM
    # --------------------------------------

    if ram <= 3:
        base -= 8

    elif ram <= 4:
        base -= 4

    elif ram >= 8:
        base += 3

    # --------------------------------------
    # FINGER LAYOUT
    # --------------------------------------

    layout_adjustment = {
        "2 Finger": -4,
        "3 Finger": 0,
        "4 Finger": 5
    }

    base += layout_adjustment.get(
        finger_layout,
        0
    )

    # --------------------------------------
    # PLAY STYLE
    # --------------------------------------

    style_adjustment = {
        "Headshot": 8,
        "Aggressive": 10,
        "Balanced": 0,
        "Sniper": -12
    }

    base += style_adjustment.get(
        play_style,
        0
    )

    # --------------------------------------
    # FINAL SETTINGS
    # --------------------------------------

    settings = {

        "General": clamp(base),

        "Red Dot": clamp(base - 5),

        "2x Scope": clamp(base - 14),

        "4x Scope": clamp(base - 25),

        "Sniper Scope": clamp(base - 55),

        "Free Look": clamp(base - 8)
    }

    return settings


# ==========================================
# DPI RECOMMENDATION
# ==========================================

def recommended_dpi(
    device,
    current_dpi,
    play_style
):

    minimum, maximum = device.get(
        "dpi_range",
        [400, 600]
    )

    if play_style == "Headshot":

        target = current_dpi + 15

    elif play_style == "Aggressive":

        target = current_dpi + 25

    elif play_style == "Sniper":

        target = current_dpi - 20

    else:

        target = current_dpi

    target = max(
        minimum,
        min(maximum, target)
    )

    lower = max(
        minimum,
        target - 20
    )

    upper = min(
        maximum,
        target + 20
    )

    return f"{lower} - {upper}"


# ==========================================
# AIM FEEDBACK ENGINE
# ==========================================

def adjust_sensitivity(
    settings,
    feedback
):

    updated = settings.copy()

    # --------------------------------------
    # DRAG TOO HIGH
    # --------------------------------------

    if feedback == "1":

        updated["General"] -= 8
        updated["Red Dot"] -= 7
        updated["2x Scope"] -= 5
        updated["4x Scope"] -= 4
        updated["Free Look"] -= 5

    # --------------------------------------
    # DRAG TOO LOW
    # --------------------------------------

    elif feedback == "2":

        updated["General"] += 8
        updated["Red Dot"] += 7
        updated["2x Scope"] += 5
        updated["4x Scope"] += 4
        updated["Free Look"] += 5

    # --------------------------------------
    # AIM TOO SLOW
    # --------------------------------------

    elif feedback == "3":

        updated["General"] += 6
        updated["Red Dot"] += 6
        updated["2x Scope"] += 5
        updated["4x Scope"] += 4
        updated["Free Look"] += 6

    # --------------------------------------
    # AIM TOO FAST
    # --------------------------------------

    elif feedback == "4":

        updated["General"] -= 6
        updated["Red Dot"] -= 6
        updated["2x Scope"] -= 5
        updated["4x Scope"] -= 4
        updated["Free Look"] -= 6

    # --------------------------------------
    # HEADSHOTS INCONSISTENT
    # --------------------------------------

    elif feedback == "5":

        updated["General"] += 3
        updated["Red Dot"] += 4
        updated["2x Scope"] += 2

    # --------------------------------------
    # PERFECT
    # --------------------------------------

    elif feedback == "6":

        return updated

    # --------------------------------------
    # LIMIT VALUES
    # --------------------------------------

    for key in updated:

        updated[key] = clamp(
            updated[key]
        )

    return updated