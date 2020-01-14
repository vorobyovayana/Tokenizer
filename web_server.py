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
                            <input type="text" name="doclimit">
                            <input type="submit" value="doclimit">
                            <input type="text" name="docoffset">
                            <input type="submit" value="docoffset">
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
                            <input type="text" name="doclimit">
                            <input type="submit" value="doclimit">
                            <input type="text" name="docoffset">
                            <input type="submit" value="docoffset">
                        </form>
                    </body>
                </html>
                '''
        # Sends the html structure as a string of bytes to browser.
        self.wfile.write(bytes(html, encoding = "utf-8"))
        # Create an object of the FieldStorage to read
        # the form contents from standard input or the environment 
        form = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ ={'REQUEST_METHOD':'POST'})
        # Get the user's query from the form.
        query = form.getvalue('query')
        # Get the user's doclimit from the form or make it equal 3 by default.
        if form.getvalue('doclimit'):            
            doclimit = int(form.getvalue('doclimit'))
        else:
            doclimit = 3
        # Get the user's docoffset from the form or make it equal 0 by default.
        if form.getvalue('docoffset'):
            docoffset = int(form.getvalue('docoffset')) - 1
        else:
            docoffset = 0
            
        # If docoffset is smaller than zero, send message to a user
        # and raise an exception.
        if docoffset < 0:
            self.wfile.write(bytes('Docoffset has to be one or bigger.', encoding = "utf-8"))
            raise ValueError              
        # Create a search engine.
        search_engine = SearchEngine('database')        
        # Search user's query and write them to 'search_results'.
        search_results = search_engine.multi_search(query)
        # If search_results is empty, send message to a user
        # and raise an exception.
        if search_results == {}:
            self.wfile.write(bytes('Your query is not in the database', encoding = "utf-8"))
            raise ValueError

        # If the docoffset is bigger than the number of documents, 
        # make the latter the doclimit.
        if docoffset > len(search_results):
            docoffset = len(search_results) - 1      
        # Create an object of the 'Contexter' class to get context windows.
        self.contexter = Contexter()
        # Get context windows and make the query words bold.
        cws = self.contexter.get_bold_cws(search_results, 3)
        # The following lines are necessary to put the volumes of "War and Peace"
        # in chronological order.
        sorted_file_names = []
        for file_name in cws:
            sorted_file_names.append(file_name)
            sorted_file_names.sort()            
        # Send tags to indicate the beginning of the html body of the page
        # and start an ordered list.
        self.wfile.write(bytes('<html><form><body><ol>', encoding = "utf-8"))
        for i, fn in enumerate(sorted_file_names):
            if i > docoffset + doclimit:
                break
            if i >= docoffset and i < docoffset + doclimit:
                # Post each file name as an element of an ordered list.
                self.wfile.write(bytes('<li><p>%s</p></i>' % fn, encoding = "utf-8"))            
                self.wfile.write(bytes('<ul>', encoding = "utf-8"))            
                # Post each quote from the file as an element of an unordered list.
                for cw in cws[fn]:
                    self.wfile.write(bytes('<li><p>%s</p></i>' % cw.line, encoding = "utf-8"))
                self.wfile.write(bytes('</ul>', encoding = "utf-8"))
        # Send tags to mark the end of the html body.
        self.wfile.write(bytes('</ol></form></body></html>', encoding = "utf-8"))
          
if __name__ == '__main__':       
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()
