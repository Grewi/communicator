#!/usr/bin/env python3
import http.server
import ssl
import json
import os
import socketserver
import urllib.request
import urllib.error
from urllib.parse import urlparse
import sys
import warnings

# Отключаем предупреждения о небезопасных соединениях
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=ResourceWarning)


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    Обработчик HTTP-запросов, который определяет тип подключения
    и перенаправляет на соответствующий драйвер.
    """
    
    def do_GET(self):
        """Обработка GET-запросов"""
        self.handle_request()
    
    def do_POST(self):
        """Обработка POST-запросов"""
        self.handle_request()
    
    def handle_request(self):
        """Основной обработчик запросов с определением типа подключения"""
        conn_type = self.detect_connection_type()
        
        if conn_type == "mtls":
            response = self.handle_mtls()
        else:
            response = self.handle_self_signed()
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def detect_connection_type(self) -> str:
        """Определяет тип подключения по наличию клиентского сертификата."""
        sock = self.connection
        
        if hasattr(sock, 'getpeercert'):
            try:
                cert = sock.getpeercert()
                if cert:
                    return "mtls"
            except Exception:
                pass
        
        return "self_signed"
    
    def handle_mtls(self):
        """Драйвер для mTLS-подключений."""
        cert_info = self.get_client_cert_info()
        
        # Здесь можно сделать запрос к другому серверу
        # client = MTLSClient()
        # response = client.get('https://another-server:8443/')
        
        return {
            "status": "success",
            "driver": "mtls_driver",
            "connection_type": "mTLS",
            "client_cert": cert_info,
            "path": self.path,
            "method": self.command
        }
    
    def handle_self_signed(self):
        """Драйвер для обычных HTTPS-подключений."""
        return {
            "status": "success",
            "driver": "self_signed_driver",
            "connection_type": "Self-signed HTTPS",
            "client_cert": None,
            "path": self.path,
            "method": self.command
        }
    
    def get_client_cert_info(self):
        """Извлекает информацию о клиентском сертификате."""
        try:
            cert = self.connection.getpeercert()
            if cert:
                subject = cert.get('subject', [])
                dn_parts = []
                for part in subject:
                    for key, value in part:
                        dn_parts.append(f"{key}={value}")
                dn = ', '.join(dn_parts) if dn_parts else None
                
                return {
                    "subject": dn,
                    "issuer": cert.get('issuer', []),
                    "not_before": cert.get('notBefore', ''),
                    "not_after": cert.get('notAfter', ''),
                    "serial_number": cert.get('serialNumber', '')
                }
        except Exception:
            pass
        return None
    
    def log_message(self, format, *args):
        """Переопределяем логирование."""
        conn_type = self.detect_connection_type()
        print(f"[{conn_type.upper()}] {format % args}")


class MTLSClient:
    """
    HTTP-клиент с поддержкой mTLS.
    Для mTLS не требует проверки сертификата сервера.
    """
    
    def __init__(self, cert_file='client.crt', key_file='client.key'):
        """
        Инициализация mTLS-клиента.
        
        Args:
            cert_file: Путь к клиентскому сертификату
            key_file: Путь к приватному ключу клиента
        """
        self.cert_file = cert_file
        self.key_file = key_file
        
        # Создаем SSL-контекст без проверки сертификата сервера
        self.context = self._create_ssl_context()
    
    def _create_ssl_context(self):
        """
        Создает SSL-контекст для mTLS-подключений.
        При mTLS проверка сертификата сервера не требуется.
        """
        # Создаем контекст
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        
        # ОТКЛЮЧАЕМ проверку сертификата сервера (не нужна при mTLS)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Загружаем клиентский сертификат для mTLS
        if os.path.exists(self.cert_file) and os.path.exists(self.key_file):
            try:
                context.load_cert_chain(certfile=self.cert_file, keyfile=self.key_file)
                print(f"[CLIENT] Loaded client certificate: {self.cert_file}")
            except Exception as e:
                print(f"[CLIENT] Warning: Failed to load client certificate: {e}")
        else:
            print(f"[CLIENT] Warning: Client certificates not found: {self.cert_file}, {self.key_file}")
            print("[CLIENT] Using without client certificate (regular HTTPS)")
        
        return context
    
    def _make_request(self, method, url, data=None, headers=None):
        """
        Выполняет HTTP-запрос с поддержкой mTLS.
        """
        # Создаем обработчик с SSL контекстом
        https_handler = urllib.request.HTTPSHandler(context=self.context)
        opener = urllib.request.build_opener(https_handler)
        
        # Подготавливаем данные
        if data:
            data = json.dumps(data).encode('utf-8')
            if not headers:
                headers = {'Content-Type': 'application/json'}
        
        # Создаем запрос
        req = urllib.request.Request(url, data=data, method=method)
        
        # Добавляем заголовки
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        try:
            with opener.open(req) as response:
                response_data = response.read().decode('utf-8')
                try:
                    return json.loads(response_data)
                except json.JSONDecodeError:
                    return {"raw_response": response_data}
        except urllib.error.HTTPError as e:
            return {
                "error": f"HTTP Error: {e.code} {e.reason}",
                "body": e.read().decode('utf-8') if e.fp else None
            }
        except urllib.error.URLError as e:
            return {
                "error": f"URL Error: {str(e)}"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get(self, url, headers=None):
        """GET запрос."""
        return self._make_request('GET', url, headers=headers)
    
    def post(self, url, data=None, headers=None):
        """POST запрос."""
        return self._make_request('POST', url, data=data, headers=headers)
    
    def put(self, url, data=None, headers=None):
        """PUT запрос."""
        return self._make_request('PUT', url, data=data, headers=headers)
    
    def delete(self, url, headers=None):
        """DELETE запрос."""
        return self._make_request('DELETE', url, headers=headers)


def create_https_server(host='0.0.0.0', port=8443, 
                        certfile='server.crt', 
                        keyfile='server.key',
                        ca_certs='ca.crt'):
    """
    Создает HTTPS-сервер с поддержкой mTLS.
    """
    handler = CustomHTTPRequestHandler
    server = socketserver.ThreadingTCPServer((host, port), handler)
    
    # Создаем SSL-контекст
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Загружаем серверный сертификат
    if os.path.exists(certfile) and os.path.exists(keyfile):
        context.load_cert_chain(certfile=certfile, keyfile=keyfile)
        print(f"[SERVER] Loaded server certificate: {certfile}")
    else:
        print(f"[SERVER] Error: Server certificates not found")
        sys.exit(1)
    
    # НЕ ТРЕБУЕМ клиентский сертификат (опционально)
    context.verify_mode = ssl.CERT_OPTIONAL
    
    # Загружаем CA только для проверки клиентских сертификатов
    if os.path.exists(ca_certs):
        context.load_verify_locations(cafile=ca_certs)
        print(f"[SERVER] Loaded CA certificates: {ca_certs}")
    else:
        print(f"[SERVER] Warning: CA certificates not found")
        print("[SERVER] Client certificate verification will be disabled")
        context.verify_mode = ssl.CERT_NONE
    
    server.socket = context.wrap_socket(server.socket, server_side=True)
    
    print(f"\n[SERVER] HTTPS/mTLS server running on https://{host}:{port}")
    print(f"[SERVER] Client certificates: {'Optional' if context.verify_mode == ssl.CERT_OPTIONAL else 'Disabled'}")
    print("[SERVER] Press Ctrl+C to stop\n")
    
    return server


def test_mtls_client():
    """
    Тестовая функция для демонстрации работы mTLS-клиента.
    """
    print("\n" + "="*60)
    print("TESTING mTLS CLIENT")
    print("="*60)
    
    # Создаем mTLS-клиент (без проверки сертификата сервера)
    client = MTLSClient(
        cert_file='client.crt',
        key_file='client.key'
    )
    
    # GET запрос
    print("\n1. Making mTLS GET request:")
    response = client.get('https://localhost:8443/')
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # POST запрос
    print("\n2. Making mTLS POST request:")
    data = {"test": "data", "message": "Hello from mTLS client"}
    response = client.post('https://localhost:8443/', data=data)
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # Запрос к другому серверу
    print("\n3. Making mTLS request to another server:")
    response = client.get('https://localhost:8443/')
    if "error" in response:
        print(f"Expected error (server not found): {response['error']}")
    else:
        print(f"Response: {json.dumps(response, indent=2)}")


if __name__ == "__main__":
    # Параметры сервера
    HOST = '0.0.0.0'
    PORT = 8442
    CERT_FILE = 'server.crt'
    KEY_FILE = 'server.key'
    CA_CERTS = 'ca.crt'
    
    # Проверяем наличие файлов
    required_files = [CERT_FILE, KEY_FILE, CA_CERTS]
    missing = [f for f in required_files if not os.path.exists(f)]
    
    if missing:
        print(f"Error: Required files not found: {', '.join(missing)}")
        print("\nTo generate certificates, run:")
        print("  # Generate CA")
        print(f"  openssl req -x509 -newkey rsa:4096 -keyout ca.key -out {CA_CERTS} -days 365 -nodes -subj '/CN=My CA'")
        print("  # Generate server certificate")
        print(f"  openssl req -newkey rsa:4096 -keyout {KEY_FILE} -out server.csr -nodes -subj '/CN=localhost'")
        print(f"  openssl x509 -req -days 365 -in server.csr -CA {CA_CERTS} -CAkey ca.key -set_serial 01 -out {CERT_FILE}")
        print("  # Generate client certificate")
        print("  openssl req -newkey rsa:4096 -keyout client.key -out client.csr -nodes -subj '/CN=client'")
        print("  openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 02 -out client.crt")
        print("  # Cleanup")
        print("  rm server.csr client.csr ca.key")
        sys.exit(1)
    
    # Запускаем сервер
    try:
        server = create_https_server(HOST, PORT, CERT_FILE, KEY_FILE, CA_CERTS)
        
        # Если передан аргумент --test
        if len(sys.argv) > 1 and sys.argv[1] == '--test':
            import time
            print("Waiting 2 seconds for server to start...")
            time.sleep(2)
            test_mtls_client()
            print("\n" + "="*60)
            print("Test completed. Server continues running.")
            print("Press Ctrl+C to stop")
            print("="*60)
        
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.shutdown()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()