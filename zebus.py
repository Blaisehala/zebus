from flask import Flask,render_template
app = Flask(__name__)


posts = [
  
  {
    'author': 'Blaise Hala',
    'title': 'Blog Post',
    'content': 'First post content ',
    'dete_posted':'April 2014'
  },

 {
    'author': 'Blaise Hala',
    'title': 'Blog Post',
    'content': 'First post content',
    'date_posted':'April 2014'
 }
]


@app.route('/')
@app.route ('/home')
def home():
  return render_template ('home.html', posts=posts)



@app.route('/about')
def about():
  return render_template('about.html')


  if __name__ == '__main__':  
    app.run(debug = True)