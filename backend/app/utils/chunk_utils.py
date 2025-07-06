import re
from typing import List, Tuple
import tiktoken

def split_by_headers(text: str) -> List[Tuple[str, str]]:
    """
    Split text into (header(s), content) pairs. 
    Handles cases where multiple headers appear consecutively without content.
    
    Returns:
        List[Tuple[str, str]]: List of combined headers and their associated content.
    """
    # Match all Markdown headers (e.g. # Title, ## Subtitle, etc.)
    pattern = re.compile(r'(#{1,6} .*)', re.MULTILINE)
    matches = list(pattern.finditer(text))  # Find all headers
    
    result = []
    i = 0

    while i < len(matches):
        header = matches[i]                 # Current header match object
        start = header.end()               # Start index for content (right after header)
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)  # Next header or end of text
        content = text[start:end].strip()  # Grab content after current header

        combined_headers = [header.group(0)]  # Start with the current header
        i += 1

        # If there's no content under this header, keep merging headers until we find content
        while not content and i < len(matches):
            next_header = matches[i]
            combined_headers.append(next_header.group(0))  # Add the next header
            start = next_header.end()
            end = matches[i + 1].start() if i + 1 < len(matches) - 1 else len(text)
            content = text[start:end].strip()  # Check if there's any content under the next header
            i += 1

        # Append the combined headers and the actual content (even if content is still empty)
        result.append(("\n".join(combined_headers), content))

    return result

def chunk_text(text: str, max_tokens: int = 500) -> List[str]:
    """
    Split text into chunks while preserving document structure.
    
    Args:
        text (str): Text to be chunked
        max_tokens (int): Maximum tokens per chunk
        
    Returns:
        List[str]: List of text chunks
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    chunks = []
    
    # Split into sections by headers
    sections = split_by_headers(text)
    
    for header, content in sections:
        # Initialize chunk with header
        current_chunk = [header]
        current_tokens = len(tokenizer.encode(header))
        
        # Split content into paragraphs
        paragraphs = re.split(r'\n\n+', content.strip())
        
        for paragraph in paragraphs:
            # If paragraph contains a table, handle it separately
            if '|' in paragraph and re.search(r'\|[-:\|\s]+\|', paragraph):
                # If current chunk is not empty and adding table would exceed limit
                if current_chunk and current_tokens > 0:
                    chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [header]  # Start new chunk with header
                    current_tokens = len(tokenizer.encode(header))
                
                # Add table as its own chunk
                table_html = convert_tables_to_html(paragraph)
                chunks.append(f"{header}\n\n{table_html}")
                continue
            
            # Split paragraph into sentences
            sentences = re.split(r'(?<=[.!?])\s+', paragraph)
            paragraph_chunk = []
            
            for sentence in sentences:
                sentence_tokens = len(tokenizer.encode(sentence))
                
                if current_tokens + sentence_tokens > max_tokens:
                    if current_chunk:
                        chunks.append('\n\n'.join(current_chunk))
                    current_chunk = [header]  # Start new chunk with header
                    current_tokens = len(tokenizer.encode(header))
                    if paragraph_chunk:
                        current_chunk.append(' '.join(paragraph_chunk))
                        current_tokens += len(tokenizer.encode(' '.join(paragraph_chunk)))
                        paragraph_chunk = []
                
                paragraph_chunk.append(sentence)
                current_tokens += sentence_tokens
            
            if paragraph_chunk:
                current_chunk.append(' '.join(paragraph_chunk))
        
        if current_chunk and current_chunk != [header]:
            chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def find_headers(text: str) -> List[str]:
    """
    Find all headers in the text.
    
    Args:
        text (str): Text to search for headers
        
    Returns:
        List[str]: List of header lines
    """
    # Match headers of the form ### Header or ## Header
    header_pattern = re.compile(r'^(#{1,6})\s+(.*)$', re.MULTILINE)
    headers = header_pattern.findall(text)
    
    return [f"{'#' * len(header[0])} {header[1].strip()}" for header in headers]

def convert_tables_to_html(text: str) -> str:
    """
    Convert Markdown tables to HTML format.
    
    Args:
        text (str): Markdown text containing tables
        
    Returns:
        str: HTML formatted text
    """
    # Find complete tables with headers and content
    table_pattern = re.compile(r'\|[^\n]+\|\n\|[-:\|\s]+\|\n(\|[^\n]+\|\n?)+')
    
    def replace_table(match):
        table_text = match.group(0)
        rows = table_text.strip().split('\n')
        
        if len(rows) < 3:  # Need at least header, separator, and one data row
            return table_text
            
        html_table = '<table>\n'
        
        # Handle header row
        header_cells = [cell.strip() for cell in rows[0].split('|')[1:-1]]
        html_table += '  <thead>\n    <tr>\n'
        for cell in header_cells:
            html_table += f'      <th>{cell}</th>\n'
        html_table += '    </tr>\n  </thead>\n'
        
        # Skip the separator row (index 1) and process data rows
        html_table += '  <tbody>\n'
        for row in rows[2:]:
            if not row.strip():  # Skip empty rows
                continue
            cells = [cell.strip() for cell in row.split('|')[1:-1]]
            html_table += '    <tr>\n'
            for cell in cells:
                html_table += f'      <td>{cell}</td>\n'
            html_table += '    </tr>\n'
        
        html_table += '  </tbody>\n</table>'
        return html_table
    
    return table_pattern.sub(replace_table, text)


# if __name__ == "__main__":
#     test_text = """
# # Main Header
# ## Sub Header A
# Content A

# ### Nested Header
# Nested content

# ## Sub Header B
# Content B
#     """
    
#     sections = split_by_headers(test_text)
#     print(sections)