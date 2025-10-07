import sys
import os
import json

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Set the working directory to project root
os.chdir(project_root)

try:
    from app import app
    from serverless_wsgi import handle_request
except ImportError as e:
    app = None
    handle_request = None
    import_error = str(e)

def handler(event, context):
    """
    Netlify Functions handler for Flask app
    """
    try:
        if app is None or handle_request is None:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Import failed',
                    'details': import_error if 'import_error' in locals() else 'Unknown import error'
                })
            }
        
        # Handle the request with serverless WSGI
        return handle_request(app, event, context)
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Function execution failed',
                'details': str(e),
                'path': event.get('path', 'unknown'),
                'method': event.get('httpMethod', 'unknown')
            })
        }