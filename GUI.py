from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required

from content_fix import Content
from download_txt import SimpleToTW

from test2 import Book, bookstore_new, bookstore_update
from JsonInit import JsonFile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
manager = Manager(app)


class NovelForm(FlaskForm):
    name = StringField('Title: ')
    author = StringField('author: ')
    url = StringField('URL: ')
    finish = RadioField('Label', choices=[("True", '已完結'), ("False", '連載中')])
    submit = SubmitField('download')


def novel_download():
    novel = Book()
    novel.save("txt", "json")


def content_fix():
    Content().update()


class SettingForm(FlaskForm):
    name = StringField('Title: ', validators=[Required()])
    author = StringField('Author: ', validators=[])
    url = StringField('URL: ', validators=[Required()])
    finish = RadioField('Label', choices=[("True", '已完結'), ("False", '連載中')])
    submit = SubmitField('Save')


class JsonFile(JsonFile):

    def get_info(self):
        return (self.get_title(), self.get_author(), self.get_url(), self.get_finish())

    def set_info(self, name, author, url, finish):
        self.set_title(name)
        self.set_url(url)
        self.set_author(author)
        self.set_finish(finish)


class Data(object):
    def __init__(self, form, name, author, url, finish):
        self.form = form
        self.name = name
        self.author = author
        self.url = url
        self.finish = finish


def convert():
    SimpleToTW().update()
    print("成功！！")


@app.route('/', methods=['POST', 'GET'])
def index():
    download_form = NovelForm()

    name, author, url, finish = JsonFile().get_info()

    if request.method == 'POST':
        if request.form['submit'] == 'download':
            bookstore_new()
            content_fix()
            flash('下載完成！！')
        # elif request.form['submit'] == 'convert':
        #     convert()
        #     flash('轉換成功！！')
        elif request.form['submit'] == 'Bookstore_update':
            bookstore_update()
            flash('更新完畢！！')

    data = Data(download_form, name, author, url, finish)
    return render_template('index.html', data=data)


@app.route('/setting', methods=['POST', 'GET'])
def setting():
    name = None
    author = None
    url = None
    finish = None

    form = SettingForm()

    if form.validate() and request.method == 'POST':
        name = form.name.data
        author = form.author.data
        url = form.url.data
        finish = form.finish.data

        print(form.name.data)
        print(form.author.data)
        print(form.url.data)
        print(form.finish.data)

        JsonFile().set_info(name, author, url, finish)
        print(JsonFile().get_finish())

        flash('設定成功!!')

    data = Data(form, name, author, url, finish)

    return render_template('setting.html', data=data)


if __name__ == '__main__':
    manager.run()
