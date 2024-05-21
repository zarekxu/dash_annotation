import re

def add_url_to_headers(file_path, url, output_path=None):
    # Read the file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Regular expressions for level 1 and level 2 headers
    level1_pattern = re.compile(r'(^# .*$)', re.MULTILINE)
    level2_pattern = re.compile(r'(^## .*$)', re.MULTILINE)

    # Function to append URL to headers
    def append_url(match):
        return f"{match.group(0)} [{url}]"

    # Modify the content by appending the URL to headers
    modified_content = level1_pattern.sub(append_url, content)
    modified_content = level2_pattern.sub(append_url, modified_content)

    # Write the modified content to the output file
    if output_path:
        with open(output_path, 'w') as file:
            file.write(modified_content)
    else:
        with open(file_path, 'w') as file:
            file.write(modified_content)

# Example usage
file_path = 'example.md'
output_path = 'modified_example.md'  # Optional: if you want to save to a different file
url = 'https://example.com'

add_url_to_headers(file_path, url, output_path)

print(f"Headers in '{file_path}' have been updated with the URL and saved to '{output_path}'")
