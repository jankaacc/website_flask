
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate
from flaskext.markdown import Markdown
from flask_uploads import UploadSet, configure_uploads, IMAGES



app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

#migrations
migrate = Migrate(app, db)

#markdown
Markdown(app)

# images
uploaded_images = UploadSet('images',IMAGES)
configure_uploads(app, uploaded_images)

from application.blog import views
from application.author import views

print(__name__)
if __name__ == 'application':
    app.run()