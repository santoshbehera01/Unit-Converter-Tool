# ⚡ Unit Converter Tool (UnitFlow)

A modern, dashboard-style desktop application for fast and accurate unit
conversions. Built with **Python 3** and **Tkinter (ttk)** using clean
object-oriented code.

![Status](https://img.shields.io/badge/status-stable-3B82F6) ![Python](https://img.shields.io/badge/python-3.9%2B-blue) ![License](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Features

- **6 Conversion Categories** — Length, Weight, Temperature, Time, Area, Speed
- **Modern Dashboard UI** — left sidebar navigation, header, summary cards, status bar
- **Currency-style Result Card** — large formatted result with one-click copy
- **Conversion History** — scrollable, sortable table of past conversions
- **Statistics Dashboard** — totals, most used category, category breakdown bars
- **CSV Export** — export your full history with one click
- **Robust Validation** — empty input, numeric-only, friendly error dialogs

## 📦 Installation

```bash
# 1. Clone or download this repository
cd Unit-Converter-Tool

# 2. (Linux only) Install Tkinter if it's not bundled
sudo apt install python3-tk

# 3. Run the app
python main.py
```

No third-party dependencies required.

## 🚀 Usage

1. Launch the app — the **Dashboard** opens by default.
2. Click any **category card** or the **Convert** tab in the sidebar.
3. Pick a conversion type, type a number, press **Convert** (or Enter).
4. Copy the result, or open the **History** tab to review/export past work.

## 📁 Folder Structure

```
Unit-Converter-Tool/
├── main.py                 # Application entry point
├── requirements.txt
├── README.md
├── .gitignore
├── assets/icons/           # Optional icon assets
├── data/
│   ├── history.json        # Persistent history store
│   └── history.csv         # Exported CSV (generated)
├── documentation/
│   ├── PROJECT_DOC.md
│   └── USER_MANUAL.md
└── screenshots/
```

## 🛠 Technologies

Python 3 • Tkinter • ttk • JSON • CSV • Object-Oriented Programming

## 🖼 Screenshots

Place app screenshots in the `screenshots/` folder.

## 🔮 Future Enhancements

- Dark mode toggle
- Custom unit favorites
- Chart visualizations (matplotlib)
- Multi-language support
- Drag-and-drop CSV import

## 📝 License

MIT
