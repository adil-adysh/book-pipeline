# GenBook

**GenBook** is an automated tool designed to help you create well-structured books effortlessly. Simply provide a topic, and the tool organizes the content, generates chapters, and saves the final book in an easy-to-read format. You can also customize the content to have more control over the output.  
## Installation


### Install via pip (recommended for CLI usage)


```bash
pip install .

```


Or build and install from source:

```bash
git clone https://github.com/adil-adysh/book-pipeline.git

cd book-pipeline

pip install .
```


### Development setup (Poetry)






```bash
pip install poetry
poetry install



poetry shell

```


pip install .
```



Or build and install from source:




```bash
git clone https://github.com/adil-adysh/book-pipeline.git

cd book-pipeline
pip install .



```



### Development (Poetry)




```bash
pip install poetry


poetry install


poetry shell
```





## Usage


1. **Set up the API key:**




   ```pwsh


   $env:GEMINI_API_KEY="your_api_key"


   ```

2. **Run the book generator from the CLI:**


   ```pwsh

   genbook --topic "Your Topic" --chapter-count 5 --output-dir "output" --chapter-prompt-file genbook/prompts/chapter_prompt.txt --toc-prompt-file genbook/prompts/toc_prompt.txt

   ```

3. **Follow the prompts:**

   - Enter the book topic and specify the number of chapters.
   - Optionally, provide additional content customization.

   - The tool will generate and save the book.



## Command-Line Options



To see all available options, run:

```pwsh

genbook --help
```



## Customization


You can provide your own structure by using custom prompt files and subtopic lists:



```pwsh
genbook --topic "AI" --chapter-count 5 --output-dir "output" --chapter-prompt-file path/to/chapter_prompt.txt --toc-prompt-file path/to/toc_prompt.txt --subtopics "subtopic1,subtopic2"

```


Contributions are welcome! If you’d like to contribute, please open an issue or submit a pull request.  

---

**Note:** The legacy pipeline in `book_pipeline.py` is deprecated. Please use `book_graph.py` for all new workflows.
