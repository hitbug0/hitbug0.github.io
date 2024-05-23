# Automating XML Sitemap Creation with ChatGPT
::tags{Web Development, Python, ChatGPT, RPA}::

---

To ensure my blog appears in Google searches, it's necessary to register an XML sitemap. However, manually updating this file every time I update a post is a hassle... So, I had ChatGPT write a script to automatically update the XML sitemap for me.

## What You Will Learn in This Article
You will learn the following:

- Overview of XML sitemaps
- How to have ChatGPT write a Python script (as an example)
- Code for automatic XML sitemap generation

## What is the XML Sitemap
Here is an overview:

- Data associated with an individual website.
    - It’s website-wide, not page-specific.
- A file that describes the information on the pages of a website in a format that search engines can read.
    - Format = XML (eXtensible Markup Language)
- Contains information about all the pages on the website, including URLs, update frequency, and importance.
    - However, not all information is strictly required.
- Using this improves the website's SEO, allowing users to find information on the website more quickly.

XML sitemaps are typically named something like `sitemap.xml`.

## How Was the Code Written?: ChatGPT
The Python code for automatic XML sitemap generation was written by ChatGPT.  
[Here is the conversation with ChatGPT](https://chat.openai.com/share/f60f65b1-b84a-4189-96b1-c6b175bae28b) during that process.  

1. Asking for an example format of an XML sitemap.

1. Requesting the code creation:
    - Asking, "Please write code in Python that does the following: ..."

1. Requesting fine-tuning:
    - Asking to format the last modification date as "yyyy-mm-ddTHH:MM:SS+09:00".

    - Including `index.html` in the sitemap.

Notably, [**even when I accidentally sent an incomplete instruction, ChatGPT was able to understand the intent**](https://chat.openai.com/share/f60f65b1-b84a-4189-96b1-c6b175bae28b#:~:text=Please%20add%20the%20following%20feature%20to%20this%20code%3A%0A%0A%2D%20Include%20index.html%20(which%20is%20not%20in%20the%20posts%20directory%2C%20but%20is%20in%20the%20same%20directory%20as%20the%20Python%20script)%20in%20the%20sitemap.) — this was quite surprising!

## the Final Code Looks Like
Here is the final code provided by ChatGPT. By changing the part of the code where it says `https://example.com`, it can be used by almost anyone. It worked perfectly for my needs.

```Python
import glob
import os
import urllib.parse
from datetime import datetime

def get_last_modified_time(file_path):
    """
    Get the last modified time of a file.
    """
    modified_time = os.path.getmtime(file_path)
    return datetime.utcfromtimestamp(modified_time)

def generate_sitemap():
    """
    Generate sitemap.xml based on the files in the 'posts' directory.
    """
    # Get the last modified date of index.html
    index_last_modified = get_last_modified_time('index.html')

    files = glob.glob('posts/*.html')
    
    urls = []
    for file_path in files:
        file_name = os.path.basename(file_path)
        last_modified = get_last_modified_time(file_path)
        encoded_file_name = urllib.parse.quote(file_name)
        urls.append((encoded_file_name, last_modified))

    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add index.html to the sitemap
    index_last_modified_str = index_last_modified.strftime('%Y-%m-%dT%H:%M:%S+09:00')
    sitemap_content += f'   <url>\n'
    sitemap_content += f'      <loc>https://example.com/index.html</loc>\n'
    sitemap_content += f'      <lastmod>{index_last_modified_str}</lastmod>\n'
    sitemap_content += f'   </url>\n'
    
    for file_name, last_modified in urls:
        last_modified_str = last_modified.strftime('%Y-%m-%dT%H:%M:%S+09:00')
        sitemap_content += f'   <url>\n'
        sitemap_content += f'      <loc>https://example.com/{file_name}</loc>\n'
        sitemap_content += f'      <lastmod>{last_modified_str}</lastmod>\n'
        sitemap_content += f'   </url>\n'
    
    sitemap_content += '</urlset>'
    
    with open('sitemap.xml', 'w') as sitemap_file:
        sitemap_file.write(sitemap_content)

if __name__ == "__main__":
    generate_sitemap()
```

## Bonus
If you save the above code as `generate_sitemap.py` in a `programs` folder, you can create a batch file in the same directory as the `programs` folder to run the script just by double-clicking the batch file.

```
python ./programs/generate_sitemap.py
```

## Summary
In this article, we covered the following:
- Overview of XML sitemaps
- How to have ChatGPT write a Python script (as an example)
- Code for automatic XML sitemap generation

I was particularly surprised when ChatGPT understood my intention even when I accidentally sent an incomplete instruction...!  
I hope this will be helpful for those looking to automate tasks or use ChatGPT in similar ways.
