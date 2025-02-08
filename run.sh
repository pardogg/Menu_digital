#!/bin/bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
#!/bin/bash
gunicorn -w 4 -b 0.0.0.0:$PORT "app:create_app()"

