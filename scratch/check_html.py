import sys
from html.parser import HTMLParser

class SimpleHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags_stack = []
        self.self_closing_tags = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
            'link', 'meta', 'param', 'source', 'track', 'wbr', 'script', 'link'
        }
        self.errors = []

    def handle_starttag(self, tag, attrs):
        # We don't stack self-closing tags
        if tag not in self.self_closing_tags:
            self.tags_stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.self_closing_tags:
            return
        if not self.tags_stack:
            self.errors.append(f"Unexpected closing tag </{tag}> at line {self.getpos()[0]}")
            return
        
        last_tag, pos = self.tags_stack.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched closing tag </{tag}> at line {self.getpos()[0]} (expected </{last_tag}> from line {pos[0]})")
            # Put it back to keep tracking if it might be an unclosed tag
            self.tags_stack.append((last_tag, pos))

def validate_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Strip script blocks to avoid parsing issues with raw HTML inside strings
    # Replace inline document.writes or js contents with spaces to keep correct line numbers
    import re
    cleaned_content = content
    # Replace script blocks content
    cleaned_content = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', lambda m: '<script>' + '\n' * m.group(1).count('\n') + '</script>', cleaned_content)
    
    parser = SimpleHTMLValidator()
    parser.feed(cleaned_content)
    
    if parser.errors:
        print("HTML Validation Errors:")
        for err in parser.errors:
            print(f"- {err}")
        return False
    
    if parser.tags_stack:
        print("Unclosed HTML tags:")
        for tag, pos in reversed(parser.tags_stack):
            print(f"- <{tag}> at line {pos[0]}")
        return False
        
    print("HTML file structure is well-formed!")
    return True

if __name__ == '__main__':
    import os
    pr_path = "/Users/phileasdazeleygaist/Desktop/My Websites/edge-cases-2026/pr.html"
    success = validate_html(pr_path)
    sys.exit(0 if success else 1)
