import streamlit as st
import requests
import pronouncing
from deep_translator import GoogleTranslator

# Function to translate text using deep-translator
def translate(text, tgt_lang_code):
    try:
        translated = GoogleTranslator(source='auto', target=tgt_lang_code).translate(text)
        return translated
    except Exception as e:
        return f"Error in translation: {e}"

# Function to get rhymes from Datamuse API
def get_rhymes(word):
    response = requests.get(f'https://api.datamuse.com/words?rel_rhy={word}&max=10')
    if response.status_code == 200:
        rhymes = [item['word'] for item in response.json()]
        return rhymes
    else:
        return []

# Function to count syllables using pronouncing
def count_syllables(word):
    phones = pronouncing.phones_for_word(word)
    if phones:
        return pronouncing.syllable_count(phones[0])
    else:
        # Fallback heuristic: count vowels as syllables
        return sum(1 for char in word.lower() if char in 'aeiou')

def main():
    st.title("Melosphere AI - Lyric Assistant Prototype")

    lyric_line = st.text_input("Enter your lyric line (English):")

   languages = {
    "Spanish": "es",
    "Kannada": "kn",
    "Tamil": "ta",
    "Malayalam": "ml",
    "Hindi": "hi",
    "Telugu": "te",
    "Japanese": "ja",
}

    tgt_lang = st.selectbox("Select target language for translation:", list(languages.keys()))

    if lyric_line:
        words = lyric_line.strip().split()
        last_word = words[-1].lower()

        # Rhymes for the last word
        rhymes = get_rhymes(last_word)
        if rhymes:
            st.write(f"Rhymes for '{last_word}': {', '.join(rhymes)}")
        else:
            st.write(f"No rhymes found for '{last_word}'.")

        # Syllable counts
        syllables_per_word = {w: count_syllables(w) for w in words}
        total_syllables = sum(syllables_per_word.values())
        st.write(f"Syllables per word: {syllables_per_word}")
        st.write(f"Total syllables in your line: {total_syllables}")

        # Translate to selected language
        translation = translate(lyric_line, languages[tgt_lang])
        st.write(f"{tgt_lang} translation: {translation}")

if __name__ == "__main__":
    main()
