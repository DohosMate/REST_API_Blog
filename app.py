from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os.path import isfile

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize the app with the extension
db.init_app(app)


class Article(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    title= db.Column(db.String(200), unique=True, nullable=False)
    article_description= db.Column(db.Text())

    def __repr__(self):
        return f"{self.id}.  {self.title} - {self.timestamp}"


if not isfile('instance\database.db'):
    print("Create database.db")    
    with app.app_context():
           db.create_all()
           

@app.route('/')
def welcome():
    return 'REST API Blog welcome. Options: /getall, /getid<id>, /add, update<id>, delete<id> '

@app.route('/getall')
def get_articles():
    articles= Article.query.all()
    output= []
    for article in articles:
        article_data= {"id": article.id,
                         "timestamp": article.timestamp,
                         "title": article.title,
                         "article_description": article.article_description}
        output.append(article_data)
    return {"articles": output}

@app.route('/getid<id>')     
def get_article(id):
    article= Article.query.get_or_404(id)
    return {"id": article.id,
            "timestamp": article.timestamp,
            "title": article.title,
            "article_description": article.article_description}

@app.route('/add', methods=['POST'])
def add_article():
    article= Article(title= request.json["title"], article_description= request.json["article_description"])
    db.session.add(article)
    db.session.commit()
    return {"id": article.id}

@app.route('/update<id>', methods=['PATCH'])
def update_article(id):
    updated_article= Article.query.get_or_404(id)
    updated_article.title = request.json["title"]
    updated_article.article_description= request.json["article_description"]
    db.session.commit()
    return {"id": updated_article.id}

@app.route('/delete<id>', methods=['DELETE'])
def delete_article(id):
    article= Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return {'deleted': article.title}


if __name__ == '__main__':
    app.run()