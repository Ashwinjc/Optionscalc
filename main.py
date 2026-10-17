from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

KV = """
#:import dp kivy.metrics.dp

<InputTile@BoxLayout>:
    orientation: 'vertical'
    padding: [dp(8), dp(6), dp(8), dp(6)]
    spacing: dp(4)
    label_text: ''
    default_text: ''
    input_ref: input_field
    canvas.before:
        Color:
            rgba: 0.12, 0.15, 0.20, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
    Label:
        text: root.label_text
        font_size: '9sp'
        bold: True
        color: 0.65, 0.75, 0.85, 1
        size_hint_y: 0.35
        halign: 'left'
        text_size: self.size
    TextInput:
        id: input_field
        text: root.default_text
        multiline: False
        font_size: '16sp'
        bold: True
        input_filter: 'float'
        input_type: 'number'
        size_hint_y: 0.65
        background_normal: ''
        background_color: 0.18, 0.22, 0.28, 1
        foreground_color: 1, 1, 1, 1
        cursor_color: 0.3, 0.6, 1, 1
        padding: [dp(6), dp(6), dp(6), dp(6)]

<CrudeCalcRoot>:
    orientation: 'vertical'
    padding: dp(14)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.06, 0.08, 0.11, 1
        Rectangle:
            pos: self.pos
            size: self.size

    # Title
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: dp(45)
        Label:
            text: "CRUDE OPTIONS CALCULATOR"
            font_size: '18sp'
            bold: True
            color: 1, 1, 1, 1
        Label:
            text: "Target & Stoploss Engine"
            font_size: '11sp'
            color: 0.5, 0.6, 0.7, 1

    # 2x3 Input Grid
    GridLayout:
        cols: 2
        spacing: dp(8)
        size_hint_y: 0.44

        InputTile:
            id: s0_tile
            label_text: "ENTERED UNDERLYING"
            default_text: "8951"
        InputTile:
            id: p0_tile
            label_text: "PREMIUM PRICE"
            default_text: "305"
        InputTile:
            id: sl_und_tile
            label_text: "SL UNDERLYING"
            default_text: "8945"
        InputTile:
            id: tgt_und_tile
            label_text: "TARGET UNDERLYING"
            default_text: "8994"
        InputTile:
            id: delta_tile
            label_text: "DELTA"
            default_text: "-0.67"
        InputTile:
            id: rrr2_tile
            label_text: "DEFINED RRR RATIO"
            default_text: "3.0"

    # Switch Row
    BoxLayout:
        size_hint_y: None
        height: dp(36)
        spacing: dp(8)
        Label:
            text: "Enable Defined RRR Target"
            font_size: '13sp'
            bold: True
            color: 0.85, 0.90, 0.98, 1
            halign: 'left'
            text_size: self.size
            valign: 'middle'
        Switch:
            id: rrr_switch
            active: False
            size_hint_x: 0.28
            on_active: root.recalculate()

    # Metrics Chip
    BoxLayout:
        size_hint_y: None
        height: dp(30)
        canvas.before:
            Color:
                rgba: 0.10, 0.13, 0.17, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(6)]
        Label:
            id: metrics_label
            text: "SL Shift: --  |  Target Shift: --  |  RRR: --"
            font_size: '11sp'
            color: 0.6, 0.75, 0.95, 1

    # Output Cards
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(8)
        size_hint_y: 0.42

        # SL Card (Red)
        BoxLayout:
            orientation: 'vertical'
            padding: [dp(10), dp(6), dp(10), dp(6)]
            canvas.before:
                Color:
                    rgba: 0.82, 0.15, 0.15, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(8)]
            Label:
                text: "STOP LOSS PREMIUM"
                font_size: '11sp'
                bold: True
                color: 1, 0.85, 0.85, 1
                size_hint_y: 0.35
            Label:
                id: sl_val
                text: "300.98"
                font_size: '28sp'
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: 0.65

        # Target Card (Green)
        BoxLayout:
            orientation: 'vertical'
            padding: [dp(10), dp(6), dp(10), dp(6)]
            canvas.before:
                Color:
                    rgba: 0.10, 0.68, 0.28, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(8)]
            Label:
                text: "TARGET PREMIUM"
                font_size: '11sp'
                bold: True
                color: 0.85, 1, 0.85, 1
                size_hint_y: 0.35
            Label:
                id: tgt_val
                text: "276.19"
                font_size: '28sp'
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: 0.65

        # Defined RRR Card (Dark Slate)
        BoxLayout:
            id: rrr2_box
            orientation: 'vertical'
            padding: [dp(10), dp(6), dp(10), dp(6)]
            opacity: 0.25
            canvas.before:
                Color:
                    rgba: 0.14, 0.18, 0.25, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(8)]
            Label:
                id: rrr2_title
                text: "TARGET @ DEFINED RRR (3.0:1)"
                font_size: '11sp'
                bold: True
                color: 0.7, 0.85, 1, 1
                size_hint_y: 0.35
            Label:
                id: rrr2_val
                text: "--"
                font_size: '28sp'
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: 0.65
"""

Builder.load_string(KV)

class CrudeCalcRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Bind inputs to recalculate on text change
        for tile in [self.ids.s0_tile, self.ids.p0_tile, self.ids.sl_und_tile, 
                     self.ids.tgt_und_tile, self.ids.delta_tile, self.ids.rrr2_tile]:
            tile.input_ref.bind(text=self.recalculate)
        self.recalculate()

    def recalculate(self, *args):
        try:
            S0 = float(self.ids.s0_tile.input_ref.text)
            P0 = float(self.ids.p0_tile.input_ref.text)
            S_sl = float(self.ids.sl_und_tile.input_ref.text)
            S_tgt = float(self.ids.tgt_und_tile.input_ref.text)
            delta = float(self.ids.delta_tile.input_ref.text)

            prem_sl_pts = -delta * (S_sl - S0)
            prem_tgt_pts = delta * (S_tgt - S0)

            exit_sl = P0 - prem_sl_pts if prem_sl_pts > 0 else P0 + abs(prem_sl_pts)
            exit_tgt = P0 + prem_tgt_pts

            rrr = abs(prem_tgt_pts / prem_sl_pts) if prem_sl_pts != 0 else 0.0

            self.ids.metrics_label.text = f"SL Shift: {-prem_sl_pts:+.2f}  |  Tgt Shift: {prem_tgt_pts:+.2f}  |  RRR: {rrr:.2f}:1"
            self.ids.sl_val.text = f"{exit_sl:.2f}"
            self.ids.tgt_val.text = f"{exit_tgt:.2f}"

            if self.ids.rrr_switch.active:
                self.ids.rrr2_box.opacity = 1.0
                rrr_val = float(self.ids.rrr2_tile.input_ref.text)
                risk_pts = abs(P0 - exit_sl)
                tgt_rrr = P0 - (risk_pts * rrr_val) if exit_tgt < P0 else P0 + (risk_pts * rrr_val)
                self.ids.rrr2_title.text = f"TARGET @ DEFINED RRR ({rrr_val:g}:1)"
                self.ids.rrr2_val.text = f"{tgt_rrr:.2f}"
            else:
                self.ids.rrr2_box.opacity = 0.25
                self.ids.rrr2_val.text = "--"
        except Exception:
            pass

class CrudeApp(App):
    def build(self):
        return CrudeCalcRoot()

if __name__ == '__main__':
    CrudeApp().run()
