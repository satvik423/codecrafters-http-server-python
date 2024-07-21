# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client_socket, address = server_socket.accept() # wait for client
        print(f"Connection from {address} has been established.")
        
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
            else:
                # Define valid paths
                valid_paths = ["/", "/index.html"]

                if path in valid_paths:
                    response = "HTTP/1.1 200 OK\r\n\r\n"
                else:
                    response = "HTTP/1.1 404 Not Found\r\n\r\n"

        except ValueError:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"

        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()

if __name__ == "__main__":
    main()
