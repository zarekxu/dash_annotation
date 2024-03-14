from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    # Some string to display
    display_string = "This is the string you want to display in the collapsible block."

    # HTML template with collapsible functionality
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Collapsible Example</title>
        <style>
            .collapsible {
                background-color: #777;
                color: white;
                cursor: pointer;
                padding: 18px;
                width: 100%;
                border: none;
                text-align: left;
                outline: none;
                font-size: 15px;
            }

            .active, .collapsible:hover {
                background-color: #555;
            }

            .content {
                padding: 0 18px;
                display: none;
                overflow: hidden;
                background-color: #f1f1f1;
            }
        </style>
    </head>
    <body>

    <h2>Collapsible String Display</h2>

    <button type="button" class="collapsible">Show/Hide String</button>
    <div class="content">
        <p>{{ display_string }}</p>
    </div>

    <script>
        var coll = document.getElementsByClassName("collapsible")[0];
        coll.addEventListener("click", function() {
            this.classList.toggle("active");
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
                content.style.display = "none";
            } else {
                content.style.display = "block";
            }
        });
    </script>

    </body>
    </html>
    """
    return render_template_string(html, display_string=display_string)

if __name__ == '__main__':
    app.run(debug=True)
