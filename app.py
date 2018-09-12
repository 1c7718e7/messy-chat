import urllib.parse
import json
import logging
import os
import codecs
import base64
from http.cookies import BaseCookie
import asyncio

log = logging.getLogger('app')

MAX_USERNAME = 30
MIN_USERNAME = 3
MAX_PASSWORD = 256
MIN_PASSWORD = 0

SESSIONS = {} # cookie -> user
USERS = {} # user -> password

def gencookie():
	bits = os.urandom(15)
	return base64.b64encode(bits, b'._').decode('ascii')

def inrange(l, x, r):
	return l <= x and x <= r

def validate_creds(user, passwd):
	if len(user) < MIN_USERNAME:
		return 'username'
	if len(passwd) < MIN_PASSWORD:
		return 'password'
	if len(user) > MAX_USERNAME:
		return 'username'
	if len(passwd) > MAX_PASSWORD:
		return 'password'
	return None

def login(user, passwd):
	log.info(f'Attempted login {user}:{passwd}')
	if user in USERS:
		if passwd != USERS[user]:
			return None
	else:
		USERS[user] = passwd
	c = gencookie()
	log.info(f'Succesful login -> {c}')
	SESSIONS[c] = user
	return c

def check_cookie(r):
	def check():
		if 'cookie' not in r.headers:
			return False
		bc = BaseCookie(r.headers['cookie'])
		if 'SESSION' not in bc:
			return False
		sess = bc['SESSION'].value
		log.debug('SESSION = '+sess)
		if sess in SESSIONS:
			log.debug('SESSION IS OK')
			r.user = SESSIONS[sess]
			return True
		return False
	if check():
		return True
	r.start_response(302, 'Found')
	r.send_header('Location', '/login.html')
	r.end_headers()
	return False

MIME_TYPES = {
	'svg': 'image/svg+xml',
	'html': 'text/html',
	'jpg': 'image/jpeg',
	'css': 'text/css',
}

async def serve_file(r, path):
	with open(path, 'rb') as f:
		r.start_response(200, 'OK')
		ext = path[path.rfind('.')+1:]
		if ext in MIME_TYPES:
			r.send_header('Content-Type', MIME_TYPES[ext])
		r.end_headers()
		r.writer.write(f.read())

async def handle_default(r):
	"""Serve a static file"""
	if '../' in r.url.path:
		raise ValueError('../ in url')
	await serve_file(r, 'gen/'+r.url.path)

async def handle_login(r):
	user = r.params.get('login', '')
	passwd = r.params.get('password', '')
	err = validate_creds(user, passwd)
	if err:
		r.start_response(302, 'Found')
		r.send_header('Location', '/login.html#'+err)
		r.end_headers()
		return
	cookie = login(user, passwd)
	if cookie == None:
		r.start_response(302, 'Found')
		r.send_header('Location', '/login.html#failed')
		r.end_headers()
		return
	r.start_response(302, 'Found')
	r.send_header('Location', '/chat')
	r.send_header('Set-Cookie', 'SESSION='+cookie)
	r.end_headers()

async def handle_index(r):
	r.start_response(302, 'Found')
	r.send_header('Location', '/chat')
	r.end_headers()

async def handle_chat(r):
	if not check_cookie(r):
		return
	await serve_file(r, 'gen/chat.html')

def db_load():
	a = []
	try:
		with open('messages.json') as f:
			data = f.read()
		d = json.JSONDecoder()
		while data != '':
			msg, i = d.raw_decode(data)
			data = data[i:]
			a.append(msg)
	except FileNotFoundError:
		return []
	log.info(f"decoded {len(a)} messages")
	return a

POLLERS = []

MESSAGES = db_load()
DB_FILE = open('messages.json', 'a')

def add_message(msg):
	MESSAGES.append(msg)
	DB_FILE.write(json.dumps(msg))
	bs = json.dumps([msg]).encode()
	for p in POLLERS:
		p.write(bs)
		p.close()
	POLLERS.clear()

async def handle_msg_post(r):
	if not check_cookie(r):
		return
	n = int(r.headers['content-length'])
	msg = (await r.reader.read(n)).decode()
	log.info(f'Message from {r.user!r}: {msg!r}')
	add_message({'data': msg, 'user': r.user})

async def handle_msg_get(r):
	if not check_cookie(r):
		return
	r.start_response(200, 'OK')
	r.send_header('Content-Type', 'application/json')
	r.end_headers()
	i = 0
	wait = False
	try: i = int(r.params['id'])
	except: pass
	try: wait = r.params['wait'] == '1'
	except: pass
	if i == len(MESSAGES) and wait:
		reader, writer = r.detach()
		POLLERS.append(writer)
	else:
		r.writer.write(json.dumps(MESSAGES[i:]).encode())

HTTP_HANDLERS = {
	'GET /': handle_index,
	'GET /login': handle_login,
	'GET /chat': handle_chat,
	'POST /msg': handle_msg_post,
	'GET /msg': handle_msg_get,
}
