# Importing asyncio for asynchronous operations
import asyncio

# Importing os to check if files exist
import os

# Import parse_qs to handle POST form data
from urllib.parse import parse_qs

# Handle client connections
async def handle_client(reader, writer):
    # Read up to 1024 bytes of data from the client
    data = await reader.read(1024)
    # Decode the bytes into a string
    message = data.decode()

    # If there is no message, close the connection
    if not message:
        writer.close()
        await writer.wait_closed()
        return

    # Get the first line of the request (e.g., "GET / HTTP/1.1")
    request_line = message.split("\r\n")[0]
    # Split the request into method (GET/POST), path, and protocol (HTTP/1.1)
    method, path, _ = request_line.split()

    # Handle GET requests
    if method == "GET":
        # If path is "/", serve the index.html
        if path == "/":
            await send_file(writer, "templates/index.html")
        # If path is "/register", serve the register.html
        elif path == "/register":
            await send_file(writer, "templates/register.html")
        # If path is not recognized, send 404
        else:
            await send_404(writer)

    # Handling POST requests
    elif method == "POST" and path == "/submit":
        # Get the body (form data) of the POST request
        body = message.split("\r\n\r\n")[1]
        # Parse the form data into a dictionary
        form = parse_qs(body)
        # Get the username field
        username = form.get('username', [''])[0]
        # Get the email field
        email = form.get('email', [''])[0]

        # If both username and email are provided
        if username and email:
            # Open db.txt file and append the new entry
            with open("db.txt", "a") as f:
                f.write(f"{username} {email}\n")
            # Prepare a success response
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Thank you!</h1>"
            # Send the success response back to client
            writer.write(response.encode())
            await writer.drain()
    else:
        
        await send_404(writer)

    # Close the connection
    writer.close()
    await writer.wait_closed()

# Function to send an HTML file to the client/browser
async def send_file(writer, filepath):
    # Check if the file exists
    if os.path.exists(filepath):
        # Open and read the file content
        with open(filepath, "r") as f:
            content = f.read()
        # Prepare the HTTP response with file content
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + content
        # Send the response
        writer.write(response.encode())
        await writer.drain()
    else:
        # If file not found, send 404
        await send_404(writer)

# Function to send a 404 Page Not Found response
async def send_404(writer):
    # Create a basic 404 response
    response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>Page Not Found</h1>"
    # Sending the 404 response
    writer.write(response.encode())
    await writer.drain()

# Main function for starting the server
def main():
    # Creating the event loop
    loop = asyncio.get_event_loop()
    # Creating the server coroutine to listen on localhost:8085
    server_coro = asyncio.start_server(handle_client, "localhost", 8085)
    # Running the server until it's ready
    server = loop.run_until_complete(server_coro)
    print("Server running at http://localhost:8085")
    try:
        # Keep the server running forever
        loop.run_forever()
    except KeyboardInterrupt:
        # Allow manual stop with Ctrl+C
        pass
    # Close the server when done
    server.close()
    loop.run_until_complete(server.wait_closed())
    # Close the event loop
    loop.close()

# If this script is run directly, call main()
if __name__ == "__main__":
    main()
