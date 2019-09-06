from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import TaskForm
from .. import db
from ..models import Department
from forms import TaskForm, RoleForm
from ..models import Department, Role



from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required


from . import admin
from forms import TaskForm,RegistrationForm

from .. import db
from ..models import Task,Employee


def check_admin():
    """
    Prevent non-admins from getting  the page
    """
    if not current_user.is_admin:
        abort(403)





@admin.route('/task/add', methods=['GET', 'POST'])
@login_required
def add_task():
    """
    Add a task to the database
    """
    check_admin()

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
        return redirect(url_for('admin.list_task'))

    # load tasks template
    return render_template('admin/task/task.html', action="Add",
                           add_task=add_task, form=form,
                           title="Add Task")


@admin.route('/task/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_task(id):
    """
    Edit a task
    """
    check_admin()

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
        flash('You have successfully edited the department.')

        # redirect to the taskshowall page
        return redirect(url_for('admin.list_task'))

    form.description.data = task.description
    form.name.data = task.name
    form.status.data = task.status
    form.importance.data = task.importance
    form.towhom.data = task.towhom
    return render_template('admin/task/task.html', action="Edit",
                           add_task=add_task, form=form,
                                task=task, title="Edit Task")


@admin.route('/task/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    """
    Delete a task from the database
    """
    check_admin()
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    flash('You have successfully deleted the department.')

    # redirect to the taskshowall page
    return redirect(url_for('admin.list_task'))

@admin.route('/task/showall', methods=['GET','POST'])
@login_required
def list_task():

    check_admin()
    tasks = Task.query.all()
    return render_template('admin/task/task_showall.html',
                           tasks=tasks, title="Tasks")




@admin.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    """
    Add a employee by admin to the database
    """
    check_admin()

    add_employee = True

    form = RegistrationForm()
    if form.validate_on_submit():
        employees = Employee(email=form.email.data,
                                username=form.username.data,
                                password=form.password.data)


        try:
            # add department to the database
            db.session.add(employees)
            db.session.commit()
            flash('You have successfully added a new Employee.')
        except:
            # in case department name already exists
            flash('Error: department name already exists.')

        # redirect to departments page
        return redirect(url_for('admin.list_employee'))

    # load department template
    return render_template('admin/employee/employee.html', action="Add",
                           add_employee=add_employee, form=form,
                           title="Add Task")

@admin.route('/employee/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    """
    Edit a employee
    """
    check_admin()

    add_employee = False

    employee = Employee.query.get_or_404(id)
    form = RegistrationForm(obj=employee)
    if form.validate_on_submit():
        employee.email = form.email.data
        employee.username = form.username.data
        db.session.commit()
        flash('You have successfully edited the Employee.')

        # redirect to the departments page
        return redirect(url_for('admin.list_employee'))

    form.email.data = employee.email
    form.username.data = employee.username


    return render_template('admin/employee/employee.html', action="Edit",
                           add_employee=add_employee, form=form,
                                employee=employee, title="Edit Employee")


@admin.route('/employee/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee(id):
    """
    Delete a employee by admin from the database
    """
    check_admin()
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash('You have successfully deleted the Employee.')

    # redirect to the departments page
    return redirect(url_for('admin.list_employee'))


@admin.route('/employee/showall', methods=['GET','POST'])
@login_required
def list_employee():

    check_admin()
    employee = Employee.query.all()
    return render_template('admin/employee/employee_showall.html',
                           employee=employee, title="Employees")
# @admin.route('/tasks/')
# @login_required
# def tasks():
#     open_tasks = db.session.query(TaskForm).filter_by(status='1').order_by(TaskForm.due_date.asc())
#     closed_tasks = db.session.query(TaskForm).filter_by(status='0').order_by(TaskForm.due_date.asc())
#     return render_template('/tasks.html', form=AddTask(request.form),
#                            open_tasks=open_tasks, closed_tasks=closed_tasks)
#
#
# # Add new tasks:
# @mod.route('/add/', methods=['POST', 'GET'])
# @login_required
# def new_task():
#     form = AddTask(request.form)
#     if form.validate():
#         new_task = FTasks(
#             form.name.data,
#             form.due_date.data,
#             form.priority.data,
#             form.posted_date.data,
#             '1',
#             session['user_id']
#         )
#         db.session.add(new_task)
#         db.session.commit()
#         flash('New entry was successfully posted. Thanks.')
#     else:
#         flash_errors(form)
#     return redirect(url_for('.tasks'))
#
#
# # Mark tasks as complete:
# @mod.route('/complete/<int:task_id>/', )
# @login_required
# def complete(task_id):
#     new_id = task_id
#     db.session.query(TaskForm).filter_by(task_id=new_id).update({"status": "0"})
#     db.session.commit()
#     flash('The task was marked as complete. Nice.')
#     return redirect(url_for('.tasks'))
#
#
# # Delete Tasks:
# @admin.route('/delete/<int:task_id>/', )
# @login_required
# def delete_entry(task_id):
#     new_id = task_id
#     db.session.query(TaskForm).filter_by(task_id=new_id).delete()
#     db.session.commit()
#     flash('The task was deleted. Why not add a new one?')
#     return redirect(url_for('.tasks'))
#
#
# # Incomplete the closed tasks:
# @admin.route('/incomplete/<int:task_id>/', )
# @login_required
# def uncomplete(task_id):
#     new_id = task_id
#     db.session.query(TaskForm).filter_by(task_id=new_id).update({'status': '1'})
#     db.session.commit()
#     flash('The task was marked as incomplete.')
#     return redirect(url_for('.tasks'))



@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))

    return render_template(title="Delete Role")
