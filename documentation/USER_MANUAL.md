# User Manual — Unit Converter Tool

## 1. Launching the App
Run `python main.py` from the project folder. The Dashboard opens by default.

## 2. The Interface
- **Left sidebar** — navigate between Dashboard, Convert, History, Statistics, About
- **Header** — shows current page title and date
- **Status bar** (bottom) — shows the last action performed

## 3. Performing a Conversion
1. Click **Convert** in the sidebar (or any category card on the Dashboard).
2. Choose a **Category** (Length, Weight, Temperature, Time, Area, Speed).
3. Choose a **Conversion** type (e.g. *Kilometer → Meter*).
4. Type a numeric **Value** (decimals and negatives allowed).
5. Click **Convert** or press **Enter**.
6. The result appears in a large, formatted card on the right.

### Copy a Result
Click **📋 Copy Result** to copy to your clipboard.

## 4. Viewing History
Click **History** in the sidebar to see every past conversion in a scrollable
table — newest first.

## 5. Exporting History
On the History page, click **⬇ Export CSV**, choose a location, and save.

## 6. Clearing History
On the History page, click **🗑 Clear History** and confirm.

## 7. Statistics
The Statistics page shows:
- Total conversions performed
- Most used category
- Time of your most recent activity
- A horizontal bar chart of conversions per category

## 8. Troubleshooting
| Problem | Solution |
|---------|----------|
| "Please enter a numeric value" | The input field is empty — type a number |
| "Please enter a valid number" | Input contains letters or symbols |
| App won't start on Linux | Install Tkinter: `sudo apt install python3-tk` |

## 9. Keyboard Shortcuts
- **Enter** — perform conversion (when typing in the value field)
