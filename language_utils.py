#language utils.py
import pandas as pd
from dateutil import parser
import re

def is_japanese_date(string):
    """Check if a string follows the Japanese date format YYYY年MM月DD日."""
    if pd.isna(string):
        return False
    return bool(re.match(r'^\d{4}年\d{2}月\d{2}日$', str(string)))

def translate_japanese_date(date_string):
    """Translate Japanese date format YYYY年MM月DD日 to English."""
    date_obj = parser.parse(str(date_string).replace('年', '-').replace('月', '-').replace('日', ''))
    return date_obj.strftime('%B %d, %Y')

# Add functions for other languages as needed
# For example:

# def is_korean_date(string):
#     # ... (Logic for Korean date detection)

# def translate_korean_date(date_string):
#     # ... (Logic for Korean date translation) 