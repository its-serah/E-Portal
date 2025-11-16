import os

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/')
    
    # Serve index.html for root and root index requests
    if path == '/' or path == '/index.html':
        with open('index.html', 'rb') as f:
            content = f.read()
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [content]
    
    # Serve other files (css, js, etc)
    file_path = '.' + path
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        
        # Determine content type
        if file_path.endswith('.css'):
            content_type = 'text/css'
        elif file_path.endswith('.js'):
            content_type = 'application/javascript'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
            content_type = 'image/jpeg'
        else:
            content_type = 'text/plain'
        
        start_response('200 OK', [('Content-Type', content_type)])
        return [content]
    
    # 404
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'404 Not Found']
