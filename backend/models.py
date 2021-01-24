from flask_sqlalchemy import SQLAlchemy

user = "postgres"
password = "123"
host = "localhost"
database_name = "trivia_test"

database_path = "postgresql://{}:{}@{}/{}".format(
    user, password, host, database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


QUESTIONS_PER_PAGE = 8


def paginate_questions(request, questions):
    # adding pagination
    # if arg object page not found assign default to 1
    page = request.args.get('page', 1, type=int)
    start = (page-1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in questions]
    return formatted_questions[start:end]


'''
Question

'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id=db.Column(db.Integer,primary_key=True)
  question = db.Column(db.String())
  answer = db.Column(db.String())
  category = db.Column(db.String())
  difficulty = db.Column(db.String())

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty
    }

'''
Category

'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = db.Column(db.Integer, primary_key=True)
  type = db.Column(db.String())

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }
