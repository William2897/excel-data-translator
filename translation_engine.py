#translation engine.py
from deep_translator import GoogleTranslator
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
import random

class TranslationEngine:
    def __init__(self, source_language='ja', target_language='en', max_workers=14):
        self.source_language = source_language
        self.target_language = target_language
        self.max_workers = max_workers
        self.translation_cache = {}

    def translate_batch(self, texts, retries=3, delay=5):
        """Translates a batch of texts with retry mechanism."""
        translator = GoogleTranslator(source=self.source_language, target=self.target_language)
        valid_texts = [str(text) for text in texts if isinstance(text, str) and len(text) <= 5000]
        if not valid_texts:
            return texts

        for attempt in range(retries):
            try:
                translations = translator.translate_batch(valid_texts)
                return translations
            except Exception as e:
                print(f"Error translating batch: {e}")
                if attempt < retries - 1:
                    print(f"Retrying... ({attempt + 1}/{retries})")
                    time.sleep(delay + random.uniform(0, 2))
                else:
                    print(f"Failed to translate batch after {retries} attempts. Returning original texts.")
                    return valid_texts

    def translate_texts_parallel(self, texts):
        """Translate texts in parallel while preserving order."""
        results = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            translated_batches = list(executor.map(self.translate_batch, np.array_split(texts, self.max_workers)))
            for batch in translated_batches:
                results.extend(batch)
        return results
