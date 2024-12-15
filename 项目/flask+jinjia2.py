from flask import Flask, render_template, request, redirect

from models import todo #导入数据模型

app = Flask(__name__)

@app.route('/')
def hello_world():
    key = request.args.get('key', 'all')

    todo_list = []
    if key == 'undo':
        todo_list = todo.undo_list
    elif key == 'done':
        todo_list = todo.done_list
    elif key == 'all':
        todo_list = todo.todo_list

    return render_template('todo_jinja.html',
                           todo_list=todo_list,
                           key=key,
                           undo_count=len(todo.undo_list)) #渲染模板，传入参数

#添加待办事项
@app.route('/add_todo', methods=["POST"])
def add_todo():
    title = request.form.get('title', None)
    if title:
        todo.count += 1
        item = {
            'id': todo.count,
            'title': title,
            'done': False
        }
        todo.todo_list.append(item)
    return redirect('/')

#删除待办事项
@app.route('/del_todo')
def del_todo():
    todo_id = request.args.get('id', None)
    if todo_id and todo_id.isdigit():
        todo_id = int(todo_id)
        current_todo = list(filter(lambda item: item['id'] == todo_id, todo.todo_list))
        if current_todo[0] in todo.todo_list:
            todo.todo_list.remove(current_todo[0])
    return redirect('/')

#删除已完成
@app.route('/del_done')
def clear_done():
    for item in todo.done_list:
        todo.todo_list.remove(item)
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)