from flask import Flask, render_template, redirect, url_for, request
import os

from src.controller.actions.Action import Action, Output
from src.controller.actions.ListAction import ListAction
from src.model.feed.facade.FeedFacade import FeedFacade, FeedDTO

template_folder_path = os.path.abspath('./src/view')
app = Flask(__name__, template_folder=template_folder_path)

# Ruta para la página de lista
@app.route('/')
def index():
    return redirect(url_for('list_feeds'))

@app.route('/list')
def list_feeds():
    action : Action = ListAction()
    output : Output = action.exec(request)
    match output.status:
        case 1:
            output = render_template('feed/list.html', **output.vars)
        case -1:
            output = render_template('error/default.html')
    return output

@app.route('/add')
def add_feed():
    return render_template('feed/add.html')

@app.route('/create', methods=['POST'])
def create_feed():
    name = request.form.get('name')
    url = request.form.get('url')
    FeedFacade().create_feed(FeedDTO(0, name, url))
    return redirect(url_for('list_feeds'))

@app.route('/edit/<id>')
def edit_feed(id):
    feed = FeedFacade().get_feed(id)
    return render_template('feed/edit.html', feed=feed)

@app.route('/update', methods=['POST'])
def update_feed():
    id = request.form.get('id')   
    name = request.form.get('name')
    url = request.form.get('url')
    FeedFacade().update_feed(FeedDTO(id, name, url))
    return redirect(url_for('list_feeds'))

@app.route('/delete/<id>')
def del_feed(id):
    FeedFacade().delete_feed(id)
    return redirect(url_for('list_feeds'))

@app.route('/error')
def show_error():
    return render_template('error/default.html')

