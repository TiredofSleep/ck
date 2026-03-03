"""
ck_sim_widgets.py -- Custom Kivy Widgets for CK Visualization
==============================================================
Operator: LATTICE (1) -- structure you can see.

Custom widgets that make CK's inner life visible:
  - LED circle (operator color + breath pulse)
  - Coherence dial (gauge with G/Y/R bands)
  - Breath wave (sine animation)
  - TL heatmap (10x10 transition matrix)
  - Crystal list (discovered patterns)

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.clock import Clock

from ck_sim.ck_sim_heartbeat import NUM_OPS, OP_NAMES


class CKLEDWidget(Widget):
    """Large circle showing operator color with breath modulation.

    Outer glow -> main circle -> bright center.
    Color set by engine's led_color (already breath-modulated).
    """

    led_color = ListProperty([0.3, 0.8, 1.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update, size=self._update, led_color=self._update)
        Clock.schedule_once(self._update, 0)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            r, g, b = self.led_color
            d = min(self.width, self.height)
            cx = self.x + self.width / 2
            cy = self.y + self.height / 2

            # Ambient glow (very faint, large)
            Color(r, g, b, 0.08)
            Ellipse(pos=(cx - d * 0.50, cy - d * 0.50), size=(d * 1.0, d * 1.0))

            # Outer glow
            Color(r, g, b, 0.15)
            Ellipse(pos=(cx - d * 0.46, cy - d * 0.46), size=(d * 0.92, d * 0.92))

            # Mid glow
            Color(r, g, b, 0.35)
            Ellipse(pos=(cx - d * 0.40, cy - d * 0.40), size=(d * 0.80, d * 0.80))

            # Inner glow
            Color(r, g, b, 0.55)
            Ellipse(pos=(cx - d * 0.35, cy - d * 0.35), size=(d * 0.70, d * 0.70))

            # Main circle
            Color(r, g, b, 1.0)
            Ellipse(pos=(cx - d * 0.30, cy - d * 0.30), size=(d * 0.60, d * 0.60))

            # Bright center highlight
            Color(min(r + 0.3, 1.0), min(g + 0.3, 1.0), min(b + 0.3, 1.0), 0.6)
            Ellipse(pos=(cx - d * 0.14, cy - d * 0.14), size=(d * 0.28, d * 0.28))

            # Hot center
            Color(min(r + 0.5, 1.0), min(g + 0.5, 1.0), min(b + 0.5, 1.0), 0.3)
            Ellipse(pos=(cx - d * 0.06, cy - d * 0.06), size=(d * 0.12, d * 0.12))


class CKCoherenceDial(Widget):
    """Horizontal coherence gauge with R/Y/G zones and T* marker."""

    coherence = NumericProperty(0.0)
    band_name = StringProperty("RED")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update, size=self._update, coherence=self._update)
        Clock.schedule_once(self._update, 0)

    def _update(self, *args):
        self.canvas.clear()
        w, h = self.width, self.height
        x, y = self.x, self.y
        t_star = 5.0 / 7.0

        with self.canvas:
            # Background
            Color(0.08, 0.08, 0.1, 1)
            Rectangle(pos=(x, y), size=(w, h))

            pad = 8
            bar_x = x + pad
            bar_y = y + h * 0.35
            bar_w = w - pad * 2
            bar_h = h * 0.3

            # Zone backgrounds
            # Red zone (0 -> 0.5)
            Color(0.35, 0.08, 0.08, 0.6)
            rw = bar_w * 0.5
            Rectangle(pos=(bar_x, bar_y), size=(rw, bar_h))

            # Yellow zone (0.5 -> T*)
            Color(0.35, 0.3, 0.05, 0.6)
            yw = bar_w * (t_star - 0.5)
            Rectangle(pos=(bar_x + rw, bar_y), size=(yw, bar_h))

            # Green zone (T* -> 1.0)
            Color(0.05, 0.3, 0.1, 0.6)
            gw = bar_w * (1.0 - t_star)
            Rectangle(pos=(bar_x + rw + yw, bar_y), size=(gw, bar_h))

            # Fill bar (actual coherence)
            c = max(0.0, min(1.0, self.coherence))
            fill_w = bar_w * c

            if c >= t_star:
                Color(0.0, 0.85, 0.3, 0.9)
            elif c >= 0.5:
                Color(1.0, 0.7, 0.0, 0.9)
            else:
                Color(1.0, 0.15, 0.1, 0.9)

            Rectangle(pos=(bar_x, bar_y), size=(fill_w, bar_h))

            # T* marker line
            Color(1.0, 1.0, 1.0, 0.7)
            ts_x = bar_x + bar_w * t_star
            Line(points=[ts_x, bar_y - 4, ts_x, bar_y + bar_h + 4], width=1.5)

            # T* label
            Color(1.0, 1.0, 1.0, 0.5)
            Rectangle(pos=(ts_x - 1, bar_y + bar_h + 4), size=(2, 6))

            # Value indicator (bright marker at current C)
            Color(1.0, 1.0, 1.0, 0.9)
            marker_x = bar_x + fill_w
            if marker_x > bar_x + 2:
                Rectangle(pos=(marker_x - 1.5, bar_y - 2), size=(3, bar_h + 4))


class CKBreathWave(Widget):
    """Scrolling breath modulation waveform."""

    modulation = NumericProperty(0.0)
    phase_name = StringProperty("INHALE")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._history = [0.0] * 100
        self.bind(pos=self._update, size=self._update)
        Clock.schedule_once(self._update, 0)

    def update_value(self, mod, phase_name):
        self.modulation = mod
        self.phase_name = phase_name
        self._history.append(mod)
        if len(self._history) > 100:
            self._history = self._history[-100:]
        self._update()

    def _update(self, *args):
        self.canvas.clear()
        w, h = self.width, self.height
        x, y = self.x, self.y

        with self.canvas:
            # Background
            Color(0.08, 0.08, 0.1, 1)
            Rectangle(pos=(x, y), size=(w, h))

            # Center line
            Color(0.2, 0.2, 0.25, 0.5)
            mid_y = y + h * 0.5
            Line(points=[x + 4, mid_y, x + w - 4, mid_y], width=1)

            # Wave line
            n = len(self._history)
            if n > 1 and w > 0:
                Color(0.3, 0.65, 1.0, 0.85)
                points = []
                step = (w - 8) / max(n - 1, 1)
                pad_y = h * 0.1
                range_y = h - pad_y * 2
                for i, val in enumerate(self._history):
                    px = x + 4 + i * step
                    py = y + pad_y + val * range_y
                    points.extend([px, py])
                if len(points) >= 4:
                    Line(points=points, width=1.5)

                # Current value dot
                Color(1.0, 1.0, 1.0, 0.9)
                last_x = x + w - 8
                last_y = y + pad_y + self.modulation * range_y
                Ellipse(pos=(last_x - 4, last_y - 4), size=(8, 8))


class CKHeatmapWidget(Widget):
    """10x10 TL transition heatmap.

    Rows = from_op, columns = to_op.
    Brighter = more transitions.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._matrix = [[0] * NUM_OPS for _ in range(NUM_OPS)]
        self.bind(pos=self._update, size=self._update)
        Clock.schedule_once(self._update, 0)

    def update_matrix(self, matrix):
        self._matrix = matrix
        self._update()

    def _update(self, *args):
        self.canvas.clear()

        max_val = 1
        for row in self._matrix:
            for v in row:
                if v > max_val:
                    max_val = v

        w, h = self.width, self.height
        x, y = self.x, self.y

        # Leave room for axis labels
        label_w = 0
        label_h = 0
        grid_x = x + label_w
        grid_y = y + label_h
        grid_w = w - label_w
        grid_h = h - label_h

        cell_w = grid_w / NUM_OPS
        cell_h = grid_h / NUM_OPS

        with self.canvas:
            # Background
            Color(0.04, 0.04, 0.06, 1)
            Rectangle(pos=(x, y), size=(w, h))

            for i in range(NUM_OPS):
                for j in range(NUM_OPS):
                    val = self._matrix[i][j] / max_val if max_val > 0 else 0

                    # Color ramp: dark -> blue -> cyan -> white
                    if val < 0.01:
                        r, g, b = 0.06, 0.06, 0.08
                    elif val < 0.3:
                        t = val / 0.3
                        r = 0.06 + t * 0.04
                        g = 0.06 + t * 0.25
                        b = 0.08 + t * 0.72
                    elif val < 0.7:
                        t = (val - 0.3) / 0.4
                        r = 0.1 + t * 0.15
                        g = 0.31 + t * 0.49
                        b = 0.8 + t * 0.2
                    else:
                        t = (val - 0.7) / 0.3
                        r = 0.25 + t * 0.75
                        g = 0.8 + t * 0.2
                        b = 1.0

                    Color(min(r, 1), min(g, 1), min(b, 1), 1)
                    cx = grid_x + j * cell_w
                    cy = grid_y + (NUM_OPS - 1 - i) * cell_h
                    Rectangle(pos=(cx + 0.5, cy + 0.5),
                              size=(cell_w - 1, cell_h - 1))

            # Grid lines (subtle)
            Color(0.2, 0.2, 0.25, 0.3)
            for k in range(NUM_OPS + 1):
                lx = grid_x + k * cell_w
                Line(points=[lx, grid_y, lx, grid_y + grid_h], width=0.5)
                ly = grid_y + k * cell_h
                Line(points=[grid_x, ly, grid_x + grid_w, ly], width=0.5)


class CKCrystalList(BoxLayout):
    """Scrollable list of discovered crystals."""

    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_y', None)
        super().__init__(**kwargs)
        self.bind(minimum_height=self.setter('height'))
        self._add_placeholder()

    def _add_placeholder(self):
        lbl = Label(
            text="Observing...",
            size_hint_y=None,
            height=26,
            font_size='11sp',
            color=(0.4, 0.4, 0.5, 1.0),
            italic=True,
        )
        self.add_widget(lbl)

    def update_crystals(self, crystals):
        self.clear_widgets()

        if not crystals:
            self._add_placeholder()
            return

        for cr in crystals[:24]:
            ops_str = ' \u2192 '.join(OP_NAMES[o] for o in cr.ops[:cr.length])
            fuse_str = OP_NAMES[cr.fuse]
            text = (f"[{ops_str}] \u2192 {fuse_str}  "
                    f"({cr.confidence:.1%}  seen:{cr.seen})")
            lbl = Label(
                text=text,
                size_hint_y=None,
                height=24,
                font_size='11sp',
                color=(0.75, 0.85, 1.0, 1.0),
                halign='left',
                valign='middle',
            )
            lbl.bind(size=lbl.setter('text_size'))
            self.add_widget(lbl)
