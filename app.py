from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime

app = Flask(__name__)

# In-Memory Storage (Simple list to store tasks)
tasks = []
next_id = 1

# Helper function to find task by ID
def find_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            return task
    return None

# Routes
@app.route('/')
def index():
    # Sort tasks by created_at in descending order (newest first)
    sorted_tasks = sorted(tasks, key=lambda x: x['created_at'], reverse=True)
    return render_template('index.html', tasks=sorted_tasks)

# CREATE - Add new task
@app.route('/add', methods=['POST'])
def add_task():
    global next_id
    
    title = request.form.get('title')
    description = request.form.get('description', '')
    
    if title:
        new_task = {
            'id': next_id,
            'title': title,
            'description': description,
            'completed': False,
            'created_at': datetime.utcnow()
        }
        tasks.append(new_task)
        next_id += 1
    
    return redirect(url_for('index'))

# READ - Get all tasks (API)
@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'completed': task['completed'],
            'created_at': task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(task_list)

# READ - Get single task (API)
@app.route('/api/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = find_task(id)
    if task:
        return jsonify({
            'id': task['id'],
            'title': task['title'],
            'description': task['description'],
            'completed': task['completed'],
            'created_at': task['created_at'].strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'error': 'Task not found'}), 404

# UPDATE - Toggle task completion
@app.route('/toggle/<int:id>')
def toggle_task(id):
    task = find_task(id)
    if task:
        task['completed'] = not task['completed']
    return redirect(url_for('index'))

# DELETE - Delete task
@app.route('/delete/<int:id>')
def delete_task(id):
    task = find_task(id)
    if task:
        tasks.remove(task)
    return redirect(url_for('index'))

# Health check endpoint (useful for deployment)
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'tasks_count': len(tasks),
        'version': '1.1',
        'environment': 'production',
        'message': 'Task Manager API is running'
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
