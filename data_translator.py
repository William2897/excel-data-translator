#data_translator.py
import pandas as pd
import time
import language_utils
from translation_engine import TranslationEngine

class Translator:
    def __init__(self, source_language='ja', target_language='en', max_workers=14):
        self.engine = TranslationEngine(
            source_language=source_language,
            target_language=target_language,
            max_workers=max_workers
        )

    def translate_dataframe(self, df, progress_callback=None):
        """Translate the entire DataFrame with a progress callback."""
        total_cells = df.size
        processed_cells = 0

        for col in df.columns:
            texts_to_translate = df[col].dropna().unique()
            texts_to_translate = [
                text 
                for text in texts_to_translate 
                if isinstance(text, str) 
                and not language_utils.is_japanese_date(text)
                and text not in self.engine.translation_cache
            ]
            if texts_to_translate:
                translations = self.engine.translate_texts_parallel(texts_to_translate)
                self.engine.translation_cache.update(dict(zip(texts_to_translate, translations)))

            df[col] = df[col].map(
                lambda x: self.engine.translation_cache.get(x, x) 
                if pd.notna(x) and isinstance(x, str) and not language_utils.is_japanese_date(x) 
                else x
            )
            processed_cells += df[col].size
            if progress_callback:
                progress_callback(processed_cells / total_cells * 100)

        for col in df.columns:
            df[col] = df[col].map(
                lambda x: language_utils.translate_japanese_date(x)
                if pd.notna(x) and isinstance(x, str) and language_utils.is_japanese_date(x)
                else x
            )
        return df

    def translate_excel_file(self, input_file_path, output_file_path, progress_callback=None, update_sheet_info=None):
        """Translate an Excel file with progress callback and sheet info updates."""
        start_time = time.time()
        sheets = pd.read_excel(input_file_path, sheet_name=None, header=None)
        translated_sheets = {}
        
        for sheet_name, df in sheets.items():
            sheet_start_time = time.time()
            if update_sheet_info:
                update_sheet_info(sheet_name, 0)  # Start of sheet translation
            
            print(f"Translating sheet: {sheet_name}")
            translated_df = self.translate_dataframe(df.copy(), progress_callback=progress_callback)
            translated_sheets[sheet_name] = translated_df
            
            sheet_end_time = time.time()
            sheet_elapsed_time = sheet_end_time - sheet_start_time
            if update_sheet_info:
                update_sheet_info(sheet_name, sheet_elapsed_time)

        with pd.ExcelWriter(output_file_path) as writer:
            for sheet_name, translated_df in translated_sheets.items():
                translated_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"Translation completed in {minutes}m {seconds}s. Translated file saved as '{output_file_path}'")