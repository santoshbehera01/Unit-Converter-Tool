"""
Unit Converter Tool — UnitFlow
A premium, workspace-style desktop utility for unit conversions.

Author: Unit Converter Tool
Python 3.x | Tkinter | ttk
"""

import csv
import json
import os
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import filedialog, messagebox, ttk

# ---------------------------------------------------------------------------
# Constants & Theme
# ---------------------------------------------------------------------------

APP_TITLE = "Unit Converter"
APP_VERSION = "2.0.0"

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
HISTORY_JSON = os.path.join(DATA_DIR, "history.json")
HISTORY_CSV = os.path.join(DATA_DIR, "history.csv")

# Fresh premium palette — warm off-white workspace + deep plum accents.
# Intentionally distinct from typical admin-dashboard blues/navy.
THEME = {
    "bg":            "#F6F4EF",   # warm parchment workspace
    "panel":         "#FFFFFF",   # cards
    "panel_alt":     "#FBF9F4",   # input wells
    "border":        "#E7E2D6",
    "border_strong": "#D6D0BF",
    "ink":           "#1B1B1F",   # near-black ink
    "ink_soft":      "#4A4A55",
    "muted":         "#8A8676",
    "accent":        "#5B2A86",   # deep plum
    "accent_hover":  "#4A2070",
    "accent_soft":   "#EFE6F7",
    "highlight":     "#E8B931",   # mustard accent
    "success":       "#2F7A55",
    "danger":        "#B23A48",
    "chip":          "#F0EBE0",
    "chip_active":   "#1B1B1F",
    "chip_active_t": "#FFFFFF",
    "result_bg":     "#1B1B1F",
    "result_fg":     "#F6F4EF",
    "result_accent": "#E8B931",
}

FONT_FAMILY = "Segoe UI"
FONT_SERIF = "Georgia"
FONT_BRAND = (FONT_SERIF, 20, "bold")
FONT_H1 = (FONT_FAMILY, 26, "bold")
FONT_H2 = (FONT_FAMILY, 14, "bold")
FONT_BODY = (FONT_FAMILY, 10)
FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
FONT_LABEL = (FONT_FAMILY, 9, "bold")
FONT_INPUT = (FONT_FAMILY, 24)
FONT_RESULT = (FONT_FAMILY, 40, "bold")
FONT_SMALL = (FONT_FAMILY, 9)
FONT_CHIP = (FONT_FAMILY, 10, "bold")

# ---------------------------------------------------------------------------
# Conversion Logic (unchanged)
# ---------------------------------------------------------------------------

CATEGORIES = {
    "Length": [
        "Kilometer -> Meter", "Meter -> Kilometer",
        "Meter -> Centimeter", "Centimeter -> Meter",
        "Meter -> Millimeter", "Millimeter -> Meter",
        "Mile -> Kilometer", "Kilometer -> Mile",
    ],
    "Weight": [
        "Kilogram -> Gram", "Gram -> Kilogram",
        "Pound -> Kilogram", "Kilogram -> Pound",
    ],
    "Temperature": [
        "Celsius -> Fahrenheit", "Fahrenheit -> Celsius",
        "Celsius -> Kelvin", "Kelvin -> Celsius",
    ],
    "Time": [
        "Seconds -> Minutes", "Minutes -> Seconds",
        "Minutes -> Hours", "Hours -> Minutes",
        "Hours -> Days", "Days -> Hours",
    ],
    "Area": [
        "Square Meter -> Square Kilometer",
        "Square Kilometer -> Square Meter",
        "Acre -> Square Meter", "Square Meter -> Acre",
    ],
    "Speed": [
        "Km/h -> m/s", "m/s -> Km/h",
        "Km/h -> mph", "mph -> Km/h",
    ],
}

CATEGORY_ICONS = {
    "Length": "📏", "Weight": "⚖️", "Temperature": "🌡️",
    "Time": "⏱️", "Area": "📐", "Speed": "🚀",
}


def convert_value(conversion: str, value: float) -> float:
    table = {
        "Kilometer -> Meter":           lambda v: v * 1000.0,
        "Meter -> Kilometer":           lambda v: v / 1000.0,
        "Meter -> Centimeter":          lambda v: v * 100.0,
        "Centimeter -> Meter":          lambda v: v / 100.0,
        "Meter -> Millimeter":          lambda v: v * 1000.0,
        "Millimeter -> Meter":          lambda v: v / 1000.0,
        "Mile -> Kilometer":            lambda v: v * 1.609344,
        "Kilometer -> Mile":            lambda v: v / 1.609344,
        "Kilogram -> Gram":             lambda v: v * 1000.0,
        "Gram -> Kilogram":             lambda v: v / 1000.0,
        "Pound -> Kilogram":            lambda v: v * 0.45359237,
        "Kilogram -> Pound":            lambda v: v / 0.45359237,
        "Celsius -> Fahrenheit":        lambda v: (v * 9.0 / 5.0) + 32.0,
        "Fahrenheit -> Celsius":        lambda v: (v - 32.0) * 5.0 / 9.0,
        "Celsius -> Kelvin":            lambda v: v + 273.15,
        "Kelvin -> Celsius":            lambda v: v - 273.15,
        "Seconds -> Minutes":           lambda v: v / 60.0,
        "Minutes -> Seconds":           lambda v: v * 60.0,
        "Minutes -> Hours":             lambda v: v / 60.0,
        "Hours -> Minutes":             lambda v: v * 60.0,
        "Hours -> Days":                lambda v: v / 24.0,
        "Days -> Hours":                lambda v: v * 24.0,
        "Square Meter -> Square Kilometer": lambda v: v / 1_000_000.0,
        "Square Kilometer -> Square Meter": lambda v: v * 1_000_000.0,
        "Acre -> Square Meter":             lambda v: v * 4046.8564224,
        "Square Meter -> Acre":             lambda v: v / 4046.8564224,
        "Km/h -> m/s":                  lambda v: v / 3.6,
        "m/s -> Km/h":                  lambda v: v * 3.6,
        "Km/h -> mph":                  lambda v: v / 1.609344,
        "mph -> Km/h":                  lambda v: v * 1.609344,
    }
    if conversion not in table:
        raise ValueError(f"Unknown conversion: {conversion}")
    return table[conversion](value)


def split_units(conversion: str):
    """Return (from_unit, to_unit) tuple for a conversion string."""
    parts = [p.strip() for p in conversion.split("->")]
    if len(parts) == 2:
        return parts[0], parts[1]
    return conversion, ""


def find_inverse(conversion: str):
    """Find the inverse conversion ('A -> B' becomes 'B -> A') if available."""
    a, b = split_units(conversion)
    inverse = f"{b} -> {a}"
    for items in CATEGORIES.values():
        if inverse in items:
            return inverse
    return None


# ---------------------------------------------------------------------------
# History Manager (unchanged behavior)
# ---------------------------------------------------------------------------


class HistoryManager:
    def __init__(self, path: str = HISTORY_JSON) -> None:
        self.path = path
        self.entries: list[dict] = []
        self._ensure_files()
        self.load()

    def _ensure_files(self) -> None:
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.entries = json.load(f)
        except (json.JSONDecodeError, OSError):
            self.entries = []

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.entries, f, indent=2)

    def add(self, category, conversion, input_value, output_value) -> None:
        self.entries.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category,
            "conversion": conversion,
            "input": input_value,
            "output": output_value,
        })
        self.save()

    def clear(self) -> None:
        self.entries = []
        self.save()

    def export_csv(self, path: str = HISTORY_CSV) -> str:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Category", "Conversion",
                             "Input", "Output"])
            for e in self.entries:
                writer.writerow([e["timestamp"], e["category"],
                                 e["conversion"], e["input"], e["output"]])
        return path

    def total(self) -> int:
        return len(self.entries)

    def most_used_category(self) -> str:
        if not self.entries:
            return "—"
        return Counter(e["category"] for e in self.entries).most_common(1)[0][0]

    def category_counts(self) -> dict:
        return dict(Counter(e["category"] for e in self.entries))

    def recent(self, n: int = 6) -> list:
        return list(reversed(self.entries[-n:]))


# ---------------------------------------------------------------------------
# Reusable Widgets
# ---------------------------------------------------------------------------


class FlatButton(tk.Label):
    """A flat clickable label with hover styling — no native button chrome."""

    def __init__(self, master, text, command, *, bg, fg, hover_bg=None,
                 hover_fg=None, font=FONT_BODY_BOLD, padx=18, pady=10,
                 cursor="hand2"):
        super().__init__(master, text=text, bg=bg, fg=fg, font=font,
                         padx=padx, pady=pady, cursor=cursor)
        self._bg = bg
        self._fg = fg
        self._hover_bg = hover_bg or bg
        self._hover_fg = hover_fg or fg
        self._command = command
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Button-1>", self._click)

    def _enter(self, _e):
        self.configure(bg=self._hover_bg, fg=self._hover_fg)

    def _leave(self, _e):
        self.configure(bg=self._bg, fg=self._fg)

    def _click(self, _e):
        if self._command:
            self._command()

    def set_colors(self, bg=None, fg=None, hover_bg=None, hover_fg=None):
        if bg: self._bg = bg
        if fg: self._fg = fg
        if hover_bg: self._hover_bg = hover_bg
        if hover_fg: self._hover_fg = hover_fg
        self.configure(bg=self._bg, fg=self._fg)


class CategoryChip(tk.Label):
    """Pill-shaped category selector chip."""

    def __init__(self, master, text, command):
        super().__init__(master, text=text, font=FONT_CHIP,
                         bg=THEME["chip"], fg=THEME["ink"],
                         padx=16, pady=8, cursor="hand2")
        self._command = command
        self._active = False
        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)
        self.bind("<Button-1>", lambda _e: self._command(self["text"]))

    def set_active(self, active: bool):
        self._active = active
        if active:
            self.configure(bg=THEME["chip_active"], fg=THEME["chip_active_t"])
        else:
            self.configure(bg=THEME["chip"], fg=THEME["ink"])

    def _enter(self, _e):
        if not self._active:
            self.configure(bg=THEME["border"])

    def _leave(self, _e):
        if not self._active:
            self.configure(bg=THEME["chip"])


def card(parent, **kwargs):
    """A rounded-look card via a 1px border frame."""
    outer = tk.Frame(parent, bg=THEME["border"], **kwargs)
    inner = tk.Frame(outer, bg=THEME["panel"])
    inner.pack(fill="both", expand=True, padx=1, pady=1)
    return outer, inner


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------


class UnitConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.history = HistoryManager()
        self.current_category = "Length"
        self.current_conversion = tk.StringVar(value=CATEGORIES["Length"][0])
        self.input_var = tk.StringVar()
        self.result_var = tk.StringVar(value="—")
        self.result_sub_var = tk.StringVar(value="Enter a value and press Convert")
        self.last_result_value = None
        self.chip_widgets = {}

        self._configure_root()
        self._configure_ttk_styles()
        self._build_layout()
        self._select_category("Length")

    # -- setup ---------------------------------------------------------------

    def _configure_root(self):
        self.root.title(APP_TITLE)
        self.root.geometry("1180x740")
        self.root.minsize(980, 640)
        self.root.configure(bg=THEME["bg"])

    def _configure_ttk_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Unit.TCombobox",
                        fieldbackground=THEME["panel_alt"],
                        background=THEME["panel_alt"],
                        foreground=THEME["ink"],
                        bordercolor=THEME["border_strong"],
                        lightcolor=THEME["border_strong"],
                        darkcolor=THEME["border_strong"],
                        arrowcolor=THEME["accent"],
                        padding=8)
        style.map("Unit.TCombobox",
                  fieldbackground=[("readonly", THEME["panel_alt"])],
                  foreground=[("readonly", THEME["ink"])])

        # Treeview for history
        style.configure("Flow.Treeview",
                        background=THEME["panel"],
                        fieldbackground=THEME["panel"],
                        foreground=THEME["ink"],
                        bordercolor=THEME["border"],
                        rowheight=30,
                        font=FONT_BODY)
        style.configure("Flow.Treeview.Heading",
                        background=THEME["panel_alt"],
                        foreground=THEME["muted"],
                        font=FONT_LABEL,
                        relief="flat",
                        padding=8)
        style.map("Flow.Treeview",
                  background=[("selected", THEME["accent_soft"])],
                  foreground=[("selected", THEME["accent"])])

    # -- layout --------------------------------------------------------------

    def _build_layout(self):
        # Top bar (slim brand bar — replaces the admin sidebar)
        topbar = tk.Frame(self.root, bg=THEME["bg"])
        topbar.pack(fill="x", padx=28, pady=(22, 0))

        brand = tk.Frame(topbar, bg=THEME["bg"])
        brand.pack(side="left")
        tk.Label(brand, text="◆", font=(FONT_SERIF, 22, "bold"),
                 fg=THEME["accent"], bg=THEME["bg"]).pack(side="left")
        tk.Label(brand, text=" UnitFlow", font=FONT_BRAND,
                 fg=THEME["ink"], bg=THEME["bg"]).pack(side="left")
        tk.Label(brand, text=f"  v{APP_VERSION}", font=FONT_SMALL,
                 fg=THEME["muted"], bg=THEME["bg"]).pack(side="left", pady=(8, 0))

        actions = tk.Frame(topbar, bg=THEME["bg"])
        actions.pack(side="right")
        FlatButton(actions, "Export CSV", self._export_csv,
                   bg=THEME["bg"], fg=THEME["ink_soft"],
                   hover_bg=THEME["chip"], hover_fg=THEME["ink"],
                   font=FONT_BODY, padx=14, pady=8).pack(side="left", padx=4)
        FlatButton(actions, "Clear History", self._clear_history,
                   bg=THEME["bg"], fg=THEME["ink_soft"],
                   hover_bg=THEME["chip"], hover_fg=THEME["danger"],
                   font=FONT_BODY, padx=14, pady=8).pack(side="left", padx=4)

        # Hairline under the brand bar
        tk.Frame(self.root, bg=THEME["border"], height=1).pack(
            fill="x", padx=28, pady=(18, 0))

        # Category chip row
        chip_row = tk.Frame(self.root, bg=THEME["bg"])
        chip_row.pack(fill="x", padx=28, pady=(18, 0))
        tk.Label(chip_row, text="CATEGORY", font=FONT_LABEL,
                 fg=THEME["muted"], bg=THEME["bg"]).pack(side="left",
                                                        padx=(0, 14))
        for cat in CATEGORIES:
            chip = CategoryChip(chip_row, f"{CATEGORY_ICONS[cat]}  {cat}",
                                self._on_chip_clicked)
            chip.pack(side="left", padx=4)
            self.chip_widgets[cat] = chip

        # Main workspace (split layout): converter (left) + side rail (right)
        main = tk.Frame(self.root, bg=THEME["bg"])
        main.pack(fill="both", expand=True, padx=28, pady=20)
        main.grid_columnconfigure(0, weight=3, uniform="m")
        main.grid_columnconfigure(1, weight=2, uniform="m")
        main.grid_rowconfigure(0, weight=1)

        self._build_converter_panel(main)
        self._build_side_rail(main)

        # Status bar (slim, modern)
        status = tk.Frame(self.root, bg=THEME["bg"])
        status.pack(fill="x", padx=28, pady=(0, 14))
        tk.Frame(status, bg=THEME["border"], height=1).pack(fill="x",
                                                            pady=(0, 8))
        self.status_label = tk.Label(status, text="Ready",
                                     font=FONT_SMALL, fg=THEME["muted"],
                                     bg=THEME["bg"], anchor="w")
        self.status_label.pack(side="left")
        tk.Label(status, text="Premium desktop utility · Tkinter",
                 font=FONT_SMALL, fg=THEME["muted"],
                 bg=THEME["bg"]).pack(side="right")

    # -- left: converter workspace ------------------------------------------

    def _build_converter_panel(self, parent):
        outer, panel = card(parent)
        outer.grid(row=0, column=0, sticky="nsew", padx=(0, 14))

        inner = tk.Frame(panel, bg=THEME["panel"])
        inner.pack(fill="both", expand=True, padx=36, pady=32)

        # Header
        head = tk.Frame(inner, bg=THEME["panel"])
        head.pack(fill="x")
        self.workspace_title = tk.Label(head, text="Length conversion",
                                        font=FONT_H1, fg=THEME["ink"],
                                        bg=THEME["panel"], anchor="w")
        self.workspace_title.pack(side="left")
        # Mustard accent underline mark
        tk.Frame(inner, bg=THEME["highlight"], height=3, width=42).pack(
            anchor="w", pady=(6, 22))

        # From / Swap / To row
        units_row = tk.Frame(inner, bg=THEME["panel"])
        units_row.pack(fill="x")
        units_row.grid_columnconfigure(0, weight=1)
        units_row.grid_columnconfigure(2, weight=1)

        self._from_box = self._unit_box(units_row, "FROM")
        self._from_box.grid(row=0, column=0, sticky="ew")

        swap_holder = tk.Frame(units_row, bg=THEME["panel"])
        swap_holder.grid(row=0, column=1, padx=14, pady=(18, 0))
        self.swap_btn = tk.Label(swap_holder, text="⇄",
                                 font=(FONT_FAMILY, 18, "bold"),
                                 bg=THEME["accent_soft"], fg=THEME["accent"],
                                 width=3, height=1, cursor="hand2",
                                 padx=4, pady=4)
        self.swap_btn.pack()
        self.swap_btn.bind("<Button-1>", lambda _e: self._swap_units())
        self.swap_btn.bind("<Enter>",
                           lambda _e: self.swap_btn.configure(
                               bg=THEME["accent"], fg=THEME["panel"]))
        self.swap_btn.bind("<Leave>",
                           lambda _e: self.swap_btn.configure(
                               bg=THEME["accent_soft"], fg=THEME["accent"]))

        self._to_box = self._unit_box(units_row, "TO")
        self._to_box.grid(row=0, column=2, sticky="ew")

        # Conversion dropdown (for selecting which formula in the category)
        cv_row = tk.Frame(inner, bg=THEME["panel"])
        cv_row.pack(fill="x", pady=(22, 0))
        tk.Label(cv_row, text="CONVERSION", font=FONT_LABEL,
                 fg=THEME["muted"], bg=THEME["panel"]).pack(anchor="w")
        self.conversion_combo = ttk.Combobox(
            cv_row, textvariable=self.current_conversion,
            state="readonly", style="Unit.TCombobox",
            font=FONT_BODY, values=CATEGORIES[self.current_category])
        self.conversion_combo.pack(fill="x", pady=(6, 0), ipady=4)
        self.conversion_combo.bind("<<ComboboxSelected>>",
                                   lambda _e: self._on_conversion_change())

        # Input field
        in_row = tk.Frame(inner, bg=THEME["panel"])
        in_row.pack(fill="x", pady=(22, 0))
        tk.Label(in_row, text="VALUE", font=FONT_LABEL,
                 fg=THEME["muted"], bg=THEME["panel"]).pack(anchor="w")
        well = tk.Frame(in_row, bg=THEME["border_strong"])
        well.pack(fill="x", pady=(6, 0))
        well_inner = tk.Frame(well, bg=THEME["panel_alt"])
        well_inner.pack(fill="x", padx=1, pady=1)
        self.input_entry = tk.Entry(well_inner, textvariable=self.input_var,
                                    font=FONT_INPUT, bd=0, relief="flat",
                                    bg=THEME["panel_alt"], fg=THEME["ink"],
                                    insertbackground=THEME["accent"])
        self.input_entry.pack(fill="x", padx=18, pady=14)
        self.input_entry.bind("<Return>", lambda _e: self._convert())

        # Action buttons row
        btn_row = tk.Frame(inner, bg=THEME["panel"])
        btn_row.pack(fill="x", pady=(20, 0))

        self.convert_btn = FlatButton(
            btn_row, "Convert  →", self._convert,
            bg=THEME["accent"], fg=THEME["panel"],
            hover_bg=THEME["accent_hover"], hover_fg=THEME["panel"],
            font=(FONT_FAMILY, 11, "bold"), padx=28, pady=14)
        self.convert_btn.pack(side="left")

        FlatButton(btn_row, "Clear", self._clear_input,
                   bg=THEME["panel"], fg=THEME["ink_soft"],
                   hover_bg=THEME["chip"], hover_fg=THEME["ink"],
                   font=FONT_BODY_BOLD, padx=18, pady=14).pack(
                       side="left", padx=(10, 0))

        FlatButton(btn_row, "Copy Result", self._copy_result,
                   bg=THEME["panel"], fg=THEME["ink_soft"],
                   hover_bg=THEME["chip"], hover_fg=THEME["accent"],
                   font=FONT_BODY_BOLD, padx=18, pady=14).pack(
                       side="left", padx=(10, 0))

        # Result display (dark dramatic panel)
        result_outer = tk.Frame(inner, bg=THEME["result_bg"])
        result_outer.pack(fill="x", pady=(26, 0))
        rin = tk.Frame(result_outer, bg=THEME["result_bg"])
        rin.pack(fill="x", padx=28, pady=24)
        tk.Label(rin, text="RESULT", font=FONT_LABEL,
                 fg=THEME["result_accent"], bg=THEME["result_bg"]).pack(
                     anchor="w")
        tk.Label(rin, textvariable=self.result_var, font=FONT_RESULT,
                 fg=THEME["result_fg"], bg=THEME["result_bg"],
                 anchor="w").pack(anchor="w", pady=(2, 0))
        tk.Label(rin, textvariable=self.result_sub_var, font=FONT_BODY,
                 fg="#A8A39A", bg=THEME["result_bg"], anchor="w").pack(
                     anchor="w", pady=(6, 0))

    def _unit_box(self, parent, label):
        wrap = tk.Frame(parent, bg=THEME["panel"])
        tk.Label(wrap, text=label, font=FONT_LABEL,
                 fg=THEME["muted"], bg=THEME["panel"]).pack(anchor="w")
        box = tk.Frame(wrap, bg=THEME["border_strong"])
        box.pack(fill="x", pady=(6, 0))
        inner = tk.Frame(box, bg=THEME["panel_alt"])
        inner.pack(fill="x", padx=1, pady=1)
        unit_label = tk.Label(inner, text="—", font=(FONT_FAMILY, 16, "bold"),
                              fg=THEME["ink"], bg=THEME["panel_alt"],
                              anchor="w", padx=18, pady=18)
        unit_label.pack(fill="x")
        wrap._unit_label = unit_label
        return wrap

    # -- right: side rail (recent + stats) ----------------------------------

    def _build_side_rail(self, parent):
        rail = tk.Frame(parent, bg=THEME["bg"])
        rail.grid(row=0, column=1, sticky="nsew")
        rail.grid_rowconfigure(1, weight=1)
        rail.grid_columnconfigure(0, weight=1)

        # Quick stats strip
        stats_outer, stats_panel = card(rail)
        stats_outer.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        sp = tk.Frame(stats_panel, bg=THEME["panel"])
        sp.pack(fill="x", padx=22, pady=20)
        sp.grid_columnconfigure(0, weight=1)
        sp.grid_columnconfigure(1, weight=1)

        self.stat_total_var = tk.StringVar(value="0")
        self.stat_top_var = tk.StringVar(value="—")
        self._stat_block(sp, 0, "TOTAL CONVERSIONS", self.stat_total_var)
        self._stat_block(sp, 1, "MOST USED", self.stat_top_var)

        # Recent history card
        hist_outer, hist_panel = card(rail)
        hist_outer.grid(row=1, column=0, sticky="nsew")
        hp = tk.Frame(hist_panel, bg=THEME["panel"])
        hp.pack(fill="both", expand=True, padx=22, pady=20)

        head = tk.Frame(hp, bg=THEME["panel"])
        head.pack(fill="x")
        tk.Label(head, text="Recent activity", font=FONT_H2,
                 fg=THEME["ink"], bg=THEME["panel"]).pack(side="left")
        tk.Label(head, text="LIVE", font=FONT_LABEL,
                 fg=THEME["accent"], bg=THEME["accent_soft"],
                 padx=8, pady=3).pack(side="right")

        tk.Frame(hp, bg=THEME["border"], height=1).pack(fill="x",
                                                        pady=(10, 8))

        # Treeview list
        tree_wrap = tk.Frame(hp, bg=THEME["panel"])
        tree_wrap.pack(fill="both", expand=True)
        cols = ("when", "conv", "in", "out")
        self.history_tree = ttk.Treeview(
            tree_wrap, columns=cols, show="headings",
            style="Flow.Treeview", height=10)
        for cid, txt, w, anc in [
            ("when", "Time", 70, "w"),
            ("conv", "Conversion", 180, "w"),
            ("in", "Input", 70, "e"),
            ("out", "Output", 90, "e"),
        ]:
            self.history_tree.heading(cid, text=txt.upper())
            self.history_tree.column(cid, width=w, anchor=anc)
        self.history_tree.pack(fill="both", expand=True)

        self._refresh_history()
        self._refresh_stats()

    def _stat_block(self, parent, col, label, var):
        frame = tk.Frame(parent, bg=THEME["panel"])
        frame.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 12, 0))
        tk.Label(frame, text=label, font=FONT_LABEL,
                 fg=THEME["muted"], bg=THEME["panel"]).pack(anchor="w")
        tk.Label(frame, textvariable=var, font=(FONT_FAMILY, 22, "bold"),
                 fg=THEME["ink"], bg=THEME["panel"]).pack(anchor="w",
                                                          pady=(4, 0))

    # -- behavior ------------------------------------------------------------

    def _set_status(self, text, color=None):
        self.status_label.configure(text=text,
                                    fg=color or THEME["muted"])

    def _on_chip_clicked(self, chip_text):
        # strip leading emoji + spaces
        for cat in CATEGORIES:
            if chip_text.endswith(cat):
                self._select_category(cat)
                return

    def _select_category(self, category):
        self.current_category = category
        for cat, chip in self.chip_widgets.items():
            chip.set_active(cat == category)
        self.workspace_title.configure(
            text=f"{category} conversion")
        items = CATEGORIES[category]
        self.conversion_combo.configure(values=items)
        self.current_conversion.set(items[0])
        self._on_conversion_change()
        self._set_status(f"Category set to {category}")

    def _on_conversion_change(self):
        conv = self.current_conversion.get()
        a, b = split_units(conv)
        self._from_box._unit_label.configure(text=a)
        self._to_box._unit_label.configure(text=b)
        self.result_var.set("—")
        self.result_sub_var.set("Enter a value and press Convert")

    def _swap_units(self):
        inv = find_inverse(self.current_conversion.get())
        if inv is None:
            messagebox.showinfo(
                "Swap unavailable",
                "There is no inverse conversion defined for this pair.")
            return
        # locate which category contains the inverse and switch if needed
        for cat, items in CATEGORIES.items():
            if inv in items:
                if cat != self.current_category:
                    self._select_category(cat)
                self.current_conversion.set(inv)
                self._on_conversion_change()
                self._set_status("Units swapped")
                return

    def _clear_input(self):
        self.input_var.set("")
        self.result_var.set("—")
        self.result_sub_var.set("Cleared")
        self.input_entry.focus_set()

    def _convert(self):
        raw = self.input_var.get().strip()
        if not raw:
            messagebox.showwarning("Missing value",
                                   "Please enter a value to convert.")
            return
        try:
            value = float(raw)
        except ValueError:
            messagebox.showerror("Invalid input",
                                 "Please enter a valid numeric value.")
            return
        conv = self.current_conversion.get()
        try:
            result = convert_value(conv, value)
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Conversion error", str(exc))
            return
        formatted = self._format_number(result)
        self.last_result_value = formatted
        self.result_var.set(formatted)
        a, b = split_units(conv)
        self.result_sub_var.set(
            f"{self._format_number(value)} {a}  →  {formatted} {b}")
        self.history.add(self.current_category, conv, value, result)
        self._refresh_history()
        self._refresh_stats()
        self._set_status("Conversion saved to history",
                         color=THEME["success"])

    @staticmethod
    def _format_number(value: float) -> str:
        if value == int(value):
            return f"{int(value):,}"
        return f"{value:,.6f}".rstrip("0").rstrip(".")

    def _copy_result(self):
        if self.last_result_value is None:
            messagebox.showinfo("Nothing to copy",
                                "Run a conversion first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(str(self.last_result_value))
        self._set_status("Result copied to clipboard",
                         color=THEME["accent"])

    # -- history & stats refresh --------------------------------------------

    def _refresh_history(self):
        for row in self.history_tree.get_children():
            self.history_tree.delete(row)
        for entry in self.history.recent(12):
            ts = entry["timestamp"].split(" ")[1][:5]
            self.history_tree.insert(
                "", "end",
                values=(ts, entry["conversion"],
                        self._format_number(entry["input"]),
                        self._format_number(entry["output"])))

    def _refresh_stats(self):
        self.stat_total_var.set(str(self.history.total()))
        self.stat_top_var.set(self.history.most_used_category())

    # -- history actions ----------------------------------------------------

    def _clear_history(self):
        if not self.history.entries:
            self._set_status("History is already empty")
            return
        if messagebox.askyesno("Clear history",
                               "Delete all saved conversions?"):
            self.history.clear()
            self._refresh_history()
            self._refresh_stats()
            self._set_status("History cleared", color=THEME["danger"])

    def _export_csv(self):
        if not self.history.entries:
            messagebox.showinfo("Nothing to export",
                                "Your history is empty.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile="history.csv",
            filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            self.history.export_csv(path)
        except OSError as exc:
            messagebox.showerror("Export failed", str(exc))
            return
        self._set_status(f"Exported to {os.path.basename(path)}",
                         color=THEME["success"])


def main() -> None:
    root = tk.Tk()
    UnitConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
