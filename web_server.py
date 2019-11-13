from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from context_windows import ContextWindow
from context_windows import Contexter
from search_engine import SearchEngine
from indexation import PositionByLine

class RequestHandler(BaseHTTPRequestHandler):
    '''
    This class creates a html page on which a user
    can perform search by clicking a button 'search.
    It also shows the results of a search for the given query.
    '''

    def do_GET(self):
        '''
        This method creates a html page on which a user
        can perform search by clicking a button 'search'.
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
        self.wfile.write(bytes(html, encoding = "utf-8"))
           
    def do_POST(self):
        '''
        This method shows the search results.
        '''
        # Create an object of the FieldStorage to read
        # the form contents from standard input or the environment 
        form = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ ={'REQUEST_METHOD':'POST'})
        # Get the user's query from the form.
        query = form.getvalue('query')
        # Create a search engine.
        search_engine = SearchEngine('database')
        # Search user's query and write them to 'search_results'.
        search_results = search_engine.multi_search(query)
        # Create an object of the 'Contexter' class to get context windows.
        self.contexter = Contexter()
        # Get context windows and make the query words bold.
        cws = self.contexter.get_bold_cws(search_results, 3)       
        # Send tags to indicate the beginning of the html body of the page
        # and start an ordered list.
        self.wfile.write(bytes('<html><form><body><ol>', encoding = "cp1251"))
        # Post each file name as an element of an ordered list.
        for i, file_name in enumerate(cws):
            self.wfile.write(bytes('<li><p>%s</p></i>' % file_name, encoding = "utf-8"))            
            self.wfile.write(bytes('<ul>', encoding = "cp1251"))
            # Post each quote from the file as an element of an unordered list.
            for cw in cws[file_name]:
                self.wfile.write(bytes('<li><p>%s</p></i>' % cw.line, encoding = "cp1251"))
            self.wfile.write(bytes('</ul>', encoding = "cp1251"))
        # Send tags to mark the end of the html body.
        self.wfile.write(bytes('</ol></form></body></html>', encoding = "cp1251"))          
          
if __name__ == '__main__':       
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()
    
