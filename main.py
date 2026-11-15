from datetime import datetime

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider
from kivy.graphics import Color, RoundedRectangle

# Desktop preview size. Android will use its actual screen size.
Window.size = (400, 760)
Window.clearcolor = (0.035, 0.055, 0.10, 1)


class Card(BoxLayout):
    """A simple rounded panel used to group dashboard information."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(14)
        self.spacing = dp(8)
        with self.canvas.before:
            Color(0.075, 0.11, 0.18, 1)
            self.panel = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        self.bind(pos=self._update_panel, size=self._update_panel)

    def _update_panel(self, *_):
        self.panel.pos = self.pos
        self.panel.size = self.size


class IrrigationApp(App):
    def build(self):
        self.title = "Smart Irrigation"
        self.moisture = 45
        self.auto = True
        self.pump = False
        self.history = ["System started — pump OFF"]

        scroll = ScrollView(do_scroll_x=False)
        page = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(18), dp(16), dp(18)],
            spacing=dp(12),
            size_hint_y=None
        )
        page.bind(minimum_height=page.setter("height"))

        heading = Label(
            text="[b]SMART IRRIGATION[/b]\n[color=9AAFC8]SYSTEM DASHBOARD[/color]",
            markup=True,
            font_size="22sp",
            halign="left",
            valign="middle",
            size_hint_y=None,
            height=dp(76)
        )
        page.add_widget(heading)

        # Moisture card
        moisture_card = Card(orientation="vertical", size_hint_y=None, height=dp(190))
        moisture_card.add_widget(Label(
            text="[color=9AAFC8]SOIL MOISTURE[/color]",
            markup=True, font_size="14sp", halign="left",
            size_hint_y=None, height=dp(24)
        ))
        self.moisture_label = Label(
            text="[b]45%[/b]", markup=True, font_size="38sp",
            size_hint_y=None, height=dp(52)
        )
        moisture_card.add_widget(self.moisture_label)
        self.progress = ProgressBar(max=100, value=45, size_hint_y=None, height=dp(16))
        moisture_card.add_widget(self.progress)
        moisture_card.add_widget(Label(
            text="Simulation slider — move to change moisture",
            font_size="12sp", color=(0.65, 0.72, 0.82, 1),
            size_hint_y=None, height=dp(22)
        ))
        self.slider = Slider(min=0, max=100, value=45, size_hint_y=None, height=dp(32))
        self.slider.bind(value=self.update_moisture)
        moisture_card.add_widget(self.slider)
        page.add_widget(moisture_card)

        # Pump and mode status
        status_card = Card(orientation="vertical", size_hint_y=None, height=dp(120))
        status_card.add_widget(Label(
            text="[color=9AAFC8]WATER PUMP STATUS[/color]",
            markup=True, font_size="14sp", size_hint_y=None, height=dp(24)
        ))
        self.pump_label = Label(
            text="[b][color=FFB454]● PUMP OFF[/color][/b]",
            markup=True, font_size="24sp"
        )
        status_card.add_widget(self.pump_label)
        self.mode_label = Label(
            text="MODE: AUTOMATIC", font_size="14sp",
            color=(0.35, 0.82, 1, 1), size_hint_y=None, height=dp(24)
        )
        status_card.add_widget(self.mode_label)
        page.add_widget(status_card)

        # Mode controls
        mode_card = Card(orientation="vertical", size_hint_y=None, height=dp(105))
        mode_card.add_widget(Label(
            text="[color=9AAFC8]CONTROL MODE[/color]", markup=True,
            font_size="14sp", size_hint_y=None, height=dp(22)
        ))
        mode_row = BoxLayout(spacing=dp(8))
        self.auto_btn = self.make_button("AUTOMATIC", (0.05, 0.48, 0.72, 1))
        self.auto_btn.bind(on_press=self.auto_mode)
        self.manual_btn = self.make_button("MANUAL", (0.20, 0.27, 0.38, 1))
        self.manual_btn.bind(on_press=self.manual_mode)
        mode_row.add_widget(self.auto_btn)
        mode_row.add_widget(self.manual_btn)
        mode_card.add_widget(mode_row)
        page.add_widget(mode_card)

        # Manual pump controls
        pump_card = Card(orientation="vertical", size_hint_y=None, height=dp(105))
        pump_card.add_widget(Label(
            text="[color=9AAFC8]MANUAL PUMP CONTROL[/color]", markup=True,
            font_size="14sp", size_hint_y=None, height=dp(22)
        ))
        pump_row = BoxLayout(spacing=dp(8))
        self.on_btn = self.make_button("PUMP ON", (0.08, 0.52, 0.36, 1))
        self.on_btn.bind(on_press=self.pump_on)
        self.off_btn = self.make_button("PUMP OFF", (0.68, 0.22, 0.25, 1))
        self.off_btn.bind(on_press=self.pump_off)
        pump_row.add_widget(self.on_btn)
        pump_row.add_widget(self.off_btn)
        pump_card.add_widget(pump_row)
        page.add_widget(pump_card)

        # History
        history_card = Card(orientation="vertical", size_hint_y=None, height=dp(165))
        history_card.add_widget(Label(
            text="[color=9AAFC8]IRRIGATION ACTIVITY[/color]", markup=True,
            font_size="14sp", size_hint_y=None, height=dp(24)
        ))
        self.history_label = Label(
            text=self.history_text(),
            font_size="12sp",
            color=(0.82, 0.88, 0.95, 1),
            halign="left", valign="top",
            size_hint_y=1
        )
        self.history_label.bind(size=self._fit_history)
        history_card.add_widget(self.history_label)
        page.add_widget(history_card)

        note = Label(
            text="Demo mode: pump controls change the app display only.\nReal pump operation needs Arduino and hardware.",
            font_size="11sp", color=(0.62, 0.70, 0.80, 1),
            halign="center", size_hint_y=None, height=dp(44)
        )
        page.add_widget(note)

        scroll.add_widget(page)
        self.refresh_controls()
        return scroll

    def make_button(self, text, color):
        return Button(
            text=text,
            bold=True,
            font_size="13sp",
            background_normal="",
            background_color=color,
            color=(1, 1, 1, 1)
        )

    def _fit_history(self, label, size):
        label.text_size = (size[0], None)

    def history_text(self):
        return "\n".join(self.history[-7:])

    def add_history(self, message):
        stamp = datetime.now().strftime("%H:%M:%S")
        self.history.append(f"{stamp}  {message}")
        if hasattr(self, "history_label"):
            self.history_label.text = self.history_text()

    def update_moisture(self, _instance, value):
        self.moisture = int(value)
        self.moisture_label.text = f"[b]{self.moisture}%[/b]"
        self.progress.value = self.moisture

        if self.auto:
            if self.moisture < 30:
                self.set_pump(True)
            elif self.moisture > 60:
                self.set_pump(False)

    def set_pump(self, status):
        if self.pump == status:
            return
        self.pump = status
        if status:
            self.pump_label.text = "[b][color=54E39A]● PUMP ON[/color][/b]"
            self.add_history("Pump switched ON")
        else:
            self.pump_label.text = "[b][color=FFB454]● PUMP OFF[/color][/b]"
            self.add_history("Pump switched OFF")

    def refresh_controls(self):
        if not hasattr(self, "on_btn"):
            return
        self.on_btn.disabled = self.auto
        self.off_btn.disabled = self.auto
        self.on_btn.opacity = 0.45 if self.auto else 1
        self.off_btn.opacity = 0.45 if self.auto else 1

    def pump_on(self, _instance):
        if not self.auto:
            self.set_pump(True)

    def pump_off(self, _instance):
        if not self.auto:
            self.set_pump(False)

    def auto_mode(self, _instance):
        self.auto = True
        self.mode_label.text = "MODE: AUTOMATIC"
        self.add_history("Automatic mode selected")
        self.refresh_controls()
        self.update_moisture(None, self.moisture)

    def manual_mode(self, _instance):
        self.auto = False
        self.mode_label.text = "MODE: MANUAL"
        self.add_history("Manual mode selected")
        self.refresh_controls()


if __name__ == "__main__":
    IrrigationApp().run()
