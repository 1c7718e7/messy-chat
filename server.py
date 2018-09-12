import logging
import asyncio
import urllib.parse
import app
import argparse

logging.basicConfig(level=logging.INFO)

log = logging.getLogger('server')

class Request():
	def start_response(self, code, msg=''):
		self.writer.write(f'HTTP/1.0 {code} {msg}\r\n'.encode())
	def send_header(self, key, val):
		self.writer.write(f'{key}: {val}\r\n'.encode())
	def end_headers(self):
		self.writer.write(b'\r\n')
	def detach(self):
		r = self.reader
		w = self.writer
		self.reader = None
		self.writer = None
		return r, w
	def close(self):
		if self.writer:
			self.writer.close()

def parsequery(path):
	i = path.find(' ')
	if i == -1:
		raise ValueError('invalid query line')
	method = path[:i]
	path = path[i+1:]
	i = path.find(' ')
	path = path[:i]
	return method, urllib.parse.urlparse(path)

async def handle_tcp(reader, writer):
	try:
		query = await reader.readline()
		method, url = parsequery(query.decode()[:-1])
		log.info(f'HTTP method:{method!r} {url}')
		f = app.HTTP_HANDLERS.get(method+' '+url.path, app.handle_default)
		r = Request()
		r.writer = writer
		r.reader = reader
		r.headers = {}
		r.method = method
		r.url = url
		r.params = {}
		for k, v in urllib.parse.parse_qsl(r.url.query):
			r.params[k] = v
		while True:
			line = await reader.readline()
			if line == b'\r\n':
				break
			line = line.decode()
			if line[-1] == '\n':
				line = line[:-1]
			i = line.find(': ')
			key = line[:i].lower()
			value = line[i+2:]
			r.headers[key] = value
		await f(r)
		r.close()
	except Exception as e:
		print(e)
		writer.write(b'HTTP/1.0 400 No\r\nContent-Type: text/html\r\n\r\n<h2>No</h2>\njust no')
		writer.close()
		raise e

argp = argparse.ArgumentParser()
argp.add_argument('--bind', default='0.0.0.0', help='Address to bind to')
argp.add_argument('--port', type=int, default=80, help='Port to bind to')
args = argp.parse_args()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_tcp, args.bind, args.port, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
log.info(f'Serving on {server.sockets[0].getsockname()}')
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
log.info('Waiting for connections to close...')
loop.run_until_complete(server.wait_closed())
loop.close()
