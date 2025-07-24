# MIT License
# 
# Copyright (c) 2025 Veronika Kocher for DIO Itelligence Offensive
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import pandas as pd
import json
import csv
import tkinter as tk
from tkinter import filedialog, messagebox
import os

def detect_delimiter(file_path):
    """Detects whether the CSV file uses semicolons or commas as delimiters."""
    with open(file_path, 'r', encoding="utf-8-sig") as f:
        first_line = f.readline()
        return ";" if ";" in first_line else ","

def convert_csv_delimiter(input_file, output_file):
    """Converts semicolon-separated CSV to comma-separated, if needed."""
    detected_delimiter = detect_delimiter(input_file)
    if detected_delimiter == ",":
        print("CSV already uses commas. No conversion needed.")
        return input_file  # No conversion needed

    with open(input_file, "r", encoding="utf-8-sig") as infile, \
         open(output_file, "w", encoding="utf-8", newline="") as outfile:
        reader = csv.reader(infile, delimiter=detected_delimiter)
        writer = csv.writer(outfile, delimiter=",")
        for row in reader:
            cleaned_row = [cell.strip() for cell in row]
            writer.writerow(cleaned_row)
    print(f"Converted CSV saved as: {output_file}")
    return output_file

def csv_to_jsonld(csv_filename, json_filename):
    # Define temporary file for delimiter conversion
    converted_csv_path = csv_filename.replace(".csv", "_converted.csv")
    csv_filename = convert_csv_delimiter(csv_filename, converted_csv_path)

    try:
        df = pd.read_csv(csv_filename, encoding="utf-8-sig", delimiter=",")
        df.columns = df.columns.str.strip()
    except Exception as e:
        messagebox.showerror("Fehler", f"CSV konnte nicht gelesen werden:\n{e}")
        return

    events = []

    for _, row in df.iterrows():
        event = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": row.get("name", "Unknown Event"),
            "startDate": row.get("startDate"),
            "endDate": row.get("endDate"),
            "location": {
                "@type": "Place",
                "name": row.get("location_name"),
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": row.get("location_street"),
                    "addressLocality": row.get("location_city"),
                    "postalCode": row.get("location_postalCode"),
                    "addressCountry": row.get("location_country")
                }
            },
            "image": row.get("image"),
            "description": row.get("description"),
            "eventAttendanceMode": row.get("eventAttendanceMode", "https://schema.org/OfflineEventAttendanceMode"),
            "performer": {
                "@type": "PerformingGroup",
                "name": row.get("performer")
            } if pd.notna(row.get("performer")) else None,
            "organizer": {
                "@type": "Organization",
                "name": row.get("organizer_name"),
                "url": row.get("organizer_url")
            },
            "offers": {
                "@type": "Offer",
                "url": row.get("offer_url"),
                "price": row.get("offer_price"),
                "priceCurrency": row.get("offer_currency"),
                "availability": row.get("offer_availability"),
                "validFrom": row.get("offer_validFrom")
            },
            "validThrough": row.get("validThrough"),
            "isAccessibleForFree": str(row.get("isAccessibleForFree", "")).strip().lower() == "true",
            "eventStatus": "https://schema.org/EventCancelled" if str(row.get("eventStatus", "")).strip().lower() == "cancelled" else None,
            "sponsor": {
                "@type": "Organization",
                "name": row.get("sponsor_name"),
                "url": row.get("sponsor_url"),
                "logo": row.get("sponsor_logo")
            } if pd.notna(row.get("sponsor_name")) else None
        }
        # Remove keys with None or empty values
        event = {k: v for k, v in event.items() if v not in [None, "", "null"]}
        events.append(event)

    with open(json_filename, "w", encoding="utf-8") as jsonfile:
        json.dump(events, jsonfile, indent=4, ensure_ascii=False)
    messagebox.showinfo("Fertig", f"JSON-LD gespeichert als:\n{json_filename}")

# === GUI ===
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)

def run_conversion():
    input_csv = entry_file.get()
    if not input_csv:
        messagebox.showwarning("Fehler", "Bitte eine CSV-Datei auswählen.")
        return

    output_json = input_csv.replace(".csv", "_JSON-LD.json")
    csv_to_jsonld(input_csv, output_json)

root = tk.Tk()
root.title("CSV → JSON-LD Konverter")

tk.Label(root, text="CSV-Datei auswählen:").pack(pady=5)
entry_file = tk.Entry(root, width=60)
entry_file.pack(padx=10)
tk.Button(root, text="Durchsuchen...", command=select_file).pack(pady=5)
tk.Button(root, text="Konvertieren", command=run_conversion).pack(pady=10)

root.mainloop()
