page = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #282c34;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            animation: fadeIn 1s ease-in-out;
        }
        .container {
            background-color: #333;
            padding: 5%;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            width: 80%;
            max-width: 400px;
            text-align: center;
        }
        h2 {
            margin-bottom: 5%;
            font-size: 2em;
        }
        label {
            display: block;
            margin-bottom: 2%;
            font-weight: bold;
        }
        input[type="text"],
        input[type="password"],
        input[type="number"] {
            width: 100%;
            padding: 5%;
            margin-bottom: 5%;
            border: 1px solid #555;
            border-radius: 4px;
            background-color: #444;
            color: #fff;
        }
        input[type="submit"] {
            width: 100%;
            padding: 5%;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 1.2em;
            transition: background-color 0.3s ease;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Register</h2>
        <form action="/register" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>

            <label for="tracked">Tracked Class:</label>
            <input placeholder="optional" type="text" id="tracked" name="tracked">

            <label for="school">School Number:</label>
            <input type="number" id="school" name="school" required>

            <input type="submit" value="Register">
        </form>
    </div>
</body>
</html>
"""
