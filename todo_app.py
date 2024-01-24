import sqlite3
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp
from datetime import datetime
import pandas as pd


conn = sqlite3.connect('tasks.sqlite', isolation_level=None)
c = conn.cursor()


class Task(BaseModel):
    name: str = ""
    description: str = ""
    state: str = ""
    category: str = ""
    created_at: datetime = datetime.now()
    created_by: str = ""

c.execute('''
          CREATE TABLE IF NOT EXISTS tasks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          description TEXT,
          state TEXT,
          category TEXT,
          created_at DATETIME,
          created_by TEXT
          )
          ''')
conn.commit()

def add_task(task: Task):
    c.execute('''
        INSERT INTO tasks (name, description, state, category, created_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?)''', 
        (task.name, task.description, task.state, task.category, task.created_at, task.created_by))
    conn.commit()

def get_tasks():
    c.execute('SELECT * FROM tasks')
    return c.fetchall()

def delete_task(task_id):
    c.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()


def main():
    st.title("Todo Task Manager")
    
    task_form = st.form(key='task_form')
    new_task = Task()
    new_task.name = task_form.text_input("Task Name")
    new_task.description = task_form.text_area("Task Description")
    new_task.state = task_form.selectbox("Task State", ['planned', 'in-progress', 'done'])
    new_task.category = task_form.selectbox("Task Category", ['school', 'work', 'personal'])
    new_task.created_at = datetime.now()
    new_task.created_by = task_form.text_input("Created By")

    if task_form.form_submit_button("Submit"):
        add_task(new_task)
        st.success("Task added successfully!")

    tasks = get_tasks()


    for task in tasks:
        task_id, name, description, state, category, created_at, created_by = task
        task_checkbox = st.checkbox(name, key=str(task_id))
        if task_checkbox:
            st.write(f"Task '{name}' marked as {state}")
        if st.button(f"Delete {name}"):
            delete_task(task_id)
    
    
    st.title("All Tasks")
    task_table_data = []
    #column_headers = ["Number", "Task ID", "Name", "Description", "State", "Category", "Created At", "Created By"]
    for task in tasks:
        task_id, name, description, state, category, created_at, created_by = task
        task_table_data.append([task_id, name, description, state, category, created_at, created_by])

    
    if task_table_data:
        st.table(task_table_data)
    else:
        st.write("No tasks available.")
    

main()
conn.close()
