from utils import make_response


def favicon(request, client_socket):
    response = make_response(404, "Not Found", keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))
    if not request.connection:
        client_socket.close()


def page_400(request, client_socket):
    response = make_response(400, """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>400 Bad Request</title>
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
            overflow: hidden;
            animation: fadeIn 1s ease-in-out;
        }
        .container {
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .error-message {
            position: absolute;
            white-space: nowrap;
            text-align: center;
        }
        .error-code {
            font-size: 6em;
            margin: 0;
        }
        .error-text {
            font-size: 2.5em;
            margin: 0;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div id="error-message" class="error-message">
            <div class="error-code">400</div>
            <div class="error-text">Bad Request</div>
        </div>
    </div>
    <script>
        const errorMessage = document.getElementById('error-message');
        const container = document.querySelector('.container');

        let angle = Math.random() * 2 * Math.PI;
        let speed = 3; // Увеличена скорость
        let x = container.clientWidth / 2 - errorMessage.clientWidth / 2;
        let y = container.clientHeight / 2 - errorMessage.clientHeight / 2;

        function moveErrorMessage() {
            x += Math.cos(angle) * speed;
            y += Math.sin(angle) * speed;

            if (x + errorMessage.clientWidth >= container.clientWidth || x <= 0) {
                angle = Math.PI - angle;
            }
            if (y + errorMessage.clientHeight >= container.clientHeight || y <= 0) {
                angle = -angle;
            }

            errorMessage.style.left = `${x}px`;
            errorMessage.style.top = `${y}px`;

            requestAnimationFrame(moveErrorMessage);
        }

        moveErrorMessage();
    </script>
</body>
</html>
""", keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))


def page_403(request, client_socket):
    response = make_response(403, """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Forbidden</title>
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
            text-align: center;
        }
        h1 {
            font-size: 100px;
            margin-bottom: 20px;
            animation: shake 0.5s infinite;
        }
        p {
            font-size: 24px;
            color: #999;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            50% { transform: translateX(5px); }
            75% { transform: translateX(-5px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>403</h1>
        <p>Forbidden</p>
    </div>
</body>
</html>
    """, keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))


def page_404(request, client_socket):
    response = make_response(404, """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 Not Found</title>
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
            text-align: center;
        }
        h1 {
            font-size: 100px;
            margin-bottom: 20px;
            animation: fadeInOut 2s infinite;
        }
        p {
            font-size: 24px;
            color: #999;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeInOut {
            0%, 100% { opacity: 0; }
            50% { opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <p>Not Found</p>
    </div>
</body>
</html>
""", keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))


def page_405(request, client_socket):
    response = make_response(405, """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>405 Method Not Allowed</title>
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
            text-align: center;
        }
        h1 {
            font-size: 100px;
            margin-bottom: 20px;
            animation: rotate 2s infinite linear;
        }
        p {
            font-size: 24px;
            color: #999;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>405</h1>
        <p>Method Not Allowed</p>
    </div>
</body>
</html>

""", keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))


def page_500(request, client_socket):
    response = make_response(500, """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 Internal Server Error</title>
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
            text-align: center;
        }
        h1 {
            font-size: 100px;
            margin-bottom: 20px;
            animation: pulse 1s infinite;
        }
        p {
            font-size: 24px;
            color: #999;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>500</h1>
        <p>Internal Server Error</p>
    </div>
</body>
</html>

""", keep_alive=request.connection)
    client_socket.sendall(response.encode('utf-8'))
