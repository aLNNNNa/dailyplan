from utils.task_data import load_tasks, save_tasks, create_task, delete_task, update_task

tasks = load_tasks("data/tasks.json")

new_task = {
    "name": "Python",
    "cycle": "weekly",
    "target": 3,
    "unit": "次"
}
create_task(tasks, new_task)
save_tasks(tasks, "data/tasks.json")
print(tasks)

updated_task = {"name": "Python进阶", "target": 5}
update_task(tasks, "task1", updated_task)
print(tasks)

new_task = {
    "name": "计算机组成原理",
    "cycle": "daily",
    "target": 1,
    "unit": "次"
}

create_task(tasks, new_task)

print(tasks)

delete_task(tasks, "task1")
save_tasks(tasks, "data/tasks.json")
print(tasks)