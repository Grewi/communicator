#!/usr/bin/env python3

import http.server
import json
import tls_response
from http import HTTPStatus

class http(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.handle_request()
    
    def do_POST(self):
        self.handle_request()
    
    def handle_request(self):
        conn_type = self.detect_connection_type()
        
        if conn_type == "mtls":
            response = self.gr_handle_mtls()
        else:
            response = self.gr_handle_tls()

        if response is not None:
            self.send_response(HTTPStatus.OK)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(json.dumps(response))))
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")

    
    def detect_connection_type(self):
        sock = self.connection
        
        if hasattr(sock, 'getpeercert'):
            try:
                cert = sock.getpeercert()
                if cert:
                    return "mtls"
            except Exception:
                pass
        
        return "self_signed"
    
    def gr_handle_mtls(self):
        print("mtls")
        return {
            "type": "mtls"
        }


    def gr_handle_tls(self):
        print("tls")

        # Если прилетел запрос с заголовком поиска 
        if self.get_header_value('X-Communicator-Search') is not None:
            return tls_response.communicator()
        
        if self.path == "/":
            return {}    
        
        return None

    def get_header_value(self, header_name: str, default: str | None = None) -> str | None:

        value = self.headers.get(header_name)
        print(value)
        if value is None:
            return default
        
        return value
