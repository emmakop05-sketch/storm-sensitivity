import json
import os

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# ============================================================
# STORM SENSITIVITY - ANDROID
# ============================================================

APP_NAME = "🌩️ STORM SENSITIVITY"

# ============================================================
# LOAD DEVICE DATABASE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEVICE_FILE = os.path.join(BASE_DIR, "devices.json")

try:
    with open(DEVICE_FILE, "r", encoding="utf-8") as f:
        devices = json.load(f)

except Exception:
    devices = {}


# ============================================================
# SENSITIVITY ENGINE
# ============================================================

def clamp(value, minimum=1, maximum=200):
    return max(minimum, min(maximum, round(value)))


def calculate_sensitivity(
    device,
    dpi,
    ram,
    refresh_rate,
    finger_layout,
    play_style,
    use_dpi=True
):

    general = 150

    performance = device.get("performance", 5)
    general += performance - 5

    # Refresh rate
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

    # RAM
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

    # DPI
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

    # Finger layout
    if finger_layout == "4 Finger":
        general += 6
    elif finger_layout == "3 Finger":
        general += 3
    elif finger_layout == "2 Finger":
        general -= 2

    # Play style
    if play_style == "Headshot":
        general += 6
    elif play_style == "Aggressive":
        general += 8
    elif play_style == "Balanced":
        general += 2
    elif play_style == "Sniper":
        general -= 8

    general = clamp(general)

    return {
        "General": general,
        "Red Dot": clamp(general - 5),
        "2x Scope": clamp(general - 16),
        "4x Scope": clamp(general - 27),
        "Sniper Scope": clamp(general - 57),
        "Free Look": clamp(general - 8)
    }


# ============================================================
# DPI RECOMMENDATION
# ============================================================

def recommended_dpi(device, current_dpi, play_style):

    minimum = device.get("dpi_min", 400)
    maximum = device.get("dpi_max", 650)

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

    lower = max(minimum, lower)
    upper = min(maximum, upper)

    return f"{lower} - {upper}"


# ============================================================
# FEEDBACK
# ============================================================

def adjust_sensitivity(settings, feedback):

    updated = settings.copy()

    changes = {
        "1": -5,
        "2": 5,
        "3": 4,
        "4": -4,
        "5": 2
    }

    change = changes.get(feedback, 0)

    for key in updated:
        updated[key] = clamp(
            updated[key] + change
        )

    return updated


# ============================================================
# KIVY UI
# ============================================================

KV = r'''

#:import dp kivy.metrics.dp

<StormLayout>:

    orientation: "vertical"
    padding: dp(15)
    spacing: dp(10)

    canvas.before:
        Color:
            rgba: 0.035, 0.024, 0.067, 1
        Rectangle:
            pos: self.pos
            size: self.size

    ScrollView:

        do_scroll_x: False

        GridLayout:

            cols: 1
            spacing: dp(12)
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "🌩️ STORM SENSITIVITY"
                font_size: dp(26)
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(50)

            Label:
                text: "Smart Free Fire Sensitivity & DPI Generator"
                color: 0.67, 0.64, 0.72, 1
                size_hint_y: None
                height: dp(30)

            Label:
                text: "📱 PHONE BRAND"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            Spinner:
                id: brand
                text: "Select Brand"
                values: root.brands
                size_hint_y: None
                height: dp(48)
                background_color: 0.11, 0.08, 0.16, 1
                color: 1, 1, 1, 1
                on_text: root.update_models(self.text)

            Label:
                text: "🔎 PHONE MODEL"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            Spinner:
                id: model
                text: "Select Model"
                values: root.models
                size_hint_y: None
                height: dp(48)
                background_color: 0.11, 0.08, 0.16, 1
                color: 1, 1, 1, 1

            Label:
                text: "🎚️ DPI"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            TextInput:
                id: dpi
                text: "460"
                input_filter: "int"
                multiline: False
                size_hint_y: None
                height: dp(48)

            Label:
                text: "💾 RAM"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            Spinner:
                id: ram
                text: "8 GB"
                values: ["2 GB", "3 GB", "4 GB", "6 GB", "8 GB", "12 GB", "16 GB", "24 GB"]
                size_hint_y: None
                height: dp(48)

            Label:
                text: "👆 FINGER LAYOUT"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            Spinner:
                id: finger
                text: "4 Finger"
                values: ["2 Finger", "3 Finger", "4 Finger"]
                size_hint_y: None
                height: dp(48)

            Label:
                text: "🎯 PLAY STYLE"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(35)

            Spinner:
                id: style
                text: "Headshot"
                values: ["Headshot", "Aggressive", "Balanced", "Sniper"]
                size_hint_y: None
                height: dp(48)

            Button:
                text: "🔥 GENERATE SENSITIVITY"
                bold: True
                background_color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(55)
                on_release: root.generate()

            Label:
                text: "🎯 YOUR STORM SETTINGS"
                bold: True
                font_size: dp(22)
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(45)

            Label:
                id: phone_result
                text: "Choose your phone and generate your settings."
                color: 0.67, 0.64, 0.72, 1
                size_hint_y: None
                height: dp(45)

            Label:
                id: general
                text: "General: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: red_dot
                text: "Red Dot: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: scope2
                text: "2x Scope: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: scope4
                text: "4x Scope: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: sniper
                text: "Sniper Scope: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: free
                text: "Free Look: --"
                font_size: dp(19)
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: dpi_result
                text: "🎚️ Recommended DPI: --"
                bold: True
                color: 0.13, 0.77, 0.37, 1
                size_hint_y: None
                height: dp(40)

            Label:
                id: match
                text: "⚡ Storm Device Match: --"
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(40)

            Label:
                text: "🔄 AIM FEEDBACK"
                bold: True
                color: 0.55, 0.36, 0.96, 1
                size_hint_y: None
                height: dp(40)

            GridLayout:
                cols: 2
                spacing: dp(7)
                size_hint_y: None
                height: dp(110)

                Button:
                    text: "⬆️ Too High"
                    on_release: root.feedback("1")

                Button:
                    text: "⬇️ Too Low"
                    on_release: root.feedback("2")

                Button:
                    text: "🐌 Too Slow"
                    on_release: root.feedback("3")

                Button:
                    text: "⚡ Too Fast"
                    on_release: root.feedback("4")

                Button:
                    text: "🎯 Inconsistent"
                    on_release: root.feedback("5")

                Button:
                    text: "✅ Perfect"
                    on_release: root.feedback("6")
'''


# ============================================================
# MAIN LAYOUT
# ============================================================

class StormLayout(BoxLayout):

    brands = StringProperty([])
    models = StringProperty([])

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.brands = list(devices.keys())

        self.current_settings = {}

    # --------------------------------------------------------
    # UPDATE MODELS
    # --------------------------------------------------------

    def update_models(self, brand):

        if brand in devices:

            self.models = list(
                devices[brand].keys()
            )

        else:

            self.models = []

    # --------------------------------------------------------
    # POPUP
    # --------------------------------------------------------

    def popup(self, title, text):

        Popup(
            title=title,
            content=Label(
                text=text
            ),
            size_hint=(0.85, 0.35)
        ).open()

    # --------------------------------------------------------
    # GENERATE
    # --------------------------------------------------------

    def generate(self):

        brand = self.ids.brand.text
        model = self.ids.model.text

        if brand not in devices:

            self.popup(
                "Phone Missing",
                "Please select your phone brand."
            )

            return

        if model not in devices[brand]:

            self.popup(
                "Phone Missing",
                "Please select your phone model."
            )

            return

        try:

            dpi = int(
                self.ids.dpi.text
            )

        except ValueError:

            self.popup(
                "DPI Error",
                "DPI must be a number."
            )

            return

        if dpi <= 0:

            self.popup(
                "DPI Error",
                "Enter a valid DPI."
            )

            return

        try:

            ram = int(
                self.ids.ram.text.split()[0]
            )

        except ValueError:

            self.popup(
                "RAM Error",
                "Select a valid RAM."
            )

            return

        finger = self.ids.finger.text

        style = self.ids.style.text

        device = devices[brand][model]

        refresh_rate = device.get(
            "refresh_rate",
            60
        )

        self.current_settings = calculate_sensitivity(

            device=device,

            dpi=dpi,

            ram=ram,

            refresh_rate=refresh_rate,

            finger_layout=finger,

            play_style=style,

            use_dpi=True
        )

        settings = self.current_settings

        self.ids.general.text = (
            f"General: {settings['General']}"
        )

        self.ids.red_dot.text = (
            f"Red Dot: {settings['Red Dot']}"
        )

        self.ids.scope2.text = (
            f"2x Scope: {settings['2x Scope']}"
        )

        self.ids.scope4.text = (
            f"4x Scope: {settings['4x Scope']}"
        )

        self.ids.sniper.text = (
            f"Sniper Scope: {settings['Sniper Scope']}"
        )

        self.ids.free.text = (
            f"Free Look: {settings['Free Look']}"
        )

        self.ids.phone_result.text = (
            f"📱 {brand} {model} • "
            f"{refresh_rate} Hz • "
            f"{ram} GB RAM • "
            f"{finger} • {style}"
        )

        dpi_range = recommended_dpi(
            device,
            dpi,
            style
        )

        self.ids.dpi_result.text = (
            f"🎚️ Recommended DPI: {dpi_range}"
        )

        performance = device.get(
            "performance",
            5
        )

        score = 60 + performance * 3

        if refresh_rate >= 120:
            score += 8

        elif refresh_rate >= 90:
            score += 5

        score = max(
            50,
            min(score, 98)
        )

        self.ids.match.text = (
            f"⚡ Storm Device Match: {score}%"
        )

    # --------------------------------------------------------
    # FEEDBACK
    # --------------------------------------------------------

    def feedback(self, value):

        if not self.current_settings:

            self.popup(
                "Generate First",
                "Generate your sensitivity first."
            )

            return

        if value == "6":

            self.popup(
                "Storm Sensitivity",
                "🔥 Perfect! Keep these settings."
            )

            return

        self.current_settings = adjust_sensitivity(
            self.current_settings,
            value
        )

        settings = self.current_settings

        self.ids.general.text = (
            f"General: {settings['General']}"
        )

        self.ids.red_dot.text = (
            f"Red Dot: {settings['Red Dot']}"
        )

        self.ids.scope2.text = (
            f"2x Scope: {settings['2x Scope']}"
        )

        self.ids.scope4.text = (
            f"4x Scope: {settings['4x Scope']}"
        )

        self.ids.sniper.text = (
            f"Sniper Scope: {settings['Sniper Scope']}"
        )

        self.ids.free.text = (
            f"Free Look: {settings['Free Look']}"
        )


# ============================================================
# APP
# ============================================================

class StormSensitivityApp(App):

    title = "Storm Sensitivity"

    def build(self):

        return Builder.load_string(
            KV
        )


if __name__ == "__main__":

    StormSensitivityApp().run()
