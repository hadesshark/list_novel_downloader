from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import Required

from downloader import Novel, SettingInfo
from content_fix import Content
from download_txt import SimpleToTW

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
manager = Manager(app)


class NovelForm(FlaskForm):
    name = StringField('Title: ')
    author = StringField('author: ')
    url = StringField('URL: ')
    finish = RadioField('Label', choices=[('yes','已完結'),('no','連載中')])
    submit = SubmitField('download')

def novel_download(jsonfile):
    novel = Novel(jsonfile)
    novel.save()


def content_fix():
    Content().update()


class SettingForm(FlaskForm):
    name = StringField('Title: ', validators=[Required()])
    author = StringField('Author: ', validators=[])
    url = StringField('URL: ', validators=[Required()])
    finish = RadioField('Label', choices=[('yes','已完結'),('no','連載中')])
    submit = SubmitField('Save')


class JsonFile(SettingInfo):

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
            novel_download(JsonFile())  # 這樣寫不太好，需要改
            content_fix()
            flash('下載完成！！')
        elif request.form['submit'] == 'convert':
            convert()
            flash('轉換成功！！')

    data = Data(download_form, name, author, url, finish)
    return render_template('index.html', data=data)


@app.route('/setting', methods=['POST', 'GET'])
def setting():
    name = None
    author = None
    url = None
    finish = None

    form = SettingForm()
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        author = form.author.data
        url = form.url.data
        finish = form.finish.data

        JsonFile().set_info(name, author, url, finish)

        flash('設定成功!!')

    data = Data(form, name, author, url, finish)

    return render_template('setting.html', data=data)

@app.route('/list_downloader', methods=['POST,', 'GET'])
def list_downloader():

    return  render_template('list_downloader.html', data=data)


if __name__ == '__main__':
    manager.run()
