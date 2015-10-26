from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import urllib
import json

#print f.read()

class PostHandler(BaseHTTPRequestHandler):
    
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        

        username = ''
        password = ''

        if 'u' in form.keys():
            username = form['u'].value
        if 'p' in form.keys():
            password = form['p'].value

        if username == 'admin' and password != '':
            id_file = open("ids.txt")
            ids = json.loads(id_file.read())

            for key in ids: #varre dicionario
                if ids[key][1] == username and ids[key][0] == password:
                    
                    self.send_response(200)
                    self.end_headers()

                    log = open("log/operative_log.log");
                    content = log.read()

                    self.wfile.write(content)

                    return
                    break

        self.send_response(401)
        self.end_headers()

	
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
