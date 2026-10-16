from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.07, 0.09, 1)

class CrudeCalc(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        
        # Header
        self.add_widget(Label(text="Crude Options Calc", font_size='22sp', bold=True, size_hint_y=None, height=40))
        
        # Input Grid
        grid = GridLayout(cols=2, spacing=8, size_hint_y=None, height=220)
        
        self.s0 = self._make_input("8951", grid, "Entered Underlying:")
        self.p0 = self._make_input("305", grid, "Premium Price:")
        self.sl_und = self._make_input("8945", grid, "SL Underlying:")
        self.tgt_und = self._make_input("8994", grid, "Target Underlying:")
        self.delta = self._make_input("-0.67", grid, "Delta:")
        self.add_widget(grid)

        # Defined RRR toggle
        toggle_box = BoxLayout(size_hint_y=None, height=40)
        toggle_box.add_widget(Label(text="Enable Defined RRR:", halign="left"))
        self.switch = Switch(active=False)
        self.switch.bind(active=self.toggle_rrr)
        toggle_box.add_widget(self.switch)
        self.add_widget(toggle_box)

        # RRR2 Input Box
        self.rrr2_box = BoxLayout(size_hint_y=None, height=35, opacity=0)
        self.rrr2_box.add_widget(Label(text="Defined Ratio (e.g. 3.0):"))
        self.rrr2 = TextInput(text="3.0", multiline=False)
        self.rrr2.bind(text=self.recalculate)
        self.rrr2_box.add_widget(self.rrr2)
        self.add_widget(self.rrr2_box)

        # Cards Output
        self.sl_card = Label(text="SL Premium: --", font_size='18sp', bold=True, color=(1, 0.2, 0.2, 1))
        self.tgt_card = Label(text="Target Premium: --", font_size='18sp', bold=True, color=(0, 1, 0.3, 1))
        self.rrr2_card = Label(text="", font_size='16sp', bold=True, color=(0.8, 0.8, 1, 1))
        
        self.add_widget(self.sl_card)
        self.add_widget(self.tgt_card)
        self.add_widget(self.rrr2_card)

        self.recalculate()

    def _make_input(self, val, grid, label):
        grid.add_widget(Label(text=label, font_size='13sp'))
        ti = TextInput(text=val, multiline=False, font_size='14sp')
        ti.bind(text=self.recalculate)
        grid.add_widget(ti)
        return ti

    def toggle_rrr(self, instance, value):
        self.rrr2_box.opacity = 1 if value else 0
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
            
            self.sl_card.text = f"Stop Loss Premium: {exit_sl:.2f}"
            self.tgt_card.text = f"Target Premium: {exit_tgt:.2f}"
            
            if self.switch.active:
                rrr_val = float(self.rrr2.text)
                risk_pts = abs(P0 - exit_sl)
                tgt_rrr = P0 - (risk_pts * rrr_val) if exit_tgt < P0 else P0 + (risk_pts * rrr_val)
                self.rrr2_card.text = f"Target @ {rrr_val:g}:1 RRR: {tgt_rrr:.2f}"
            else:
                self.rrr2_card.text = ""
        except ValueError:
            pass

class CrudeApp(App):
    def build(self):
        return CrudeCalc()

if __name__ == '__main__':
    CrudeApp().run()