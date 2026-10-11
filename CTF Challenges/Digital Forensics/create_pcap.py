from scapy.all import IP, TCP, Raw, wrpcap
from PIL import Image, ImageDraw
import io
import os


# =========================================================
# CREATE HIDDEN EVIDENCE IMAGE
# =========================================================

img = Image.new("RGB", (900, 500), "white")
draw = ImageDraw.Draw(img)

draw.text(
    (100, 200),
    "RECOVERED EVIDENCE",
    fill="black"
)

draw.text(
    (100, 250),
    "TECH{missing_evidence}",
    fill="black"
)

image_buffer = io.BytesIO()
img.save(image_buffer, format="PNG")
image_data = image_buffer.getvalue()


# =========================================================
# HTTP MULTIPART UPLOAD
# =========================================================

boundary = "----CyberArenaBoundary"

body_start = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="evidence"; filename="evidence.png"\r\n'
    "Content-Type: image/png\r\n"
    "\r\n"
).encode()

body_end = (
    f"\r\n--{boundary}--\r\n"
).encode()

http_body = body_start + image_data + body_end


http_request = (
    f"POST /upload HTTP/1.1\r\n"
    f"Host: evidence-server.local\r\n"
    f"Content-Type: multipart/form-data; boundary={boundary}\r\n"
    f"Content-Length: {len(http_body)}\r\n"
    f"User-Agent: CyberArena-Investigator\r\n"
    f"\r\n"
).encode() + http_body


http_response = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: text/plain\r\n"
    b"Content-Length: 25\r\n"
    b"\r\n"
    b"Evidence received safely."
)


# =========================================================
# TCP PACKETS
# =========================================================

client_ip = "10.10.10.20"
server_ip = "10.10.10.10"

client_port = 49152
server_port = 80

packets = []

seq_client = 1000
seq_server = 5000


# TCP handshake
packets.append(
    IP(src=client_ip, dst=server_ip) /
    TCP(
        sport=client_port,
        dport=server_port,
        flags="S",
        seq=seq_client
    )
)

packets.append(
    IP(src=server_ip, dst=client_ip) /
    TCP(
        sport=server_port,
        dport=client_port,
        flags="SA",
        seq=seq_server,
        ack=seq_client + 1
    )
)

packets.append(
    IP(src=client_ip, dst=server_ip) /
    TCP(
        sport=client_port,
        dport=server_port,
        flags="A",
        seq=seq_client + 1,
        ack=seq_server + 1
    )
)


# =========================================================
# HTTP REQUEST
# =========================================================

request_data = http_request

packets.append(
    IP(src=client_ip, dst=server_ip) /
    TCP(
        sport=client_port,
        dport=server_port,
        flags="PA",
        seq=seq_client + 1,
        ack=seq_server + 1
    ) /
    Raw(load=request_data)
)


# =========================================================
# HTTP RESPONSE
# =========================================================

packets.append(
    IP(src=server_ip, dst=client_ip) /
    TCP(
        sport=server_port,
        dport=client_port,
        flags="PA",
        seq=seq_server + 1,
        ack=seq_client + 1 + len(request_data)
    ) /
    Raw(load=http_response)
)


# Final ACK
packets.append(
    IP(src=client_ip, dst=server_ip) /
    TCP(
        sport=client_port,
        dport=server_port,
        flags="A",
        seq=seq_client + 1 + len(request_data),
        ack=seq_server + 1 + len(http_response)
    )
)


# =========================================================
# WRITE PCAP
# =========================================================

output_file = "evidence.pcap"

wrpcap(output_file, packets)

print("========================================")
print("Cyber Arena forensic PCAP created!")
print("========================================")
print(f"File: {os.path.abspath(output_file)}")
print("Packets:", len(packets))
print("Hidden file: evidence.png")
print("Flag: TECH{missing_evidence}")