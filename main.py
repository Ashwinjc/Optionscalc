from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window

# Dark trading background
Window.clearcolor = (0.06, 0.08, 0.11, 1)

class Card(BoxLayout):
    """A card container with rounded corners and background color."""
    def __init__(self, bg_color=(0.12, 0.15, 0.19, 1), radius=[10], **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = radius
        with self.canvas.before:
            self.col = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_bg_color(self, color):
        self.col.rgba = color

class CrudeCalc(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(do_scroll_x=False, **kwargs)
        
        # Root vertical layout inside scroll view
        root = BoxLayout(orientation='vertical', padding=[16, 20, 16, 20], spacing=14, size_hint_y=None)
        root.bind(minimum_height=root.setter('height'))

        # Header Title
        title_box = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        title_box.add_widget(Label(text="CRUDE OPTIONS CALCULATOR", font_size='18sp', bold=True, color=(1, 1, 1, 1)))
        title_box.add_widget(Label(text="Dynamic Target & Stoploss Engine", font_size='12sp', color=(0.5, 0.6, 0.7, 1)))
        root.add_widget(title_box)

        # --- Card 1: Input Parameters ---
        input_card = Card(orientation='vertical', padding=[14, 14, 14, 14], spacing=10, size_hint_y=None, height=270)
        
        grid = GridLayout(cols=2, spacing=[10, 8], size_hint_y=None, height=240)
        self.s0 = self._make_input_row("Entered Underlying", "8951", grid)
        self.p0 = self._make_input_row("Premium Price", "305", grid)
        self.sl_und = self._make_input_row("SL Underlying", "8945", grid)
        self.tgt_und = self._make_input_row("Target Underlying", "8994", grid)
        self.delta = self._make_input_row("Option Delta", "-0.67", grid)
        
        input_card.add_widget(grid)
        root.add_widget(input_card)

        # --- Card 2: Defined RRR Toggle Card ---
        rrr_card = Card(orientation='vertical', padding=[14, 10, 14, 10], spacing=6, size_hint_y=None, height=95)
        
        switch_row = BoxLayout(size_hint_y=None, height=36)
        switch_row.add_widget(Label(text="Enable Defined RRR", font_size='14sp', bold=True, halign='left', valign='middle'))
        self.switch = Switch(active=False, size_hint_x=0.3)
        self.switch.bind(active=self.toggle_rrr)
        switch_row.add_widget(self.switch)
        rrr_card.add_widget(switch_row)

        self.rrr2_row = BoxLayout(size_hint_y=None, height=36, opacity=0)
        self.rrr2_row.add_widget(Label(text="Target Ratio (e.g. 3.0)", font_size='13sp', color=(0.6, 0.7, 0.8, 1)))
        self.rrr2 = TextInput(
            text="3.0", 
            multiline=False, 
            font_size='14sp', 
            size_hint_x=0.45,
            background_color=(0.18, 0.22, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[8, 6, 8, 6]
        )
        self.rrr2.bind(text=self.recalculate)
        self.rrr2_row.add_widget(self.rrr2)
        rrr_card.add_widget(self.rrr2_row)
        root.add_widget(rrr_card)

        # --- Metrics Chip Row (SL Shift | Target Shift | RRR) ---
        self.metrics_card = Card(bg_color=(0.09, 0.12, 0.16, 1), padding=[8, 8, 8, 8], size_hint_y=None, height=44)
        self.metrics_label = Label(text="SL: --  |  Target: --  |  RRR: --", font_size='12sp', bold=True, color=(0.6, 0.75, 0.9, 1))
        self.metrics_card.add_widget(self.metrics_label)
        root.add_widget(self.metrics_card)

        # --- Card 3: Stop Loss Premium (Red) ---
        self.sl_box = Card(bg_color=(0.82, 0.15, 0.15, 1), orientation='vertical', padding=[12, 10, 12, 10], size_hint_y=None, height=75)
        self.sl_box.add_widget(Label(text="STOP LOSS PREMIUM", font_size='11sp', bold=True, color=(1, 0.85, 0.85, 1)))
        self.sl_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1))
        self.sl_box.add_widget(self.sl_val)
        root.add_widget(self.sl_box)

        # --- Card 4: Target Premium (Green) ---
        self.tgt_box = Card(bg_color=(0.10, 0.68, 0.28, 1), orientation='vertical', padding=[12, 10, 12, 10], size_hint_y=None, height=75)
        self.tgt_box.add_widget(Label(text="TARGET PREMIUM", font_size='11sp', bold=True, color=(0.85, 1, 0.85, 1)))
        self.tgt_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1))
        self.tgt_box.add_widget(self.tgt_val)
        root.add_widget(self.tgt_box)

        # --- Card 5: Defined RRR Target Card ---
        self.rrr2_box = Card(bg_color=(0.15, 0.20, 0.28, 1), orientation='vertical', padding=[12, 10, 12, 10], size_hint_y=None, height=0, opacity=0)
        self.rrr2_title = Label(text="TARGET @ DEFINED RRR", font_size='11sp', bold=True, color=(0.7, 0.85, 1, 1))
        self.rrr2_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1))
        self.rrr2_box.add_widget(self.rrr2_title)
        self.rrr2_box.add_widget(self.rrr2_val)
        root.add_widget(self.rrr2_box)

        self.add_widget(root)
        self.recalculate()

    def _make_input_row(self, label_text, default_val, grid):
        lbl = Label(text=label_text, font_size='13sp', halign='left', valign='middle', color=(0.8, 0.85, 0.9, 1))
        lbl.bind(size=lbl.setter('text_size'))
        grid.add_widget(lbl)
        
        ti = TextInput(
            text=default_val, 
            multiline=False, 
            font_size='14sp',
            background_color=(0.18, 0.22, 0.28, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(1, 1, 1, 1),
            padding=[8, 8, 8, 8]
        )
        ti.bind(text=self.recalculate)
        grid.add_widget(ti)
        return ti

    def toggle_rrr(self, instance, value):
        if value:
            self.rrr2_row.opacity = 1
            self.rrr2_box.height = 75
            self.rrr2_box.opacity = 1
        else:
            self.rrr2_row.opacity = 0
            self.rrr2_box.height = 0
            self.rrr2_box.opacity = 0
        self.recalculate()

    def recalculate(self, *args):
        try:
            S0 = float(self.s0.text)
            P0 = float(self.p0.text)
            S_sl = float(self.sl_und.text)
            S_tgt = float(self.tgt_und.text)
            delta = float(self.delta.text)
            
            prem_sl_pts = -delta * (S_sl - S0)
            prem_tgt_pts = delta * (S_tgt - S0)
            
            exit_sl = P0 - prem_sl_pts if prem_sl_pts > 0 else P0 + abs(prem_sl_pts)
            exit_tgt = P0 + prem_tgt_pts
            
            rrr = abs(prem_tgt_pts / prem_sl_pts) if prem_sl_pts != 0 else 0.0
            
            self.metrics_label.text = f"SL Shift: {-prem_sl_pts:+.2f}  |  Tgt Shift: {prem_tgt_pts:+.2f}  |  RRR: {rrr:.2f}:1"
            self.sl_val.text = f"{exit_sl:.2f}"
            self.tgt_val.text = f"{exit_tgt:.2f}"
            
            if self.switch.active:
                rrr_val = float(self.rrr2.text)
                risk_pts = abs(P0 - exit_sl)
                tgt_rrr = P0 - (risk_pts * rrr_val) if exit_tgt < P0 else P0 + (risk_pts * rrr_val)
                self.rrr2_title.text = f"TARGET @ DEFINED RRR ({rrr_val:g}:1)"
                self.rrr2_val.text = f"{tgt_rrr:.2f}"
        except ValueError:
            pass

class CrudeApp(App):
    def build(self):
        return CrudeCalc()

if __name__ == '__main__':
    CrudeApp().run()
