from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required


from . import manager
from forms import TaskForm

from .. import db
from ..models import Task


def check_manager():
    """
    Prevent non-manager from accessing the page
    """
    if not current_user.is_manager:
        abort(403)


# tasks to add edit delete Views

# @manager.route('/manager/dashboard')
# @login_required
# def manager_dashboard():
#     # prevent non-admins from accessing the page
#     if not current_user.is_manager:
#         abort(403)
#
#     return render_template('home/manager_dashboard.html', title="Dashboard")

@manager.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Add a task to the database
    """
    check_manager()

    add_task = True

    form = TaskForm()
    if form.validate_on_submit():
        task = Task(name=form.name.data,
                                description=form.description.data,status=form.status.data,importance=form.importance.data,towhom=form.towhom.data)
        try:
            # add task to the database
            db.session.add(task)
            db.session.commit()
            flash('You have successfully added a new Task.')
        except:
            # in case task name already exists
            flash('Error: task name already exists.')

        # redirect to tasks_showall page
        return redirect(url_for('manager.list_task'))

    # load tasks template
    return render_template('manager/task/task.html', action="Add",
                           add_task=add_task, form=form,
                           title="Add Task")


@manager.route('/task/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a task
    """
    check_manager()

    add_task = False

    task = Task.query.get_or_404(id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.name = form.name.data
        task.description = form.description.data
        task.status = form.status.data
        task.importance = form.importance.data
        task.towhom = form.towhom.data
        db.session.commit()
        flash('You have successfully edited the task.')

        # redirect to the taskshowall page
        return redirect(url_for('manager.list_task'))

    form.description.data = task.description
    form.name.data = task.name
    form.status.data = task.status
    form.importance.data = task.importance
    form.towhom.data = task.towhom
    return render_template('manager/task/task.html', action="Edit",
                           add_task=add_task, form=form,
                                task=task, title="Edit Task")

@manager.route('/task/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a task from the database
    """
    check_manager()
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the task')

    # redirect to the taskshowall page
    return redirect(url_for('manager.list_task'))

@manager.route('/task/showall', methods=['GET','POST'])
@login_required
def list_task():

    check_manager()
    tasks = Task.query.all()
    return render_template('manager/task/task_showall.html',
                           tasks=tasks, title="Task List")

# @manager.route('/database/add', methods=['GET', 'POST'])
# @login_required
# def add_task():
#     """
#     Add a tasks to the database
#     """
#     check_manager()
#
#     add_task = True
#
#     form = TaskForm()
#     if form.validate_on_submit():
#         task = Task(name=form.name.data,
#                                 description=form.description.data,status=form.status.data,importance=form.importance.data,towhom=form.towhom.data)
#         try:
#             # add task to the database
#             db.session.add(task)
#             db.session.commit()
#             flash('You have successfully added a new Task.')
#         except:
#             # in case task name already exists
#             flash('Error: Task name already exists.')
#
#         # redirect to taskshowall page
#         return redirect(url_for('manager.list_task'))
#
#     # load task template
#     return render_template('manager/task/task.html', action="Add",
#                            add_task=add_task, form=form,
#                            title="Add Task")
#
#
# @manager.route('/database/edit/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_task(id):
#     """
#     Edit a task
#     """
#     check_manager()
#
#     add_task = False
#
#     task = Task.query.get_or_404(id)
#     form = TaskForm(obj=task)
#     if form.validate_on_submit():
#         task.name = form.name.data
#         task.description = form.description.data
#         task.status = form.status.data
#         task.importance = form.importance.data
#         task.towhom = form.towhom.data
#         db.session.commit()
#         flash('You have successfully edited the department.')
#
#         # redirect to the taskshowall page
#         return redirect(url_for('manager.list_task'))
#
#     form.description.data = task.description
#     form.name.data = task.name
#     form.status.data = task.status
#     form.importance.data = task.importance
#     form.towhom.data = task.towhom
#     return render_template('manager/task/task.html', action="Edit",
#                            add_task=add_task, form=form,
#                                 task=task, title="Edit Task")
#
#
# @manager.route('/database/delete/<int:id>', methods=['GET', 'POST'])
# @login_required
# def delete_task(id):
#     """
#     Delete a tasks from the database
#     """
#     check_manager()
#     task = Task.query.get_or_404(id)
#     db.session.delete(task)
#     db.session.commit()
#     flash('You have successfully deleted the department.')
#
#     # redirect to the taskshowall page
#     return redirect(url_for('manager.list_task'))
#
# @manager.route('/database/showall', methods=['GET','POST'])
# @login_required
# def list_task():
#
#     check_manager()
#     tasks = Task.query.all()
#     return render_template('manager/task/task_showall.html',
#                            tasks=tasks, title="Tasks")
