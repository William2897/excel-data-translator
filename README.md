# Excel Data Translator

A Python application that translates Excel files from one language to another using Google Translate, with special handling for date formats and a graphical user interface.

## Features

- Translate entire Excel files while preserving structure
- Support for multiple sheets in a workbook
- Special handling for Japanese date formats (converts YYYY年MM月DD日 to English date format)
- Efficient translation with parallel processing
- Translation caching to avoid duplicate API calls
- User-friendly graphical interface

## Requirements

- Python 3.11+
- pandas
- deep_translator
- numpy
- python-dateutil

## Installation

1. Clone this repository or download the files
2. Install required dependencies:

```sh
pip install pandas deep-translator numpy python-dateutil
```

## Project Structure

- [File_Translator.py](File_Translator.py) - Main GUI application file
- [data_translator.py](data_translator.py) - Core translation logic for Excel files
- [translation_engine.py](translation_engine.py) - Translation engine using Google Translate
- [language_utils.py](language_utils.py) - Utilities for language-specific operations
- translate.ico - Application icon

## Usage

Run the application by executing:

```sh
python File_Translator.py
```

## How It Works

1. The [`TranslationEngine`](translation_engine.py) class handles text translation using Google Translate API
2. The [`Translator`](data_translator.py) class processes Excel files sheet by sheet
3. Special formats like Japanese dates are handled by functions in [`language_utils.py`](language_utils.py)
4. The application uses threading for efficient parallel translation

## Extending

To add support for additional languages or special format handling:
1. Add new detection and translation functions in [language_utils.py](language_utils.py)
2. Update the translation process in [data_translator.py](data_translator.py) to use these functions
