#!/usr/bin/env python3

import http.server
import json
import requestKey


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
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(json.dumps(response))))
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
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

        # Указываем адрес хоста для которого хоти получить ключ
        return requestKey.key("localhost:8003")
  

    def get_header_value(self, header_name: str, default: str | None = None) -> str | None:

        value = self.headers.get(header_name)
        print(value)
        if value is None:
            return default
        
        return value