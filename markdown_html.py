<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Markdown Renderer</title>
</head>
<body>
    <h1>Markdown Renderer</h1>
    <textarea id="markdown-input" rows="10" cols="50"># Hello Markdown!</textarea>
    <div id="markdown-output"></div>

    <!-- Include the Marked library -->
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        // Function to render Markdown
        function renderMarkdown() {
            const markdownText = document.getElementById('markdown-input').value;
            const htmlContent = marked(markdownText);
            document.getElementById('markdown-output').innerHTML = htmlContent;
        }

        // Render Markdown on page load
        renderMarkdown();

        // Optional: Render Markdown whenever the input changes
        document.getElementById('markdown-input').addEventListener('input', renderMarkdown);
    </script>
</body>
</html>
