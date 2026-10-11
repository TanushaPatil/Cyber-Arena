import socket
import random
import base64
import time


HOST = "127.0.0.1"
PORT = 5002

FLAG = "TECH{final_puzzle}"


def generate_question():
    a = random.randint(10, 99)
    b = random.randint(10, 99)

    operation = random.choice(["+", "-", "*"])

    if operation == "+":
        answer = a + b
        question = f"{a} + {b}"

    elif operation == "-":
        answer = a - b
        question = f"{a} - {b}"

    else:
        answer = a * b
        question = f"{a} * {b}"

    return question, answer


def start_server():

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind(
        (HOST, PORT)
    )

    server.listen(5)

    print("=" * 50)
    print("CYBER ARENA - FINAL PUZZLE SERVER")
    print("=" * 50)
    print(f"Listening on {HOST}:{PORT}")
    print("Waiting for participant...")
    print()

    while True:

        conn, address = server.accept()

        print(
            f"[+] Connection from {address}"
        )

        try:

            conn.sendall(
                b"\nCYBER ARENA - THE FINAL PUZZLE\n"
            )

            conn.sendall(
                b"Solve 20 mathematical questions.\n"
            )

            conn.sendall(
                b"You have 20 seconds.\n\n"
            )

            start_time = time.time()

            for number in range(1, 21):

                question, answer = generate_question()

                message = (
                    f"[{number}/20] {question} = ?\n"
                    f"Answer: "
                )

                conn.sendall(
                    message.encode()
                )

                data = conn.recv(1024)

                if not data:
                    break

                elapsed = time.time() - start_time

                if elapsed > 20:

                    conn.sendall(
                        b"\nTIME OUT!\n"
                    )

                    break

                try:

                    user_answer = int(
                        data.decode().strip()
                    )

                except ValueError:

                    conn.sendall(
                        b"Invalid answer.\n"
                    )

                    break

                if user_answer != answer:

                    conn.sendall(
                        b"Wrong answer. Challenge failed.\n"
                    )

                    break

            else:

                # All 20 questions were solved
                encoded_flag = base64.b64encode(
                    FLAG.encode()
                ).decode()

                conn.sendall(
                    b"\nAll answers correct!\n"
                )

                conn.sendall(
                    b"One final encoded value was recovered:\n"
                )

                conn.sendall(
                    f"{encoded_flag}\n".encode()
                )

                conn.sendall(
                    b"\nDecode it to obtain the flag.\n"
                )

        except Exception as error:

            print(
                f"[!] Error: {error}"
            )

        finally:

            conn.close()

            print(
                "[+] Connection closed"
            )


if __name__ == "__main__":
    start_server()