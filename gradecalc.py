from flask import Flask, request, render_template_string

app = Flask(__name__)

#EQ
def calculate_grades(prelim):
    # Variables
    prelim_weight = 0.2
    midterm_weight = 0.3
    final_weight = 0.5
    desired_grade = 75

    prelim_score = float(prelim) * prelim_weight
    added_weights = midterm_weight + final_weight
    required_midterm_final = (desired_grade - prelim_score) / added_weights

    if required_midterm_final > 100:
        return None, None, True, False, False
    else:
        midterm_final_grade = round(required_midterm_final, 2)
        dean_list = midterm_final_grade <= 81.25
        difficult_pass = midterm_final_grade >= 90
        return midterm_final_grade, midterm_final_grade, False, dean_list, difficult_pass

@app.route('/', methods=['GET', 'POST'])
def index():
    prelim = ""
    midterm = ""
    final = ""
    error = ""
    impossible = False
    dean_list = False
    difficult_pass = False

    if request.method == 'POST':
        prelim = request.form['prelim']
        try:
            prelim = float(prelim)
            if prelim < 1 or prelim > 100:
                error = "Please enter a grade between 1 and 100."
            else:
                midterm, final, impossible, dean_list, difficult_pass = calculate_grades(prelim)
                if impossible:
                    error = "It is impossible to achieve the desired grade with the given prelim score."
        except ValueError:
            error = "Invalid input. Please enter a valid number."

    html_code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Grade Calculator</title>
        <style>
            body {
                font-family: Georgia, serif;
                background-color: #8a7979;
                text-align: center;
                padding: 320px;
            }
            h1 {
                color: #333333;
            }
            input[type="number"] {
                padding: 10px;
                margin: 10px;
                border-radius: 8px;
                border: 1px solid #ccc;
                font-size: 16px;
            }
            button {
                background-color: #8a2727;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 10px;
                cursor: pointer;
                border-radius: 8px;
                border: none;
            }
            button:hover {
                background-color: #cad9d9;
            }
            p {
                font-size: 18px;
                color: #555;
            }
            .error {
                color: red;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>Required Grade Calculator</h1>
        
        <form method="POST" style="border: 2px solid black; padding: 20px; border-radius: 10px; display: inline-block; background-color: white;">
            <label for="prelim" style="font-size: 24px;">Enter your Prelim Grade:</label><br>
            <input type="number" id="prelim" name="prelim" min="1" max="100" step="0.01" required><br><br>
            <button type="submit">Calculate</button>
        </form>

        {% if error %}
        <p class="error">{{ error }}</p>
        {% endif %}

        {% if midterm and final and not impossible %}
        <p style="color:black; font-size:25px;">To pass with the least grade of 75, you need at least:</p>
        <p style="color:black; font-size:25px;">Midterm Grade: <strong>{{ midterm }}</strong></p>
        <p style="color:black; font-size:25px;">Final Grade: <strong>{{ final }}</strong></p>
        {% endif %}

        {% if dean_list %}
        <p style="color:green; font-size:25px;">You can qualify for the Dean's Lister!</p>
        {% endif %}

        {% if difficult_pass %}
        <p style="color:red; font-size:25px;">It's difficult to pass with this Prelim grade. You'll need a Midterm and Final Grade of 90 or higher!</p>
        {% endif %}

        <footer>
            <p>By Dion Andrei G. Quiamzon (BSCS)</p>
        </footer>

    </body>
    </html>
    """
    return render_template_string(html_code, prelim=prelim, midterm=midterm, final=final, error=error, dean_list=dean_list, difficult_pass=difficult_pass)

if __name__ == "__main__":
    app.run(debug=True)
