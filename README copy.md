# GitHub Repository Word Cloud Generator

This script analyzes a GitHub repository and generates a word cloud from its content, helping you visualize the most commonly used words in the codebase.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. (Optional) Set up GitHub authentication:

   - Create a GitHub personal access token (<https://github.com/settings/tokens>)
   - Set the token as an environment variable:

     ```bash
     export GITHUB_TOKEN='your_token_here'
     ```

   Note: The script will work without authentication for public repositories, but you may hit rate limits.

## Usage

1. Run the script:

```bash
python main.py
```

2. When prompted, enter the GitHub repository URL (e.g., <https://github.com/username/repository>)

3. The script will:
   - Scan the repository for text files
   - Process the content to extract keywords
   - Generate a word cloud image (saved as 'wordcloud.png')
   - Display the top 20 most frequent keywords

## Supported File Types

The script processes the following file types:

- Python (.py)
- JavaScript (.js)
- Java (.java)
- C++ (.cpp, .h)
- C# (.cs)
- Ruby (.rb)
- PHP (.php)
- Text files (.txt)
- Markdown (.md)
