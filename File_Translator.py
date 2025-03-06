#file_translator.py

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from data_translator import Translator
import threading
import openpyxl

class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Translator")
        self.root.geometry("500x500")
        self.create_widgets()
        self.filepath = None
        self.completion_times = []

    def create_widgets(self):
        self.file_label = tk.Label(self.root, text="No file selected")
        self.file_label.pack(pady=5)

        self.select_button = tk.Button(self.root, text="Select File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.language_label = tk.Label(self.root, text="Select Language:")
        self.language_label.pack(pady=5)

        self.language_var = tk.StringVar(self.root)
        self.language_var.set("ja")  # default value

        self.language_menu = tk.OptionMenu(self.root, self.language_var, "ja", "ko", "zh")
        self.language_menu.pack(pady=5)

        self.translate_button = tk.Button(self.root, text="Translate", command=self.start_translation, state=tk.DISABLED)
        self.translate_button.pack(pady=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, padx=20, pady=10)

        self.sheet_count_label = tk.Label(self.root, text="Sheets Detected: 0")
        self.sheet_count_label.pack(pady=5)

        self.current_sheet_label = tk.Label(self.root, text="Current Sheet: ")
        self.current_sheet_label.pack(pady=5)

        self.completion_time_label = tk.Label(self.root, text="Status:")
        self.completion_time_label.pack(pady=5)

        self.status_text = tk.Text(self.root, height=8, wrap=tk.WORD)
        self.status_text.pack(fill=tk.X, padx=20, pady=10)
        self.status_text.config(state=tk.DISABLED)

    def select_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")])
        if self.filepath:
            self.file_label.config(text=self.filepath)
            self.translate_button.config(state=tk.NORMAL)

            try:
                workbook = openpyxl.load_workbook(self.filepath)
                sheet_count = len(workbook.sheetnames)
                self.sheet_count_label.config(text=f"Sheets Detected: {sheet_count}")
            except Exception as e:
                messagebox.showerror("Error", f"Error reading file: {e}")
        else:
            self.file_label.config(text="No file selected")
            self.translate_button.config(state=tk.DISABLED)

    def start_translation(self):
        self.translate_button.config(state=tk.DISABLED)
        self.completion_times = []
        self.status_text.config(state=tk.NORMAL)
        self.status_text.delete('1.0', tk.END)
        self.status_text.config(state=tk.DISABLED)
        threading.Thread(target=self.translate_file).start()

    def translate_file(self):
        input_file_path = self.filepath
        output_file_path = input_file_path.replace(".xlsx", "_translated.xlsx")
        try:
            source_language = self.language_var.get()
            translator = Translator(source_language=source_language, target_language='en')
            translator.translate_excel_file(
                input_file_path, 
                output_file_path, 
                progress_callback=self.update_progress, 
                update_sheet_info=self.update_sheet_info
            )
            messagebox.showinfo("Success", f"Translation completed. File saved as {output_file_path}")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        finally:
            self.translate_button.config(state=tk.NORMAL)

    def update_progress(self, progress):
        self.progress['value'] = progress
        self.root.update_idletasks()

    def update_sheet_info(self, current_sheet, completion_time):
        if completion_time == -1:
            status = f"Failed to translate sheet: {current_sheet}"
        elif completion_time == 0:
            status = f"Started translating sheet: {current_sheet}"
        else:
            status = f"Completed sheet: {current_sheet} in {completion_time:.2f}s"

        self.current_sheet_label.config(text=f"Current Sheet: {current_sheet}")
        self.completion_time_label.config(text="Status:\n" + status)  # Display only the current status
        self.update_status(status)
        self.root.update_idletasks()

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TranslatorApp(root)
    root.mainloop()