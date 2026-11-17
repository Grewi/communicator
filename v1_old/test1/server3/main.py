#!/usr/bin/env python3

import http.server
import socketserver
import server as main_server

def start_server(host, port, certfile, keyfile, ca_certs):
    handler = main_server.http
    s = socketserver.ThreadingTCPServer((host, port), handler)
    return s

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8001
    CERT_FILE = 'server.crt'
    KEY_FILE = 'server.key'
    CA_CERTS = 'ca.crt'

    try:
        print("Start server http://" + HOST + ":" + str(PORT))
        s = start_server(HOST, PORT, CERT_FILE, KEY_FILE, CA_CERTS)
        s.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        s.shutdown()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()        