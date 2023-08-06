flask-admin-ckeditor
====================
simple!



```python
#coding:utf8
import peewee
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

from flask_admin_ckeditor import init_app,ModelViewMixin,CKTextAreaField

# flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
db = peewee.SqliteDatabase('test.sqlite', check_same_thread=False)

class BaseModel(peewee.Model):
	class Meta:
		database = db

# model
class Article(BaseModel):
	html = peewee.CharField(max_length=80,null=True)

# view
class ArticleView(ModelViewMixin,ModelView):
	html_field = 'html'
	form_overrides = {
		'html': CKTextAreaField
	}

# admin
admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ArticleView(Article))

# init
init_app(app)

if __name__ == '__main__':
	try:
		Article.create_table()
	except:
		pass
	app.run(debug=True)
```

done http://127.0.0.1:5000/admin
