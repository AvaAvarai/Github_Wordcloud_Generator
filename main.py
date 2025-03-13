import os
import re
from github import Github
from urllib.parse import urlparse
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def extract_repo_info(url):
    """Extract owner and repository name from GitHub URL."""
    path = urlparse(url).path.strip('/')
    owner, repo = path.split('/')[:2]
    return owner, repo

def process_content(content):
    """Process text content to extract keywords."""
    # Convert to lowercase and tokenize
    tokens = word_tokenize(content.lower())
    
    # Remove stopwords, special characters, and common programming terms
    stop_words = set(stopwords.words('english'))
    programming_terms = {'def', 'class', 'import', 'return', 'if', 'else', 'for', 'while'}
    stop_words.update(programming_terms)
    
    # Only keep alphabetic tokens that are not in stop words
    keywords = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    return keywords

def generate_word_cloud(keywords):
    """Generate and save word cloud from keywords."""
    # Calculate frequency distribution
    freq_dist = FreqDist(keywords)
    
    # Create and generate word cloud
    wordcloud = WordCloud(width=1600, height=800, background_color='white').generate_from_frequencies(freq_dist)
    
    # Display the word cloud
    plt.figure(figsize=(20,10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig('wordcloud.png')
    plt.close()
    
    return freq_dist

def main():
    # Get GitHub repository URL from user
    repo_url = input("Enter GitHub repository URL: ")
    
    try:
        # Extract repository information
        owner, repo_name = extract_repo_info(repo_url)
        
        # Initialize GitHub (uses GITHUB_TOKEN environment variable if available)
        g = Github(os.getenv('GITHUB_TOKEN'))
        
        # Get repository
        repo = g.get_repo(f"{owner}/{repo_name}")
        
        print(f"Scanning repository: {repo.full_name}")
        
        # Get all file contents
        all_content = []
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                try:
                    # Only process text files
                    if file_content.name.endswith(('.py', '.js', '.java', '.cpp', '.h', '.cs', '.rb', '.php', '.txt', '.md')):
                        content = file_content.decoded_content.decode('utf-8')
                        all_content.append(content)
                except Exception as e:
                    print(f"Error processing {file_content.path}: {str(e)}")
        
        # Combine all content
        combined_content = ' '.join(all_content)
        
        # Process content to get keywords
        keywords = process_content(combined_content)
        
        # Generate word cloud and get frequency distribution
        freq_dist = generate_word_cloud(keywords)
        
        # Print top 20 keywords
        print("\nTop 20 keywords:")
        for word, freq in freq_dist.most_common(20):
            print(f"{word}: {freq}")
            
        print("\nWord cloud has been saved as 'wordcloud.png'")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
