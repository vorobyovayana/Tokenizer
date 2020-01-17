from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from context_windows import ContextWindow
from context_windows import Contexter
from search_engine import SearchEngine
from indexation import PositionByLine
import time

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
        html = """
                <html>
                    <body>
                        <form method = "post">
                            <input type = 'text' name = 'query' placeholder = 'Insert your query'>
                            <input type = 'submit' value = 'Search'>
                            <br>
                            <input type = 'text' name = 'doclimit' placeholder = 'doclimit'>
                            <input type = 'text' name = 'docoffset' placeholder = 'docoffset'>
                        </form>
                    </body>
                </html>
                """
        # Sends the html structure as a string of bytes to browser.
        self.wfile.write(bytes(html, encoding = "utf-8"))
           
    def do_POST(self):
        '''
        This method shows the search results.
        '''
        # Start the time.
        start_time = time.time()
        # Create an object of the FieldStorage to read
        # the form contents from standard input or the environment 
        form = cgi.FieldStorage(fp = self.rfile, headers = self.headers, environ ={'REQUEST_METHOD':'POST'})
        # Get the user's query from the form.
        query = form.getvalue('query')
        # Get the user's doclimit from the form or make it equal 4 by default.
        if form.getvalue('doclimit'):            
            doclimit = int(form.getvalue('doclimit'))
        else:
            doclimit = 4
        # Get the user's docoffset from the form or make it equal 0 by default.
        if form.getvalue('docoffset') and int(form.getvalue('docoffset')) >= 0 :
            docoffset = int(form.getvalue('docoffset')) - 1
        else:
            docoffset = 0            
        # Create an empty list for limits and offsets for specific
        # documents.
        limofpairs = []
        # Get limits and offsets for specific
        # documents.
        for i in range(doclimit):
            if form.getvalue("cw%slimit" % i):
                cw_limit = int(form.getvalue("cw%slimit" % i))          
            else:
                cw_limit = 1 
            if form.getvalue("cw%soffset" % i):
                 cw_offset = int(form.getvalue("cw%soffset" % i))         
            else:                
                cw_offset = 1
            # Add to the list.    
            limofpairs.append((cw_offset, cw_limit))
        print(limofpairs, 'limofpairs')
        # Send response to the browser that the requested page was found.
        self.send_response(200)        
        # Establish that the content must be interpreted as
        # html mark up.
        self.send_header("Content-type", "text/html; charset=utf-8")        
        # The end of the headers.
        self.end_headers()
        # The html structure to request a user's query, and limit and offset for the documents.
        self.wfile.write(bytes('''
                <html>
                    <body>
                        <form method = 'post'>
                                <label for = "query"> query
                                <input type = 'text' name = 'query' value='%s' placeholder = 'Please, insert your query'>
                                <input type = 'submit' value = 'Search'>
                                <br>
                                <label for = "doclimit"> doclimit
                                <input type = 'text' name = 'doclimit' value = '%s'>
                                <br>
                                <label for = "docoffset"> docoffset
                                <input type = 'text' name = 'docoffset' 'value = '%s'>'''% (query, doclimit, docoffset), encoding = "utf-8"))                  
        # Create a search engine.
        search_engine = SearchEngine('database')        
        # Search user's query and write them to 'search_results'.
        search_results = search_engine.limited_multi_search(query, doclimit, docoffset)
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
        cws = self.contexter.get_bold_cws_limited(search_results, 5, doclimit, docoffset, limofpairs)
        # Put the volumes of "War and Peace" in chronological order.
        sorted_file_names = sorted(cws)
        # Send tags to indicate the beginning of the html body of the page
        # and start an ordered list.
        self.wfile.write(bytes('''<html><body><form><ol>''', encoding = "utf-8"))
        # Iterating through the file names.
        for i, fn in enumerate(sorted_file_names):
            # Exit the cycle if 'i' is out of limit.
            if i >= docoffset + doclimit: 
                break
            if i >= docoffset:
                limofpair = limofpairs[i]
                print(limofpair, 'pair')
                # Post each file name as an element of an ordered list.
                self.wfile.write(bytes('<li><p>%s</p></i>' % fn, encoding = "utf-8"))
                # Create slots for limits and offsets for each specific document.
                self.wfile.write(bytes("""
                                        <label for = "cw%soffset"> offset
                                        <input type = "text" name = "cw%soffset"  value = "%s">
                                        <label for = "cw%slimit"> limit
                                        <input type = "text" name = "cw%slimit"  value = "%s" >
                                        """% (i, i, limofpair[0], i, i, limofpair[1]), encoding="utf-8"))
                # Send the tag to indicate the beginning of the unordered list.
                self.wfile.write(bytes('<ul>', encoding = "utf-8"))
                for t, cw in enumerate(cws[fn]):
                    print(cws[fn], 'cws')
                    print(t, 't')
                    print((limofpair[0] - 1) + limofpair[1], 'sum')
                    print(limofpair[0] - 1, 'offset')
                    if t >= ((limofpair[0] - 1) + limofpair[1]):
                        break
                    if t >= (limofpair[0] - 1):
                        print(t, 't')
                        print((limofpair[0] - 1) + limofpair[1])
                        # Post each quote from the file as an element of an unordered list.
                        self.wfile.write(bytes('<li><p>%s</p></i>' % cw, encoding = "utf-8"))
                self.wfile.write(bytes('</ul>', encoding = "utf-8"))
        # Send tags to mark the end of the html body.
        self.wfile.write(bytes('</ol></form></body></html>', encoding = "utf-8"))
        # Print the time. 
        print('time: ', time.time() - start_time)
          
if __name__ == '__main__':       
    server = HTTPServer(('', 80), RequestHandler)
    server.serve_forever()
