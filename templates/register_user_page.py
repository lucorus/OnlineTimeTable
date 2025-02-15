def generate_registration_page(schools: list) -> str:
    school_options = ''.join(
        f'<option value="{uuid}" data-city="{city}">{title} <span style="font-size: 0.8em; color: #888;">({city})</span></option>'
        for uuid, title, city in schools
    )

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registration Page</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}

            .container {{
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                width: 300px;
            }}

            h2 {{
                text-align: center;
                margin-bottom: 20px;
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }}

            input, select, button {{
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }}

            button {{
                background-color: #28a745;
                color: white;
                border: none;
                cursor: pointer;
            }}

            button:hover {{
                background-color: #218838;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Registration Form</h2>
            <form id="registrationForm" action="/register_user" method="post">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>

                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>

                <label for="school">School:</label>
                <select id="school" name="school_uuid" required>
                    <option value="">Select your school</option>
                    {school_options}
                </select>

                <label for="tracked">Tracked:</label>
                <input type="text" id="tracked" name="tracked" pattern="\\S*" title="No spaces allowed">

                <button type="submit">Register</button>
            </form>
        </div>
    </body>
    </html>
    """
