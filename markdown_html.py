<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown to HTML</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        textarea {
            width: 100%;
            height: 200px;
            margin-bottom: 20px;
        }
        .output {
            border: 1px solid #ccc;
            padding: 20px;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>

<h1>Markdown to HTML Converter</h1>

<textarea id="markdownContent" placeholder="Type your Markdown content here..."></textarea>
<br>
<button onclick="convertMarkdown()">Convert to HTML</button>

<h2>Output:</h2>
<div class="output" id="outputBox">
    <!-- Rendered HTML will be displayed here -->
</div>

<script>
    function convertMarkdown() {
        const markdownContent = document.getElementById("markdownContent").value;
        fetch("/render_markdown", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: markdownContent }),
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("outputBox").innerHTML = data.rendered_html;
        });
    }
</script>

</body>
</html>
