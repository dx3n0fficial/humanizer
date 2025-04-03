# Dx3n Text Humanizer

![Dx3n Text Humanizer Logo](generated-icon.png)

## Created by Huzaifah Tahir (Dx3n)

A sophisticated text humanization application that transforms AI-generated content into more natural, human-like writing that can evade AI detection systems.

## 🔍 Overview

Dx3n Text Humanizer is a powerful tool that makes AI-written content sound genuinely human-written through a combination of advanced text processing techniques and linguistic manipulation strategies. The application features a user-friendly interface built with Streamlit, making it accessible to users without technical knowledge.

### 🎯 Key Features

- **Multiple Humanization Levels**: Choose from 5 different humanization styles, from subtle to scholarly
- **Advanced Anti-Detection**: Uses sophisticated techniques to bypass AI content detectors
- **Text Database**: Save, retrieve, and manage your humanized texts
- **Detailed Statistics**: View word counts, sentence analysis, and text similarity metrics
- **User-Friendly Interface**: Simple, intuitive design with helpful guidance throughout

## 💫 Anti-Detection Technologies

Dx3n Text Humanizer implements several cutting-edge techniques to evade AI detection:

- **Unicode Homoglyphs**: Replaces characters with visually identical ones from Cyrillic, Greek, Cherokee, and other alphabets
- **Human Error Patterns**: Inserts realistic typos, punctuation errors, and self-corrections in four different styles
- **Invisible Timing Markers**: Embeds hidden characters that mimic human typing rhythm
- **Statistical Pattern Breaking**: Disrupts AI-generated statistical patterns
- **Golden Ratio Positioning**: Places special characters at positions that match natural human writing patterns

## 🚀 Getting Started

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app.py
   ```
4. Access the app in your web browser at `http://localhost:5000`

## 📋 Usage

### Basic Usage

1. Navigate to the "Humanize Text" tab
2. Paste your AI-generated text in the input box or upload a text file
3. Adjust the humanization level (1-5) as needed
4. Click "Humanize My Text"
5. View, download, or copy your human-like result

### Humanization Levels

- **Level 1**: Subtle changes, preserves almost all original content
- **Level 2**: Light humanization with minor phrasing adjustments
- **Level 3**: Balanced approach (recommended for general purpose)
- **Level 4**: Significant humanization with more casual style
- **Level 5**: Scholarly style with elevated vocabulary and sophisticated structure

### Saving and Managing Texts

1. After humanizing text, navigate to the "My Saved Texts" tab
2. Click "Save Current Text" and add optional notes or tags
3. View, search, or load previously saved texts at any time

## 🔧 Advanced Options

For enhanced functionality, you can integrate with external APIs:

- **Gemini AI**: For premium quality humanization (requires API key)
- **Plagiarism Check**: Verify your text is unique (requires Google API key)

Set these API keys in your environment variables to enable these features.

## 🔗 Project Structure

- `app.py`: Main application file with Streamlit UI and core functionality
- `humanizer.py`: Contains the text humanization algorithms and stealth features
- `text_utils.py`: Utility functions for text processing with custom tokenizers
- `database.py`: Custom database implementation for storing humanized texts
- `text_database.json`: Database file for storing humanized texts

## ⚠️ Disclaimer

This tool is provided for educational and research purposes only. Users are responsible for ensuring their use of this software complies with all applicable laws, regulations, and terms of service.

## 📄 License

© 2025 Dx3n Text Humanizer - Created by Huzaifah Tahir (Dx3n) - All Rights Reserved