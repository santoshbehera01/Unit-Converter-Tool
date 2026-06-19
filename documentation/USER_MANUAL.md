# User Manual — Unit Converter Tool

## 1. Introduction

The **Unit Converter Tool (UnitFlow)** is a desktop application developed using Python and Tkinter. It allows users to perform fast and accurate unit conversions across multiple categories through a simple and user friendly interface.

---

## 2. Starting the Application

### Step 1

Open a terminal in the project folder.

### Step 2

Run the following command:

```bash
python main.py
```

### Step 3

The application dashboard will open automatically.

---

## 3. Application Interface

The application consists of the following sections:

### Dashboard

Provides an overview of conversion activity and quick access to conversion categories.

### Convert

Used to perform unit conversions.

### History

Displays previously performed conversions.

### Statistics

Shows conversion usage statistics and category summaries.

### Status Bar

Displays application status and user actions.

---

## 4. Performing a Conversion

1. Open the **Convert** section.
2. Select a conversion category:
   - Length
   - Weight
   - Temperature
   - Time
   - Area
   - Speed
3. Choose the required conversion type.
4. Enter a numeric value.
5. Click **Convert**.
6. The converted result will be displayed instantly.

---

## 5. Viewing Conversion History

1. Open the **History** section.
2. View all previously performed conversions.
3. Review conversion details and records.
4. Use available options to manage history data.

---

## 6. Exporting History

1. Navigate to the **History** page.
2. Click **Export CSV**.
3. Select a save location.
4. Save the exported file.

The conversion history will be exported in CSV format.

---

## 7. Statistics Dashboard

The Statistics page provides:

- Total Conversions
- Most Frequently Used Category
- Recent Activity Information
- Category wise Conversion Summary

These statistics help users analyze conversion usage.

---

## 8. Data Storage

The application stores data locally in:

```text
data/history.json
```

Exported files are stored as:

```text
data/history.csv
```

Both files are managed automatically by the application.

---

## 9. Troubleshooting

| Problem | Solution |
|----------|----------|
| Application does not start | Ensure Python 3 is installed correctly. |
| Invalid input error | Enter numeric values only. |
| Conversion not working | Verify that a valid category and conversion type are selected. |
| Missing history file | Restart the application. Required files will be created automatically. |
| Tkinter error on Linux | Install Tkinter using `sudo apt install python3-tk`. |

---

## 10. Conclusion

The Unit Converter Tool provides a reliable and efficient solution for performing everyday unit conversions. With its intuitive interface, conversion history, and statistics features, the application offers a convenient experience for students, professionals, and general users.