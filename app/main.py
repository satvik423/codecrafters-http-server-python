import socket
import threading

def handle_client(client_socket):
    # Receive the request
    request = client_socket.recv(1024).decode("utf-8")
    print(f"Received request:\n{request}")
    
    # Extract the path from the request line
    try:
        request_line = request.split("\r\n")[0]
        method, path, http_version = request_line.split(" ")
        print(f"Requested path: {path}")

        # Handle the /echo/{str} endpoint
        if path.startswith("/echo/"):
            echo_str = path[len("/echo/"):]
            response_body = echo_str
            content_type = "text/plain"
            content_length = len(response_body)
            response = (
                f"HTTP/1.1 200 OK\r\n"
                f"Content-Type: {content_type}\r\n"
                f"Content-Length: {content_length}\r\n"
                f"\r\n"
                f"{response_body}"
            )
        # Handle the /user-agent endpoint
        elif path == "/user-agent":
            # Extract User-Agent header
            headers = request.split("\r\n")[1:]
            user_agent = None
            for header in headers:
                if header.lower().startswith("user-agent:"):
                    user_agent = header.split(": ", 1)[1]
                    break

            if user_agent:
                response_body = user_agent
                content_type = "text/plain"
                content_length = len(response_body)
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {content_length}\r\n"
                    f"\r\n"
                    f"{response_body}"
                )
            else:
                response = "HTTP/1.1 400 Bad Request\r\n\r\n"
        else:
            # Define valid paths
            valid_paths = ["/", "/index.html"]

            if path in valid_paths:
                response_body = "<html><body><h1>Welcome</h1></body></html>"
                content_type = "text/html"
                content_length = len(response_body)
                response = (
                    f"HTTP/1.1 200 OK\r\n"
                    f"Content-Type: {content_type}\r\n"
                    f"Content-Length: {content_length}\r\n"
                    f"\r\n"
                    f"{response_body}"
                )
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"

    except ValueError:
        response = "HTTP/1.1 400 Bad Request\r\n\r\n"

    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    print("Server started on port 4221")

    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address} has been established.")
        
        # Start a new thread for each client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
