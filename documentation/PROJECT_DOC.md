# Project Documentation — Unit Converter Tool

## Overview
A professional desktop unit converter built with Python + Tkinter following
OOP principles and PEP 8 style. Designed as a modern dashboard rather than a
typical form-based utility.

## Architecture

```
main.py
├── Constants & Theme         # color palette, fonts
├── Conversion Logic          # CATEGORIES + convert_value()
├── HistoryManager            # JSON persistence + CSV export
├── UI Widgets                # HoverButton, SidebarButton, make_card
└── UnitConverterApp          # main controller (pages, navigation, status)
```

### Key Classes
| Class | Responsibility |
|-------|----------------|
| `HistoryManager` | Load/save/clear history, compute stats, CSV export |
| `SidebarButton`  | Custom sidebar nav row with hover + active states |
| `HoverButton`    | tk.Button with hover color transitions |
| `UnitConverterApp` | Application controller — pages and event handlers |

### Pages
- **Dashboard** — KPI cards + category quick-pick grid
- **Convert** — input card + currency-style result card
- **History** — scrollable Treeview with Export & Clear
- **Statistics** — KPIs + per-category breakdown bars
- **About** — app info + technologies

## Data Storage
- `data/history.json` — list of `{timestamp, category, conversion, input, output}`
- `data/history.csv` — generated on export

## Validation Strategy
- Empty input → warning dialog
- Non-numeric input → error dialog
- Missing conversion type → warning dialog
- All conversion math wrapped in try/except with friendly error message

## Design System
- Color palette: deep navy sidebar (`#1E2A44`), accent blue (`#3B82F6`),
  light workspace (`#F4F6FB`), white cards
- Typography: Segoe UI throughout, hierarchical sizes
- Components: cards with 1px borders, hover effects, status bar, scrollbars

## Testing Checklist
- All 6 categories convert correctly
- Negative and decimal inputs handled
- History persists across restarts
- CSV export produces valid file
- Clear history requires confirmation
