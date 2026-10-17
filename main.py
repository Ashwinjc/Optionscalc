from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.07, 0.10, 1)

class StyledCard(BoxLayout):
    def __init__(self, bg_color=(0.11, 0.14, 0.19, 1), radius=10, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        self.radius = [dp(radius)]
        with self.canvas.before:
            self.col = Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def set_color(self, rgba):
        self.col.rgba = rgba


class CrudeCalc(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(16), spacing=dp(12), **kwargs)

        # Title Header
        header = BoxLayout(orientation='vertical', size_hint_y=0.08)
        header.add_widget(Label(text="CRUDE OPTIONS CALCULATOR", font_size='18sp', bold=True, color=(1, 1, 1, 1)))
        header.add_widget(Label(text="Dynamic Target & Stoploss Engine", font_size='11sp', color=(0.45, 0.55, 0.68, 1)))
        self.add_widget(header)

        # 2x3 Grid Layout (Top 6 Boxes from Blueprint)
        grid = GridLayout(cols=2, spacing=dp(10), size_hint_y=0.42)
        
        self.s0 = self._create_input_tile("ENTERED UNDERLYING", "8951", grid)
        self.p0 = self._create_input_tile("PREMIUM PRICE", "305", grid)
        self.sl_und = self._create_input_tile("SL UNDERLYING", "8945", grid)
        self.tgt_und = self._create_input_tile("TARGET UNDERLYING", "8994", grid)
        self.delta = self._create_input_tile("DELTA", "-0.67", grid)
        self.rrr2 = self._create_input_tile("DEFINED RRR RATIO", "3.0", grid)
        self.add_widget(grid)

        # Switch Strip (Below grid, toggle aligned to the right)
        switch_bar = BoxLayout(size_hint_y=0.06, spacing=dp(8))
        switch_bar.add_widget(Label(
            text="Enable Defined RRR Target", 
            font_size='13sp', 
            bold=True, 
            halign='left', 
            valign='middle',
            color=(0.85, 0.90, 0.98, 1)
        ))
        self.switch = Switch(active=False, size_hint_x=0.28)
        self.switch.bind(active=self.on_switch_toggle)
        switch_bar.add_widget(self.switch)
        self.add_widget(switch_bar)

        # Live Metrics Strip (SL Shift, Target Shift, Calculated RRR)
        self.chip_bar = StyledCard(bg_color=(0.08, 0.11, 0.15, 1), size_hint_y=0.05, padding=[dp(8), 0, dp(8), 0])
        self.metrics_label = Label(text="SL Shift: -- | Target Shift: -- | RRR: --", font_size='12sp', color=(0.6, 0.75, 0.95, 1))
        self.chip_bar.add_widget(self.metrics_label)
        self.add_widget(self.chip_bar)

        # Result Cards Container (Bottom Area)
        self.results_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=0.39)

        # Stop Loss Premium Card (Red)
        self.sl_card = StyledCard(bg_color=(0.84, 0.16, 0.16, 1), orientation='vertical', padding=[dp(12), dp(8), dp(12), dp(8)])
        self.sl_card.add_widget(Label(text="STOP LOSS PREMIUM", font_size='11sp', bold=True, color=(1, 0.85, 0.85, 1), size_hint_y=0.35))
        self.sl_val = Label(text="--", font_size='28sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.sl_card.add_widget(self.sl_val)
        self.results_container.add_widget(self.sl_card)

        # Target Premium Card (Green)
        self.tgt_card = StyledCard(bg_color=(0.10, 0.68, 0.28, 1), orientation='vertical', padding=[dp(12), dp(8), dp(12), dp(8)])
        self.tgt_card.add_widget(Label(text="TARGET PREMIUM", font_size='11sp', bold=True, color=(0.85, 1, 0.85, 1), size_hint_y=0.35))
        self.tgt_val = Label(text="--", font_size='28sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.tgt_card.add_widget(self.tgt_val)
        self.results_container.add_widget(self.tgt_card)

        # Target @ Defined RRR Card (Dynamic Dark Navy Card)
        self.rrr2_card = StyledCard(bg_color=(0.14, 0.18, 0.25, 1), orientation='vertical', padding=[dp(12), dp(8), dp(12), dp(8)])
        self.rrr2_title = Label(text="TARGET @ DEFINED RRR (3.0:1)", font_size='11sp', bold=True, color=(0.7, 0.85, 1, 1), size_hint_y=0.35)
        self.rrr2_val = Label(text="--", font_size='28sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.rrr2_card.add_widget(self.rrr2_title)
        self.rrr2_card.add_widget(self.rrr2_val)
        
        # Initially hidden until switch is toggled
        self.results_container.add_widget(self.rrr2_card)
        self.rrr2_card.opacity = 0
        self.rrr2_card.size_hint_y = 0.001

        self.add_widget(self.results_container)
        self.recalculate()

    def _create_input_tile(self, label_text, default_val, parent_grid):
        tile = StyledCard(orientation='vertical', padding=[dp(10), dp(6), dp(10), dp(6)], spacing=dp(4))
        
        lbl = Label(text=label_text, font_size='9sp', bold=True, color=(0.60, 0.70, 0.82, 1), size_hint_y=0.35, halign='left')
        lbl.bind(size=lbl.setter('text_size'))
        tile.add_widget(lbl)

        ti = TextInput(
            text=default_val,
            multiline=False,
            font_size='16sp',
            bold=True,
            size_hint_y=0.65,
            background_color=(0.17, 0.22, 0.29, 1),
            foreground_color=(1, 1, 1, 1),
            cursor_color=(0.3, 0.6, 1, 1),
            padding=[dp(8), dp(6), dp(8), dp(6)]
        )
        ti.bind(text=self.recalculate)
        tile.add_widget(ti)
        
        parent_grid.add_widget(tile)
        return ti

    def on_switch_toggle(self, instance, value):
        if value:
            self.rrr2_card.opacity = 1
            self.rrr2_card.size_hint_y = 1
        else:
            self.rrr2_card.opacity = 0
            self.rrr2_card.size_hint_y = 0.001
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
