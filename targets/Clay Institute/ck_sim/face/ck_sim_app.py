"""
ck_sim_app.py -- CK Coherence Machine Kivy Application
========================================================
Operator: HARMONY (7) -- where everything comes together.

Two-screen app:
  Screen 1: CHAT    -- talk to CK (default, grandma-friendly)
  Screen 2: DASHBOARD -- CK's inner life (engineer view)

CK is a synthetic organism. You raise him, not program him.

Run:  python -m ck_sim.ck_sim_app

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import sys

# Parse CK's args BEFORE Kivy eats them
_ck_study_topic = None
_ck_study_hours = 8.0
_clean_argv = [sys.argv[0]]
_args = sys.argv[1:]
_i = 0
while _i < len(_args):
    if _args[_i] == '--study' and _i + 1 < len(_args):
        _ck_study_topic = _args[_i + 1]
        _i += 2
    elif _args[_i] == '--hours' and _i + 1 < len(_args):
        try:
            _ck_study_hours = float(_args[_i + 1])
        except ValueError:
            pass
        _i += 2
    else:
        _clean_argv.append(_args[_i])
        _i += 1
sys.argv = _clean_argv  # Give Kivy only what it understands

from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Rectangle

# CK runs a 50Hz engine + rich UI -- Kivy's default iteration limit is too low
Clock.max_iteration = 30

from ck_sim.ck_sim_engine import CKSimEngine
from ck_sim.ck_sim_heartbeat import OP_NAMES
from ck_sim.ck_sim_audio import AudioEngine
from ck_sim.ck_sim_ears import EarsEngine
from ck_sim.ck_emotion import EMOTION_COLORS
# Import widgets so Kivy registers them before kv parsing
from ck_sim.ck_sim_widgets import (  # noqa: F401
    CKLEDWidget, CKCoherenceDial, CKBreathWave,
    CKHeatmapWidget, CKCrystalList,
)

KV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ck_sim.kv')


# ================================================================
#  ROOT WIDGET (ScreenManager container)
# ================================================================

class CKRootWidget(BoxLayout):
    """Root widget containing the ScreenManager."""
    manager = ObjectProperty(None)


# ================================================================
#  SCREEN 1: CHAT
# ================================================================

class CKChatScreen(Screen):
    """Chat screen -- talk to CK. Default screen for everyone."""
    chat_scroll = ObjectProperty(None)
    chat_container = ObjectProperty(None)
    text_input = ObjectProperty(None)
    emotion_dot = ObjectProperty(None)
    stage_label = ObjectProperty(None)
    mood_label = ObjectProperty(None)
    bond_label = ObjectProperty(None)
    study_label = ObjectProperty(None)
    chat_mic_btn = ObjectProperty(None)


# ================================================================
#  SCREEN 2: DASHBOARD
# ================================================================

class CKDashScreen(Screen):
    """Dashboard screen -- CK's inner life. For engineers."""
    led_widget = ObjectProperty(None)
    coherence_dial = ObjectProperty(None)
    breath_wave = ObjectProperty(None)
    heatmap = ObjectProperty(None)
    crystal_scroll = ObjectProperty(None)
    crystal_list = ObjectProperty(None)

    mode_label = ObjectProperty(None)
    operator_label = ObjectProperty(None)
    coherence_label = ObjectProperty(None)
    body_label = ObjectProperty(None)
    breath_label = ObjectProperty(None)
    entropy_label = ObjectProperty(None)
    tick_label = ObjectProperty(None)
    ear_label = ObjectProperty(None)
    speaker_btn = ObjectProperty(None)
    mic_btn = ObjectProperty(None)
    btq_label = ObjectProperty(None)
    emotion_label = ObjectProperty(None)
    organism_label = ObjectProperty(None)
    sense_label = ObjectProperty(None)


# ================================================================
#  CHAT MESSAGE WIDGET
# ================================================================

class ChatBubble(BoxLayout):
    """A single chat message bubble."""

    def __init__(self, sender: str, text: str, emotion_color=None, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('padding', [6, 3, 6, 3])
        super().__init__(**kwargs)

        is_ck = (sender == 'ck')

        # Message label -- text wrapping uses text_size bound to parent width
        lbl = Label(
            text=text,
            size_hint_y=None,
            size_hint_x=1,
            font_size='14sp',
            color=(0.75, 0.85, 1.0, 1.0) if is_ck else (0.8, 0.8, 0.85, 1.0),
            halign='left' if is_ck else 'right',
            valign='top',
            markup=False,
        )
        self._lbl = lbl

        # Key fix: bind text wrapping to PARENT width, not own size.
        # This avoids the chicken-and-egg problem where label has no
        # width yet when texture_size first fires.
        def _rewrap(inst, width):
            # Set text_size width so Kivy wraps the text, leave height None
            lbl.text_size = (width - 12, None)
        self.bind(width=_rewrap)

        def _resize_label(inst, texture_size):
            # Once texture is computed with correct wrapping, set height
            lbl.height = texture_size[1] + 4
        lbl.bind(texture_size=_resize_label)

        def _resize_bubble(inst, lbl_height):
            self.height = max(30, lbl_height + 10)
        lbl.bind(height=_resize_bubble)

        # Background color
        if is_ck:
            bg_color = (0.08, 0.12, 0.2, 1.0)
        else:
            bg_color = (0.12, 0.12, 0.14, 1.0)

        with self.canvas.before:
            Color(*bg_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)

        # Emotion dot for CK messages
        if is_ck and emotion_color:
            r, g, b = emotion_color
            with self.canvas.before:
                Color(r, g, b, 0.8)
                self._emo_dot = Ellipse(
                    pos=(self.x + 4, self.y + self.height - 12),
                    size=(8, 8))

        self.bind(pos=self._update_bg, size=self._update_bg)
        self.add_widget(lbl)
        self.height = 40  # initial placeholder until layout fires

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        if hasattr(self, '_emo_dot'):
            self._emo_dot.pos = (self.x + 4, self.y + self.height - 12)


# ================================================================
#  APPLICATION
# ================================================================

class CKSimApp(App):
    """The CK Coherence Machine -- two-screen Kivy app."""

    title = 'CK Coherence Machine'

    def build(self):
        Builder.load_file(KV_PATH)
        Window.clearcolor = (0.05, 0.05, 0.07, 1)

        self.audio = AudioEngine()

        # Engine construction auto-starts sensorium (including EarsEngine).
        # Do NOT create a second EarsEngine -- it would fight over the mic.
        self.engine = CKSimEngine()
        self.engine.audio_engine = self.audio

        # Reuse the ears the sensorium already created
        self.ears = getattr(self.engine, 'ears_engine', None)
        if self.ears is None:
            self.ears = EarsEngine()
            self.engine.ears_engine = self.ears

        self._ui_counter = 0
        self._engine_event = None
        self._scroll_pending = False

        return CKRootWidget()

    def on_start(self):
        # GUI is open = user is calling CK for help. Be attentive!
        self.engine.user_present = True
        self.engine.start()
        self._engine_event = Clock.schedule_interval(
            self._engine_tick, 1.0 / 50.0)
        print("[CK] Engine started at 50Hz -- chat mode (user present)")

    def on_stop(self):
        if self._engine_event:
            self._engine_event.cancel()
        self.audio.stop()
        if self.ears:
            self.ears.stop()
        self.engine.stop()
        print("[CK] Engine stopped. TL + development saved.")

    # ── 50Hz engine tick ──

    def _engine_tick(self, dt):
        try:
            self.engine.tick(dt)
        except Exception as e:
            if self._ui_counter % 250 == 0:  # Don't spam
                print(f"[CK] Engine tick error: {e}")
        self._ui_counter += 1

        # UI at ~10Hz (every 5th engine tick)
        if self._ui_counter % 5 == 0:
            try:
                self._update_chat_ui()
                self._update_dash_ui()
            except Exception as e:
                if self._ui_counter % 250 == 0:
                    print(f"[CK] UI update error: {e}")

    # ── Chat UI update ──

    def _update_chat_ui(self):
        mgr = self.root.manager if self.root else None
        if not mgr:
            return
        chat = mgr.get_screen('chat')
        if not chat:
            return

        eng = self.engine

        # Emotion dot
        if chat.emotion_dot:
            emo_color = eng.emotion_color
            chat.emotion_dot.canvas.clear()
            with chat.emotion_dot.canvas:
                Color(*emo_color, 0.9)
                d = min(chat.emotion_dot.width,
                        chat.emotion_dot.height) * 0.7
                cx = chat.emotion_dot.x + chat.emotion_dot.width / 2
                cy = chat.emotion_dot.y + chat.emotion_dot.height / 2
                Ellipse(pos=(cx - d / 2, cy - d / 2), size=(d, d))

        # Stage label
        if chat.stage_label:
            chat.stage_label.text = eng.dev_stage_name

        # Mood label
        if chat.mood_label:
            chat.mood_label.text = (
                f"{eng.emotion_primary} {eng.emotion.current.symbol}")

        # Bond label
        if chat.bond_label:
            chat.bond_label.text = eng.bond_stage

        # Study/knowledge status
        if chat.study_label:
            study = eng.study_progress
            if study == 'Idle':
                chat.study_label.text = f"K:{eng.knowledge_count}"
                chat.study_label.color = (0.35, 0.45, 0.6, 0.6)
            else:
                chat.study_label.text = study[:30]
                chat.study_label.color = (0.4, 0.8, 0.4, 0.9)

        # Mic button state
        if chat.chat_mic_btn:
            chat.chat_mic_btn.text = (
                'MIC ON' if self.ears.is_running else 'MIC')

        # New messages -- drain from engine's pending list (never loses msgs)
        # Skip 'user' messages since we show those immediately in send_chat_message
        # Skip study/discovery noise -- chat is for conversation, not status updates
        new = eng.drain_ui_messages(limit=3)
        added = False
        if new:
            for sender, text in new:
                if sender == 'user':
                    continue  # already shown instantly
                # Filter out study/discovery/thesis noise from chat
                if text and text.startswith('[') and any(
                        text.startswith(p) for p in (
                        '[STUDY', '[DISCOVERY', '[RE-READING',
                        '[THESIS', '[MIRROR', '[NOTE')):
                    continue  # engine log, not conversation
                emo_color = eng.emotion_color if sender == 'ck' else None
                bubble = ChatBubble(
                    sender, text, emotion_color=emo_color)
                if chat.chat_container:
                    chat.chat_container.add_widget(bubble)
                    added = True

            if added:
                self._request_scroll_bottom(chat)

    # ── Dashboard UI update ──

    def _update_dash_ui(self):
        mgr = self.root.manager if self.root else None
        if not mgr:
            return
        dash = mgr.get_screen('dashboard')
        if not dash:
            return

        eng = self.engine

        # LED
        if dash.led_widget:
            dash.led_widget.led_color = list(eng.led_color)

        # Coherence dial
        if dash.coherence_dial:
            dash.coherence_dial.coherence = eng.coherence
            dash.coherence_dial.band_name = eng.band_name

        # Breath wave
        if dash.breath_wave:
            dash.breath_wave.update_value(
                eng.breath_mod, eng.breath_phase_name)

        # Heatmap (slower)
        if dash.heatmap and eng.tick_count % 25 == 0:
            dash.heatmap.update_matrix(eng.get_tl_matrix())

        # Crystals (even slower)
        if dash.crystal_list and eng.tick_count % 50 == 0:
            dash.crystal_list.update_crystals(eng.crystals)

        # Labels
        if dash.mode_label:
            m = eng.mode_name
            if eng.brain.bump:
                m += "  ** BUMP **"
            dash.mode_label.text = f"MODE: {m}"

        if dash.operator_label:
            dash.operator_label.text = (
                f"B: {OP_NAMES[eng.phase_b]}  \u2192  "
                f"D: {OP_NAMES[eng.phase_d]}  \u2192  "
                f"BC: {OP_NAMES[eng.phase_bc]}")

        if dash.coherence_label:
            dash.coherence_label.text = (
                f"C: {eng.coherence:.3f}  Band: {eng.band_name}")

        if dash.body_label:
            b = eng.body
            dash.body_label.text = (
                f"E: {b.heartbeat.E:.2f}  "
                f"A: {b.heartbeat.A:.2f}  "
                f"K: {b.heartbeat.K:.2f}")

        if dash.breath_label:
            dash.breath_label.text = (
                f"Breath: {eng.breath_phase_name}  "
                f"Mod: {eng.breath_mod:.2f}")

        if dash.entropy_label:
            dash.entropy_label.text = (
                f"Entropy: {eng.entropy:.2f}  "
                f"Crystals: {len(eng.crystals)}  "
                f"Tick: {eng.tick_count}")

        if dash.tick_label:
            dash.tick_label.text = f"{eng.ticks_per_second:.0f} t/s"

        # Ear status
        if dash.ear_label:
            if self.ears.is_running:
                feat = self.ears.get_features()
                ear_op = OP_NAMES[feat['operator']]
                dash.ear_label.text = (
                    f"Ear: {ear_op}  "
                    f"D2: {feat['d2_mag']:.2f}  "
                    f"RMS: {feat['rms']:.3f}")
            else:
                dash.ear_label.text = "Ear: OFF"

        # Button states
        if dash.speaker_btn:
            dash.speaker_btn.text = (
                'SPEAKER ON' if self.audio.is_running else 'SPEAKER')
        if dash.mic_btn:
            dash.mic_btn.text = (
                'MIC ON' if self.ears.is_running else 'MIC')

        # BTQ status
        if dash.btq_label:
            band = eng.btq_band
            btq_colors = {
                'GREEN': (0.15, 0.8, 0.3, 1.0),
                'YELLOW': (0.9, 0.7, 0.0, 1.0),
                'RED': (0.9, 0.15, 0.1, 1.0),
            }
            dash.btq_label.text = f"BTQ: {band}"
            dash.btq_label.color = btq_colors.get(
                band, (0.4, 0.4, 0.5, 1.0))

        # Emotion label
        if dash.emotion_label:
            emo = eng.emotion.current
            r, g, b = emo.color
            dash.emotion_label.text = (
                f"Emotion: {emo.primary} {emo.symbol}")
            dash.emotion_label.color = (r, g, b, 1.0)

        # Organism status bar (includes knowledge/study from experience lattice)
        if dash.organism_label:
            study = eng.study_progress
            dash.organism_label.text = (
                f"Stage: {eng.dev_stage_name} | "
                f"Mood: {eng.personality_mood} | "
                f"Bond: {eng.bond_stage} | "
                f"Immune: {eng.immune_band} | "
                f"Knowledge: {eng.knowledge_count} | "
                f"Concepts: {eng.concept_count} | "
                f"{study}")

        # Sensorium: fractal sensation (calm — just the organism reading)
        if dash.sense_label and hasattr(eng, 'sensorium'):
            try:
                sense = eng.sensorium.get_sense_for_voice()
                org = sense.get('organism', 'BALANCE')
                oc = sense.get('organism_coherence', 0.5)
                layers = sense.get('layers', {})
                parts = [f"{k}={v['state'][:3]}" for k, v in layers.items()]
                dash.sense_label.text = (
                    f"{org} ({oc:.2f})  "
                    + "  ".join(parts))
            except Exception:
                pass

    # ── Screen navigation ──

    def go_dashboard(self):
        mgr = self.root.manager
        if mgr:
            mgr.transition = SlideTransition(direction='left')
            mgr.current = 'dashboard'

    def go_chat(self):
        mgr = self.root.manager
        if mgr:
            mgr.transition = SlideTransition(direction='right')
            mgr.current = 'chat'

    # ── Scroll helper (debounced) ──

    def _request_scroll_bottom(self, chat):
        """Schedule scroll-to-bottom after layout settles.

        Uses two-pass: first lets layout compute, then scrolls.
        Cancels any pending scroll and reschedules to avoid races.
        """
        sv = chat.chat_scroll
        if not sv:
            return

        # Cancel any previous pending scroll
        if hasattr(self, '_scroll_event') and self._scroll_event:
            self._scroll_event.cancel()

        def _do_scroll(dt):
            sv.scroll_y = 0
            self._scroll_pending = False
            self._scroll_event = None
        self._scroll_pending = True
        self._scroll_event = Clock.schedule_once(_do_scroll, 0.15)

    # ── Chat input ──

    def send_chat_message(self):
        mgr = self.root.manager
        if not mgr:
            return
        chat = mgr.get_screen('chat')
        if not chat or not chat.text_input:
            return

        text = chat.text_input.text.strip()
        if not text:
            return

        chat.text_input.text = ''

        # Show user's message immediately as a bubble (don't wait for drain)
        if chat.chat_container:
            bubble = ChatBubble('user', text)
            chat.chat_container.add_widget(bubble)
            self._request_scroll_bottom(chat)

        self.engine.receive_text(text)

    # ── Controls ──

    def toggle_engine(self):
        if self.engine.running:
            self.engine.stop()
            if self._engine_event:
                self._engine_event.cancel()
                self._engine_event = None
            print("[CK] Paused")
        else:
            self.engine.start()
            self._engine_event = Clock.schedule_interval(
                self._engine_tick, 1.0 / 50.0)
            print("[CK] Resumed")

    def toggle_speaker(self):
        if self.audio.is_running:
            self.audio.stop()
            print("[CK] Speaker OFF")
        else:
            self.audio.start()
            print("[CK] Speaker ON")

    def toggle_mic(self):
        if self.ears.is_running:
            self.ears.stop()
            print("[CK] Mic OFF")
        else:
            self.ears.start()
            print("[CK] Mic ON")

    def save_tl(self):
        self.engine.save_tl()
        print(f"[CK] TL saved ({self.engine.brain.tl_total} transitions)")

    def load_tl(self):
        fn = self.engine.tl_filename
        if self.engine.load_tl_file(fn):
            print(f"[CK] TL loaded from {fn}")
        else:
            print(f"[CK] No TL file found at {fn}")


if __name__ == '__main__':
    CKSimApp().run()
