from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestHandler(BaseHTTPRequestHandler):
    '''
    This module creates a html page on which a user
    can perform search by clicking a button 'search.
    '''

    def do_GET(self):
        '''
        This module creates a html page on which a user
        can perform search by clicking a button 'search.
        Handling of a request of type GET.
        '''

        # Send response to the browser that the requested page was found.
        self.send_response(200)

        # Establish that the content must be interpreted as
        # html mark up.
        self.send_header("Content-type", "text/html; charset=utf-8")

        # The end of the headers.
        self.end_headers()

        # The html structure of the future search page.
        html = '''
                <html>
                    <body>
                        <form method="post">
                            <input type="text" name="query">
                            <input type="submit" value="Search">
                        </form>
                    </body>
                </html>
                '''
        # Sends the html structure as a string of bytes to browser.
        self.wfile.write(bytes(html, encoding="utf-8"))

if __name__ == '__main__':       
    h = HTTPServer(('', 80), RequestHandler)
    h.serve_forever()
