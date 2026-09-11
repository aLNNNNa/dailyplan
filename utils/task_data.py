import json,os
from datetime import date,timedelta

def load_tasks(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump({}, file)
        return {}
    else:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                tasks = json.load(file)
            return tasks
        except json.JSONDecodeError:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump({}, file)
            return {}

def save_tasks(tasks, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(tasks, file)
    return True

def create_task(tasks, new_task):
    #检查任务名称是否重复
    for key_name in tasks:

        if tasks[key_name]["name"] == new_task["name"]:
            print("任务已存在，不可创建")
            return False

    today = date.today()
    if new_task["cycle"] == "daily":
        end_date = today
    elif new_task["cycle"] == "weekly":
        end_date = today + timedelta(days=6)
    elif new_task["cycle"] == "monthly":
        end_date = today + timedelta(days=29)
    else:
        print("日期出错")
        return False

    new_task["unit"] = "次"
    new_task["create_date"] = str(today)
    new_task["start_date"] = str(today)
    new_task["end_date"] = str(end_date)
    new_task["completion_history"] = []
    new_task["overdue_history"] = []
    new_task["overdue_completion_history"] = []

    #全部循环检查完毕后再创建
    task_id = f"task{len(tasks) + 1}"
    tasks[task_id] = new_task
    print("创建成功！")
    return True



def delete_task(tasks, task_id):
    if task_id in tasks:
        del tasks[task_id]

        new_id = 1
        new_tasks = {}

        for task_id, task in tasks.items():
            new_task_id = f"task{new_id}"
            new_tasks[new_task_id] = task
            new_id += 1
        tasks.clear()
        tasks.update(new_tasks)
        print("删除成功！")

        return True
    else:
        return False

def update_task(tasks, task_id, updated_task):
    if task_id in tasks:
        for key, value in updated_task.items():
            match key:
                case "name" | "target" | "reminder" | "deadline":
                    tasks[task_id][key] = value
                case _:
                    continue
        return True
    else:
        return False

def complete_task(tasks,task_id):
 
    if task_id in tasks:
        task = tasks[task_id]
        today = str(date.today())
        status = get_task_status(task)

        if status == "active":
            task["completion_history"].append(today)
            print("恭喜你，成功打卡")
            return True
        elif status == "overdue":
            task["overdue_completion_history"].append(today)
            print("下次一定要按时完成呦~")
            return True
        elif status == "completed":
            print("这项任务已经完成了，无需再次操作。")
            return False

    else:
        print("任务不存在，请检查后重新输入！")
        return False

def format_time(prompt):
            
    def validate_hour(hour):
        return 0 <= hour <= 23

    def validate_minute(minute):
        return 0 <= minute <= 59

    while True:
        time = input(prompt)
        time = time.replace("：",":")

        try:
            if ":" not in time:
                time = f"{int(time):02d}:00"
            hour,minute = time.split(":")
            hour = int(hour)
            minute = int(minute)
            if validate_hour(hour) and validate_minute(minute):
                break
            else:
                print("数字不符合范围，重新输入！")
                continue
        except ValueError:
            print("请输入数字！")
            continue
            
    time = f"{hour:02d}:{minute:02d}"
    return time

def get_current_progress(task):
    start_date = date.fromisoformat(task["start_date"])
    end_date = date.fromisoformat(task["end_date"])
    count = 0

    #正常完成
    for completed in task["completion_history"]:
        completion_date = date.fromisoformat(completed)
        if start_date <= completion_date <= end_date:
            count += 1

    #逾期完成
    for overdue in task["overdue_completion_history"]:
        overdue_completion_date = date.fromisoformat(overdue)
        if overdue_completion_date > end_date:
            count += 1

    return count


def get_overdue_status(task):
    status = get_task_status(task)

    if status != "overdue":
        return False
    
    today = str(date.today())

    for overdue in task["overdue_history"]:
        if overdue["date"] == today:
            return False
        
    reason = input(f"请输入{task['name']}本次逾期原因：")
    
    task["overdue_history"].append({
        "date":today,
        "reason":reason
    })
    return True




def get_task_status(task):
    today = date.today()
    end_date = date.fromisoformat(task["end_date"])

    count = get_current_progress(task)
    target = task["target"]

    if count >= target:
        return "completed"
    
    elif today > end_date:
        return "overdue"
    
    else:
        return "active"

    