from flask import Flask, render_template, redirect, url_for, request
import os

from src.controller.actions.Action import Action, Output
from src.controller.actions.ListAction import ListAction
from src.controller.actions.CreateAction import CreateAction
from src.controller.actions.EditAction import EditAction
from src.controller.actions.UpdateAction import UpdateAction
from src.controller.actions.DeleteAction import DeleteAction
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
    action : Action = CreateAction()
    output : Output = action.exec(request)
    match output.status:
        case 1:
            output = redirect(url_for('list_feeds'))
        case -1:
            output = render_template('error/default.html')
    return output

@app.route('/edit/<id>')
def edit_feed(id):
    action : Action = EditAction()
    output : Output = action.exec(request)
    match output.status:
        case 1:
            output = render_template('feed/edit.html', **output.vars)
        case -1:
            output = render_template('error/default.html')
    return output

@app.route('/update', methods=['POST'])
def update_feed():
    action : Action = UpdateAction()
    output : Output = action.exec(request)
    match output.status:
        case 1:
            output = redirect(url_for('list_feeds'))
        case -1:
            output = render_template('error/default.html')
    return output

@app.route('/delete/<id>')
def delete_feed(id):
    action : Action = DeleteAction()
    output : Output = action.exec(request)
    match output.status:
        case 1:
            output = redirect(url_for('list_feeds'))
        case -1:
            output = render_template('error/default.html')
    return output

@app.route('/error')
def show_error():
    return render_template('error/default.html')

