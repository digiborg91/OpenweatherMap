from bottle import route, request, debug, run, template, static_file

@route('/images/<ireland>')
def send_image(ireland):
	return static_file(ireland, root='./images/')

@route('/')
def index():
	return template('weatherMap.tpl')
	
debug(True)
run(reloader=True)