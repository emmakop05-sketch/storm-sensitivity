import json
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# STORM SENSITIVITY
# ============================================================

APP_NAME = "🌩️ STORM SENSITIVITY"

BG = "#090611"
CARD = "#15101f"
CARD2 = "#1d1629"

PURPLE = "#8b5cf6"
PURPLE_DARK = "#6d28d9"

WHITE = "#ffffff"
GRAY = "#aaa3b8"
GREEN = "#22c55e"
RED = "#ef4444"


# ============================================================
# LOAD DEVICE DATABASE
# ============================================================

try:

    with open(
        "devices.json",
        "r",
        encoding="utf-8"
    ) as file:

        devices = json.load(file)

except FileNotFoundError:

    devices = {}

    print(
        "⚠️ devices.json not found."
    )

except json.JSONDecodeError:

    devices = {}

    print(
        "⚠️ devices.json contains invalid JSON."
    )


# ============================================================
# MAIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Storm Sensitivity"
)

root.geometry(
    "1200x800"
)

root.minsize(
    950,
    650
)

root.configure(
    bg=BG
)


# ============================================================
# VARIABLES
# ============================================================

brand_var = tk.StringVar(
    master=root
)

model_var = tk.StringVar(
    master=root
)

search_var = tk.StringVar(
    master=root
)

manual_model_var = tk.StringVar(
    master=root
)

dpi_enabled = tk.BooleanVar(
    master=root,
    value=True
)

dpi_var = tk.StringVar(
    master=root,
    value="460"
)

manual_refresh_var = tk.StringVar(
    master=root,
    value="90"
)

ram_var = tk.StringVar(
    master=root,
    value="8 GB"
)

finger_var = tk.StringVar(
    master=root,
    value="4 Finger"
)

style_var = tk.StringVar(
    master=root,
    value="Headshot"
)

device_mode = tk.StringVar(
    master=root,
    value="database"
)


current_settings = {}


# ============================================================
# SENSITIVITY ENGINE
# ============================================================

def calculate_sensitivity(
    device,
    dpi,
    ram,
    refresh_rate,
    finger_layout,
    play_style,
    use_dpi
):

    # Base value
    general = 150

    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    performance = device.get(
        "performance",
        5
    )

    general += performance - 5

    # --------------------------------------------------------
    # REFRESH RATE
    # --------------------------------------------------------

    if refresh_rate >= 144:

        general += 10

    elif refresh_rate >= 120:

        general += 8

    elif refresh_rate >= 90:

        general += 5

    elif refresh_rate >= 60:

        general += 2

    else:

        general -= 5

    # --------------------------------------------------------
    # RAM
    # --------------------------------------------------------

    if ram >= 16:

        general += 6

    elif ram >= 12:

        general += 5

    elif ram >= 8:

        general += 3

    elif ram >= 6:

        general += 1

    elif ram <= 3:

        general -= 5

    # --------------------------------------------------------
    # DPI
    # --------------------------------------------------------

    if use_dpi and dpi:

        if dpi >= 600:

            general -= 4

        elif dpi >= 550:

            general -= 2

        elif dpi >= 500:

            general -= 1

        elif dpi >= 450:

            general += 2

        elif dpi < 400:

            general += 4

    # --------------------------------------------------------
    # FINGER LAYOUT
    # --------------------------------------------------------

    if finger_layout == "4 Finger":

        general += 6

    elif finger_layout == "3 Finger":

        general += 3

    elif finger_layout == "2 Finger":

        general -= 2

    # --------------------------------------------------------
    # PLAY STYLE
    # --------------------------------------------------------

    if play_style == "Headshot":

        general += 6

    elif play_style == "Aggressive":

        general += 8

    elif play_style == "Balanced":

        general += 2

    elif play_style == "Sniper":

        general -= 8

    # --------------------------------------------------------
    # LIMIT
    # --------------------------------------------------------

    general = max(
        50,
        min(general, 200)
    )

    # --------------------------------------------------------
    # OTHER SETTINGS
    # --------------------------------------------------------

    red_dot = general - 5

    scope_2x = general - 16

    scope_4x = general - 27

    sniper = general - 57

    free_look = general - 8

    return {

        "General": max(
            1,
            red_dot + 5
        ),

        "Red Dot": max(
            1,
            red_dot
        ),

        "2x Scope": max(
            1,
            scope_2x
        ),

        "4x Scope": max(
            1,
            scope_4x
        ),

        "Sniper Scope": max(
            1,
            sniper
        ),

        "Free Look": max(
            1,
            free_look
        )
    }


# ============================================================
# DPI RECOMMENDATION
# ============================================================

def recommended_dpi(
    device,
    current_dpi,
    play_style
):

    minimum = device.get(
        "dpi_min",
        450
    )

    maximum = device.get(
        "dpi_max",
        600
    )

    if current_dpi:

        lower = current_dpi - 5

        upper = current_dpi + 35

    else:

        lower = minimum

        upper = minimum + 40

    if play_style == "Headshot":

        lower += 5
        upper += 5

    elif play_style == "Sniper":

        lower -= 10
        upper -= 10

    lower = max(
        minimum,
        lower
    )

    upper = min(
        maximum,
        upper
    )

    return f"{lower} - {upper}"


# ============================================================
# FEEDBACK ENGINE
# ============================================================

def adjust_sensitivity(
    settings,
    feedback
):

    updated = settings.copy()

    changes = {

        "1": -5,

        "2": 5,

        "3": 4,

        "4": -4,

        "5": 2
    }

    change = changes.get(
        feedback,
        0
    )

    for key in updated:

        updated[key] = max(
            1,
            min(
                200,
                updated[key] + change
            )
        )

    return updated


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    root,
    bg=BG
)

header.pack(
    fill="x",
    padx=35,
    pady=(25, 15)
)


tk.Label(
    header,
    text=APP_NAME,
    bg=BG,
    fg=PURPLE,
    font=(
        "Segoe UI",
        29,
        "bold"
    )
).pack(
    anchor="w"
)


tk.Label(
    header,
    text="Smart Free Fire Sensitivity & DPI Generator",
    bg=BG,
    fg=GRAY,
    font=(
        "Segoe UI",
        11
    )
).pack(
    anchor="w"
)


# ============================================================
# MAIN CONTAINER
# ============================================================

main = tk.Frame(
    root,
    bg=BG
)

main.pack(
    fill="both",
    expand=True,
    padx=35,
    pady=5
)


# ============================================================
# LEFT PANEL
# ============================================================

left_outer = tk.Frame(
    main,
    bg=CARD,
    width=410
)

left_outer.pack(
    side="left",
    fill="y",
    padx=(0, 15)
)

left_outer.pack_propagate(
    False
)


# ============================================================
# SCROLLABLE LEFT PANEL
# ============================================================

canvas = tk.Canvas(
    left_outer,
    bg=CARD,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    left_outer,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


left = tk.Frame(
    canvas,
    bg=CARD
)


canvas_window = canvas.create_window(
    (0, 0),
    window=left,
    anchor="nw"
)


def update_scroll(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_canvas(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


left.bind(
    "<Configure>",
    update_scroll
)

canvas.bind(
    "<Configure>",
    resize_canvas
)


# ============================================================
# DEVICE MODE
# ============================================================

tk.Label(
    left,
    text="📱 DEVICE MODE",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        14,
        "bold"
    )
).pack(
    anchor="w",
    padx=25,
    pady=(25, 10)
)


mode_frame = tk.Frame(
    left,
    bg=CARD
)

mode_frame.pack(
    padx=25,
    fill="x"
)


def change_mode():

    if device_mode.get() == "database":

        database_frame.pack(
            fill="x"
        )

        manual_frame.pack_forget()

    else:

        database_frame.pack_forget()

        manual_frame.pack(
            fill="x"
        )


tk.Radiobutton(
    mode_frame,
    text="📚 Phone Database",
    variable=device_mode,
    value="database",
    command=change_mode,
    bg=CARD,
    fg=WHITE,
    selectcolor=CARD2,
    activebackground=CARD,
    activeforeground=WHITE
).pack(
    side="left"
)


tk.Radiobutton(
    mode_frame,
    text="✏️ My phone isn't listed",
    variable=device_mode,
    value="manual",
    command=change_mode,
    bg=CARD,
    fg=WHITE,
    selectcolor=CARD2,
    activebackground=CARD,
    activeforeground=WHITE
).pack(
    side="left"
)


# ============================================================
# DATABASE FRAME
# ============================================================

database_frame = tk.Frame(
    left,
    bg=CARD
)

database_frame.pack(
    fill="x"
)


# ============================================================
# BRAND
# ============================================================

tk.Label(
    database_frame,
    text="Brand",
    bg=CARD,
    fg=WHITE
).pack(
    anchor="w",
    padx=25,
    pady=(15, 5)
)


brand_combo = ttk.Combobox(
    database_frame,
    textvariable=brand_var,
    values=list(
        devices.keys()
    ),
    state="readonly"
)

brand_combo.pack(
    padx=25,
    fill="x"
)


# ============================================================
# MODEL SEARCH
# ============================================================

tk.Label(
    database_frame,
    text="🔎 Search Model",
    bg=CARD,
    fg=WHITE
).pack(
    anchor="w",
    padx=25,
    pady=(12, 5)
)


search_entry = tk.Entry(
    database_frame,
    textvariable=search_var,
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

search_entry.pack(
    padx=25,
    fill="x",
    ipady=8
)


# ============================================================
# MODEL LIST
# ============================================================

model_list = tk.Listbox(
    database_frame,
    bg=CARD2,
    fg=WHITE,
    selectbackground=PURPLE,
    selectforeground=WHITE,
    relief="flat",
    height=6
)

model_list.pack(
    padx=25,
    fill="x",
    pady=(8, 10)
)


def update_models(event=None):

    brand = brand_var.get()

    model_list.delete(
        0,
        tk.END
    )

    if not brand:

        return

    for model in devices[brand]:

        model_list.insert(
            tk.END,
            model
        )

    if model_list.size() > 0:

        model_list.selection_set(
            0
        )

        model_var.set(
            model_list.get(0)
        )


def search_models(*args):

    brand = brand_var.get()

    if not brand:

        return

    query = search_var.get().lower()

    model_list.delete(
        0,
        tk.END
    )

    for model in devices[brand]:

        if query in model.lower():

            model_list.insert(
                tk.END,
                model
            )

    if model_list.size() > 0:

        model_list.selection_set(
            0
        )

        model_var.set(
            model_list.get(0)
        )


def select_model(event=None):

    selected = model_list.curselection()

    if not selected:

        return

    model_var.set(
        model_list.get(
            selected[0]
        )
    )


brand_combo.bind(
    "<<ComboboxSelected>>",
    update_models
)

search_var.trace_add(
    "write",
    search_models
)

model_list.bind(
    "<<ListboxSelect>>",
    select_model
)


# ============================================================
# MANUAL PHONE FRAME
# ============================================================

manual_frame = tk.Frame(
    left,
    bg=CARD
)


tk.Label(
    manual_frame,
    text="✏️ ENTER YOUR PHONE",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        13,
        "bold"
    )
).pack(
    anchor="w",
    padx=25,
    pady=(15, 10)
)


tk.Label(
    manual_frame,
    text="Phone model",
    bg=CARD,
    fg=WHITE
).pack(
    anchor="w",
    padx=25
)


manual_model_entry = tk.Entry(
    manual_frame,
    textvariable=manual_model_var,
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

manual_model_entry.pack(
    padx=25,
    fill="x",
    pady=(5, 10),
    ipady=8
)


tk.Label(
    manual_frame,
    text="Refresh Rate (Hz)",
    bg=CARD,
    fg=WHITE
).pack(
    anchor="w",
    padx=25
)


manual_refresh_entry = tk.Entry(
    manual_frame,
    textvariable=manual_refresh_var,
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

manual_refresh_entry.pack(
    padx=25,
    fill="x",
    pady=(5, 10),
    ipady=8
)


# ============================================================
# DPI
# ============================================================

tk.Label(
    left,
    text="🎚️ DPI",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        13,
        "bold"
    )
).pack(
    anchor="w",
    padx=25,
    pady=(15, 5)
)


def update_dpi():

    if dpi_enabled.get():

        dpi_entry.config(
            state="normal"
        )

    else:

        dpi_entry.config(
            state="disabled"
        )


tk.Checkbutton(
    left,
    text="Use DPI",
    variable=dpi_enabled,
    command=update_dpi,
    bg=CARD,
    fg=WHITE,
    selectcolor=CARD2,
    activebackground=CARD,
    activeforeground=WHITE
).pack(
    anchor="w",
    padx=25
)


dpi_entry = tk.Entry(
    left,
    textvariable=dpi_var,
    bg=CARD2,
    fg=WHITE,
    insertbackground=WHITE,
    relief="flat"
)

dpi_entry.pack(
    padx=25,
    fill="x",
    pady=(3, 12),
    ipady=8
)


# ============================================================
# RAM
# ============================================================

tk.Label(
    left,
    text="💾 RAM",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        12,
        "bold"
    )
).pack(
    anchor="w",
    padx=25
)


ram_combo = ttk.Combobox(
    left,
    textvariable=ram_var,
    values=[
        "2 GB",
        "3 GB",
        "4 GB",
        "6 GB",
        "8 GB",
        "12 GB",
        "16 GB",
        "24 GB"
    ],
    state="readonly"
)

ram_combo.pack(
    padx=25,
    fill="x",
    pady=(5, 12)
)


# ============================================================
# FINGER LAYOUT
# ============================================================

tk.Label(
    left,
    text="👆 FINGER LAYOUT",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        12,
        "bold"
    )
).pack(
    anchor="w",
    padx=25
)


finger_frame = tk.Frame(
    left,
    bg=CARD
)

finger_frame.pack(
    padx=25,
    fill="x",
    pady=8
)


finger_buttons = {}


def choose_finger(value):

    finger_var.set(
        value
    )

    for name, button in finger_buttons.items():

        if name == value:

            button.config(
                bg=PURPLE
            )

        else:

            button.config(
                bg=CARD2
            )


for value in [
    "2 Finger",
    "3 Finger",
    "4 Finger"
]:

    button = tk.Button(
        finger_frame,
        text=value.split()[0],
        command=lambda v=value: choose_finger(v),
        bg=CARD2,
        fg=WHITE,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        width=8,
        cursor="hand2"
    )

    button.pack(
        side="left",
        padx=3
    )

    finger_buttons[value] = button


choose_finger(
    "4 Finger"
)


# ============================================================
# PLAY STYLE
# ============================================================

tk.Label(
    left,
    text="🎯 PLAY STYLE",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        12,
        "bold"
    )
).pack(
    anchor="w",
    padx=25,
    pady=(10, 5)
)


style_combo = ttk.Combobox(
    left,
    textvariable=style_var,
    values=[
        "Headshot",
        "Aggressive",
        "Balanced",
        "Sniper"
    ],
    state="readonly"
)

style_combo.pack(
    padx=25,
    fill="x"
)


# ============================================================
# GENERATE FUNCTION
# ============================================================

def generate():

    global current_settings

    # --------------------------------------------------------
    # DATABASE MODE
    # --------------------------------------------------------

    if device_mode.get() == "database":

        brand = brand_var.get()

        model = model_var.get()

        if not brand:

            messagebox.showerror(
                "Phone Missing",
                "Please select your phone brand."
            )

            return

        if not model:

            messagebox.showerror(
                "Phone Missing",
                "Please select your phone model."
            )

            return

        if model not in devices[brand]:

            messagebox.showerror(
                "Phone Error",
                "That phone is not available."
            )

            return

        device = devices[brand][model]

        phone_name = f"{brand} {model}"

        refresh_rate = device.get(
            "refresh_rate",
            60
        )

    # --------------------------------------------------------
    # MANUAL MODE
    # --------------------------------------------------------

    else:

        phone_name = manual_model_var.get().strip()

        if not phone_name:

            messagebox.showerror(
                "Phone Missing",
                "Type your phone model."
            )

            return

        try:

            refresh_rate = int(
                manual_refresh_var.get()
            )

        except ValueError:

            messagebox.showerror(
                "Refresh Rate Error",
                "Refresh rate must be a number."
            )

            return

        if refresh_rate <= 0:

            messagebox.showerror(
                "Refresh Rate Error",
                "Enter a valid refresh rate."
            )

            return

        device = {

            "refresh_rate": refresh_rate,

            "performance": 5,

            "dpi_min": 400,

            "dpi_max": 650
        }

    # --------------------------------------------------------
    # RAM
    # --------------------------------------------------------

    try:

        ram = int(
            ram_var.get().split()[0]
        )

    except:

        messagebox.showerror(
            "RAM Error",
            "Select a valid RAM."
        )

        return

    # --------------------------------------------------------
    # DPI
    # --------------------------------------------------------

    if dpi_enabled.get():

        try:

            dpi = int(
                dpi_var.get()
            )

        except:

            messagebox.showerror(
                "DPI Error",
                "DPI must be a number."
            )

            return

        if dpi <= 0:

            messagebox.showerror(
                "DPI Error",
                "DPI must be greater than 0."
            )

            return

    else:

        dpi = None

    # --------------------------------------------------------
    # OTHER OPTIONS
    # --------------------------------------------------------

    finger_layout = finger_var.get()

    play_style = style_var.get()

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    current_settings = calculate_sensitivity(

        device=device,

        dpi=dpi,

        ram=ram,

        refresh_rate=refresh_rate,

        finger_layout=finger_layout,

        play_style=play_style,

        use_dpi=dpi_enabled.get()
    )

    # --------------------------------------------------------
    # DISPLAY
    # --------------------------------------------------------

    for name, label in result_labels.items():

        label.config(
            text=str(
                current_settings[name]
            )
        )

    device_result.config(
        text=(
            f"📱 {phone_name}  •  "
            f"{refresh_rate} Hz  •  "
            f"{ram} GB RAM  •  "
            f"{finger_layout}  •  "
            f"{play_style}"
        ),
        fg=WHITE
    )

    # --------------------------------------------------------
    # DPI RESULT
    # --------------------------------------------------------

    if dpi_enabled.get():

        dpi_result = recommended_dpi(

            device=device,

            current_dpi=dpi,

            play_style=play_style
        )

        dpi_result_label.config(
            text=f"🎚️ Recommended DPI: {dpi_result}"
        )

    else:

        dpi_result_label.config(
            text="🎚️ DPI: Not being used"
        )

    # --------------------------------------------------------
    # MATCH SCORE
    # --------------------------------------------------------

    performance = device.get(
        "performance",
        5
    )

    score = 60

    score += performance * 3

    if refresh_rate >= 120:

        score += 8

    elif refresh_rate >= 90:

        score += 5

    score = max(
        50,
        min(
            score,
            98
        )
    )

    match_label.config(
        text=f"⚡ Storm Device Match: {score}%"
    )


# ============================================================
# GENERATE BUTTON
# ============================================================

generate_button = tk.Button(
    left,
    text="🔥 GENERATE SENSITIVITY",
    command=generate,
    bg=PURPLE,
    fg=WHITE,
    activebackground=PURPLE_DARK,
    activeforeground=WHITE,
    relief="flat",
    font=(
        "Segoe UI",
        12,
        "bold"
    ),
    cursor="hand2"
)

generate_button.pack(
    padx=25,
    fill="x",
    pady=(22, 25),
    ipady=13
)


# ============================================================
# RIGHT PANEL
# ============================================================

right = tk.Frame(
    main,
    bg=CARD
)

right.pack(
    side="right",
    fill="both",
    expand=True
)


# ============================================================
# RESULTS HEADER
# ============================================================

tk.Label(
    right,
    text="🎯 YOUR STORM SETTINGS",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        20,
        "bold"
    )
).pack(
    anchor="w",
    padx=30,
    pady=(30, 5)
)


device_result = tk.Label(
    right,
    text="Choose your phone and generate your settings.",
    bg=CARD,
    fg=GRAY,
    font=("Segoe UI", 10)
)

device_result.pack(
    anchor="w",
    padx=30,
    pady=(0, 20)
)


# ============================================================
# RESULT CARD
# ============================================================

result_card = tk.Frame(
    right,
    bg=CARD2
)

result_card.pack(
    padx=30,
    fill="x"
)


result_labels = {}


for name in [
    "General",
    "Red Dot",
    "2x Scope",
    "4x Scope",
    "Sniper Scope",
    "Free Look"
]:

    row = tk.Frame(
        result_card,
        bg=CARD2
    )

    row.pack(
        fill="x",
        padx=25,
        pady=10
    )

    tk.Label(
        row,
        text=name,
        bg=CARD2,
        fg=WHITE,
        font=(
            "Segoe UI",
            11
        )
    ).pack(
        side="left"
    )

    value_label = tk.Label(
        row,
        text="--",
        bg=CARD2,
        fg=PURPLE,
        font=(
            "Segoe UI",
            16,
            "bold"
        )
    )

    value_label.pack(
        side="right"
    )

    result_labels[name] = value_label


# ============================================================
# DPI RESULT
# ============================================================

dpi_result_label = tk.Label(
    right,
    text="🎚️ Recommended DPI: --",
    bg=CARD,
    fg=GREEN,
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

dpi_result_label.pack(
    anchor="w",
    padx=30,
    pady=(20, 5)
)


# ============================================================
# MATCH SCORE
# ============================================================

match_label = tk.Label(
    right,
    text="⚡ Storm Device Match: --",
    bg=CARD,
    fg=WHITE,
    font=(
        "Segoe UI",
        12,
        "bold"
    )
)

match_label.pack(
    anchor="w",
    padx=30,
    pady=5
)


# ============================================================
# FEEDBACK
# ============================================================

tk.Label(
    right,
    text="🔄 AIM FEEDBACK",
    bg=CARD,
    fg=PURPLE,
    font=(
        "Segoe UI",
        13,
        "bold"
    )
).pack(
    anchor="w",
    padx=30,
    pady=(28, 8)
)


feedback_frame = tk.Frame(
    right,
    bg=CARD
)

feedback_frame.pack(
    padx=27,
    fill="x"
)


def feedback(value):

    global current_settings

    if not current_settings:

        messagebox.showwarning(
            "Generate First",
            "Generate your sensitivity first."
        )

        return

    if value == "6":

        messagebox.showinfo(
            "Storm Sensitivity",
            "🔥 Perfect! Keep these settings."
        )

        return

    current_settings = adjust_sensitivity(
        current_settings,
        value
    )

    for name, label in result_labels.items():

        label.config(
            text=str(
                current_settings[name]
            )
        )


for text, value in [

    ("⬆️ Too High", "1"),

    ("⬇️ Too Low", "2"),

    ("🐌 Too Slow", "3"),

    ("⚡ Too Fast", "4"),

    ("🎯 Inconsistent", "5"),

    ("✅ Perfect", "6")
]:

    tk.Button(
        feedback_frame,
        text=text,
        command=lambda v=value: feedback(v),
        bg=CARD2,
        fg=WHITE,
        activebackground=PURPLE,
        activeforeground=WHITE,
        relief="flat",
        font=("Segoe UI", 9),
        cursor="hand2"
    ).pack(
        side="left",
        padx=3,
        pady=3
    )


# ============================================================
# DEFAULT DEVICE
# ============================================================

if devices:

    first_brand = list(
        devices.keys()
    )[0]

    brand_var.set(
        first_brand
    )

    update_models()


ram_combo.set(
    "8 GB"
)

style_combo.set(
    "Headshot"
)

update_dpi()

change_mode()


# ============================================================
# MOUSE WHEEL
# ============================================================

def mouse_wheel(event):

    canvas.yview_scroll(
        int(
            -1 * (event.delta / 120)
        ),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# ============================================================
# START
# ============================================================

root.mainloop()