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


class CrudeCalc(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=dp(14), spacing=dp(10), **kwargs)

        # 1. Title Header
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(48))
        header.add_widget(Label(text="CRUDE OPTIONS CALCULATOR", font_size='18sp', bold=True, color=(1, 1, 1, 1)))
        header.add_widget(Label(text="Dynamic Target & Stoploss Engine", font_size='11sp', color=(0.45, 0.55, 0.68, 1)))
        self.add_widget(header)

        # 2. 2x3 Grid Layout (Top 6 Boxes from Blueprint)
        grid = GridLayout(cols=2, spacing=dp(8), size_hint_y=0.45)
        
        self.s0 = self._create_tile("ENTERED UNDERLYING", "8951", grid)
        self.p0 = self._create_tile("PREMIUM PRICE", "305", grid)
        self.sl_und = self._create_tile("SL UNDERLYING", "8945", grid)
        self.tgt_und = self._create_tile("TARGET UNDERLYING", "8994", grid)
        self.delta = self._create_tile("DELTA", "-0.67", grid)
        self.rrr2 = self._create_tile("DEFINED RRR RATIO", "3.0", grid)
        self.add_widget(grid)

        # 3. Switch Strip
        switch_bar = BoxLayout(size_hint_y=None, height=dp(38), spacing=dp(8))
        switch_bar.add_widget(Label(
            text="Enable Defined RRR Target", 
            font_size='13sp', 
            bold=True, 
            color=(0.85, 0.90, 0.98, 1)
        ))
        self.switch = Switch(active=False, size_hint_x=0.28)
        self.switch.bind(active=self.on_switch_toggle)
        switch_bar.add_widget(self.switch)
        self.add_widget(switch_bar)

        # 4. Shift & RRR Metrics Strip
        self.chip_bar = StyledCard(bg_color=(0.08, 0.11, 0.15, 1), size_hint_y=None, height=dp(32))
        self.metrics_label = Label(text="SL Shift: -- | Target Shift: -- | RRR: --", font_size='11sp', color=(0.6, 0.75, 0.95, 1))
        self.chip_bar.add_widget(self.metrics_label)
        self.add_widget(self.chip_bar)

        # 5. Result Cards Container
        self.results_container = BoxLayout(orientation='vertical', spacing=dp(8), size_hint_y=0.45)

        # Stop Loss Premium Card (Red)
        self.sl_card = StyledCard(bg_color=(0.84, 0.16, 0.16, 1), orientation='vertical', padding=[dp(8), dp(6), dp(8), dp(6)])
        self.sl_card.add_widget(Label(text="STOP LOSS PREMIUM", font_size='11sp', bold=True, color=(1, 0.85, 0.85, 1), size_hint_y=0.35))
        self.sl_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.sl_card.add_widget(self.sl_val)
        self.results_container.add_widget(self.sl_card)

        # Target Premium Card (Green)
        self.tgt_card = StyledCard(bg_color=(0.10, 0.68, 0.28, 1), orientation='vertical', padding=[dp(8), dp(6), dp(8), dp(6)])
        self.tgt_card.add_widget(Label(text="TARGET PREMIUM", font_size='11sp', bold=True, color=(0.85, 1, 0.85, 1), size_hint_y=0.35))
        self.tgt_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.tgt_card.add_widget(self.tgt_val)
        self.results_container.add_widget(self.tgt_card)

        # Defined RRR Target Card
        self.rrr2_card = StyledCard(bg_color=(0.14, 0.18, 0.25, 1), orientation='vertical', padding=[dp(8), dp(6), dp(8), dp(6)])
        self.rrr2_title = Label(text="TARGET @ DEFINED RRR (3.0:1)", font_size='11sp', bold=True, color=(0.7, 0.85, 1, 1), size_hint_y=0.35)
        self.rrr2_val = Label(text="--", font_size='26sp', bold=True, color=(1, 1, 1, 1), size_hint_y=0.65)
        self.rrr2_card.add_widget(self.rrr2_title)
        self.rrr2_card.add_widget(self.rrr2_val)
        
        # Default state: do not add to container until switched on
        self.add_widget(self.results_container)
        self.recalculate()

    def _create_tile(self, label_text, default_val, parent_grid):
        tile = StyledCard(orientation='vertical', padding=[dp(8), dp(4), dp(8), dp(4)], spacing=dp(2))
        
        lbl = Label(text=label_text, font_size='9sp', bold=True, color=(0.60, 0.70, 0.82, 1), size_hint_y=0.35)
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
            padding=[dp(6), dp(4), dp(6), dp(4)]
        )
        ti.bind(text=self.recalculate)
        tile.add_widget(ti)
        
        parent_grid.add_widget(tile)
        return ti

    def on_switch_toggle(self, instance, value):
        if value:
            if self.rrr2_card not in self.results_container.children:
                self.results_container.add_widget(self.rrr2_card)
        else:
            if self.rrr2_card in self.results_container.children:
                self.results_container.remove_widget(self.rrr2_card)
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

            self.metrics_label.text = f"SL Shift
