from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # Here you can add or modify content to pass to your HTML template
    content = "This is the content that will be shown or hidden."
    return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Collapse Example</title>
    <style>
        .appmessagediv {
            cursor: pointer;
            padding: 5px;
            border: 1px solid #ddd;
        }
        .appmessagediv:hover {
            background-color: #f5f5f5;
        }
        .toggle {
            display: inline-block;
            width: 20px;
            height: 20px;
            line-height: 20px;
            text-align: center;
            margin-right: 10px;
            background-color: #eee;
        }
    </style>
</head>
<body>
    <div id="upperdiv"></div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            var content = "{{ content }}";
            var upperdiv = document.getElementById('upperdiv');
            var collapsibleHTML = `
                <div class="message">
                    <div class="appmessagediv" onclick="toggleCollapse(this)">
                        <div class="toggle">+</div>
                        <div class="appmessage" style="display: none;">${content}</div>
                    </div>
                </div>
            `;
            upperdiv.innerHTML += collapsibleHTML;
        });

        function toggleCollapse(element) {
            var contentDiv = element.querySelector(".appmessage");
            var toggleDiv = element.querySelector(".toggle");
            if (contentDiv.style.display === "none") {
                contentDiv.style.display = "block";
                toggleDiv.textContent = "-";
            } else {
                contentDiv.style.display = "none";
                toggleDiv.textContent = "+";
            }
        }
    </script>
</body>
</html>''', content=content)

if __name__ == '__main__':
    app.run(debug=True)
