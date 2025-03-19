
# Gemini Book Generator  

**Gemini Book Generator** is an automated tool designed to help you create well-structured books effortlessly. Simply provide a topic, and the tool organizes the content, generates chapters, and saves the final book in an easy-to-read format. You can also customize the content to have more control over the output.  

---

## Features  

- **Automated Book Generation** – Enter a topic, and the tool generates structured content.  
- **Customizable Output** – Adjust prompts to modify the book’s structure.  
- **Interactive Editing Mode** – Optionally refine and edit content before finalizing.  
- **EPUB Format Support** – Saves the generated book as an EPUB file for easy reading.  

---

## Requirements  

Before using the tool, ensure you have the following installed:  

- **Python 3.9 or later**  
- **Poetry** (for dependency management)  
- **Mypy** (for type checking)  
- **A valid API key** – Required to generate content ([Get your API key here](https://aistudio.google.com/app/apikey))  

---

## Installation  

1. **Clone the repository:**  

   ```bash
   git clone https://github.com/adil-adysh/book-pipeline.git
   cd book-pipeline
   ```  

2. **Install Poetry** (if not installed):  

   ```bash
   pip install poetry
   ```  

3. **Install Mypy globally:**  

   ```bash
   pip install mypy
   ```  

4. **Install dependencies using Poetry:**  

   ```bash
   poetry install
   ```  

5. **Activate the virtual environment:**  

   ```bash
   poetry shell
   ```  

---

## Usage  

1. **Set up the API key:**  

   ```bash
   # Linux/macOS
   export GEMINI_API_KEY=your_api_key

   # Windows (Command Prompt)
   set GEMINI_API_KEY=your_api_key
   ```  

2. **Run the book generator:**  

   ```bash
   poetry run python gemini_book_generator/main.py
   ```  

3. **Follow the prompts:**  
   - Enter the book topic and specify the number of chapters.  
   - Optionally, provide additional content customization.  
   - The tool will generate and save the book.  

---

## Command-Line Options  

To see all available options, run:  

```bash
poetry run python gemini_book_generator/main.py --help
```  

---

## Customization  

You can provide your own structure by using custom prompt files and subtopic lists:  

```bash
poetry run python gemini_book_generator/main.py --toc-prompt-file path/to/toc_prompt.txt --chapter-prompt-file path/to/chapter_prompt.txt --subtopics-list "subtopic1,subtopic2"
```  

---

## Code Quality & Type Checking  

To check for type errors, run **Mypy**:  

```bash
mypy gemini_book_generator/
```  

If additional type definitions are needed, install them with:  

```bash
mypy --install-types
```  

---

## Troubleshooting  

- Ensure all dependencies are installed.  
- Verify that the API key is set correctly.  
- Check file paths when using custom settings.  

---

## License  

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.  

---

### Contributing  

Contributions are welcome! If you’d like to contribute, please open an issue or submit a pull request.  
