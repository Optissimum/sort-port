#!flask/bin/python
from app import app
app.run(debug=True)
@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response
