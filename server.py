import socket, ssl

HOST, PORT = '127.0.0.1', 1234

def handle(conn):
  print(conn.recv())
  """
  put the kms signing process here
  """
  conn.write(b'HTTP/1.1 200 OK\n\n%s' % conn.getpeername()[0].encode())

def main():
  sock = socket.socket()
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind((HOST, PORT))
  sock.listen(5)
  context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
  context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # 1. key, 2. cert, 3. intermediates
  context.load_verify_locations("root.pem")
  context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  # optional
  context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
  while True:
    conn = None
    ssock, addr = sock.accept()
    try:
      conn = context.wrap_socket(ssock, server_side=True)
      handle(conn)
    except ssl.SSLError as e:
      print(e)
    finally:
      if conn:
        conn.close()
if __name__ == '__main__':
  main()
