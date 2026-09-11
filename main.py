from utils.task_data import load_tasks,create_task,save_tasks,complete_task,update_task,delete_task,format_time,get_current_progress,get_task_status,get_overdue_status
from datetime import date

tasks = load_tasks("data/tasks.json")

while True:
    print("===========DailyPlan===========")
    print(date.today())
    print()
    print("今日任务：")
    print("-------------------------------")

    for task_id, task in tasks.items():
        count = get_current_progress(task)
        status = get_task_status(task)

        if status == "active":
            print(f"[ ] {task['name']:<20} {task['cycle']:<8} {count}/{task['target']}{task['unit']}")

    print("\n已完成")
    print("--------------------------------")

    for task_id, task in tasks.items():
        status = get_task_status(task)

        if status == "completed":
            print(task["name"])

    print("\n逾期任务：")
    print("--------------------------------")

    for task_id, task in tasks.items():
        status = get_task_status(task)
        count = get_current_progress(task)

        if status == "overdue":
            print(f"{task['name']:<20} {task['cycle']:<8} {count}/{task['target']}{task['unit']}")
            if get_overdue_status(task):
                save_tasks(tasks,"data/tasks.json")

    print("1. 完成任务")
    print("2. 查看任务详情")
    print("3. 修改任务")
    print("4. 删除任务")
    print("5. 添加任务")
    print("6. 退出")
    print("===============================")

    choice = input("请选择操作（1-6）：")

    if choice == "1":
        found = False
        name = input("请输入完成的任务名称：")
        for task_id,task in tasks.items():
            if task["name"] == name:
                found = True
                break
        if found:
            result = complete_task(tasks,task_id)
            if result:
                save_tasks(tasks,"data/tasks.json")
        else:
            print("任务不存在")

            
    elif choice == "2":
        name = input("请输入想要查询的任务名称：")
        found = False   

        for task_id, task in tasks.items():
            if task["name"] == name:
                print("\n========== 任务详情 ==========\n") 

                print(f"任务名称    ：{task['name']}")
                print(f"任务周期    ：{task['cycle']}")
                print(f"目标次数    ：{task['target']} {task['unit']}")
                print(f"提醒时间    ：{task['reminder']}")
                print(f"每日截止    ：{task['deadline']}")
                print(f"创建日期    ：{task['create_date']}")
                print(f"开始日期    ：{task['start_date']}")
                print(f"结束日期    ：{task['end_date']}")  

                if task["completion_history"]:
                    print(f"完成记录    ：{', '.join(task['completion_history'])}")
                else:
                    print("完成记录    ：暂无") 

                if task["overdue_history"]:
                    print("逾期记录    ：")
                    for overdue in task["overdue_history"]:
                        print(f"日期：{overdue["date"]},原因：{overdue["reason"]}")

                else:
                    print("逾期记录    ：暂无")

                if task["overdue_completion_history"]:
                    print(f"逾期完成记录：{', '.join(task['overdue_completion_history'])}")
                else:
                    print("逾期完成记录：暂无")

                print("\n==============================\n") 

                found = True
                break   

        if not found:
            print("任务不存在！")
        

    elif choice == "3":
        while True:
            name = input("请输入你要修改的任务名称：")

            found = False

            for task_id,task in tasks.items():
                if task["name"] == name:
                    t_id = task_id
                    found = True
                    break

            if found:
                print("1.修改任务名称")
                print("2.修改目标次数")
                print("3.修改提醒时间")
                print("4.修改每日截止时间")
                print("5.返回")

                update_choice = int(input("请选择要修改的内容："))

                match update_choice:
                    case 1:
                        new_name = input("请输入新的任务名称：")
                        updated_task = {
                            "name": new_name
                        }
                    case 2:
                        new_target = int(input("请输入新的目标次数："))
                        updated_task = {
                            "target": new_target
                        }
                    case 3:
                        new_reminder = input("请输入新的提醒时间：")
                        updated_task ={
                            "reminder":new_reminder
                        }
                    case 4:
                        new_deadline = input("请输入新的截止时间：")
                        updated_task = {
                            "deadline" : new_deadline
                        }
                    case 5:
                        break
                if update_task(tasks,t_id,updated_task) :
                    save_tasks(tasks,"data/tasks.json")
                    print("修改成功！")
            else:
                print("任务不存在！请重新输入")
                continue
            

    elif choice == "4":
        name = input("选择你要删除的任务：")
        found = False

        for task_id,task in tasks.items():
            if task["name"] == name:
                found = True
                break
        if found:
            if delete_task(tasks,task_id):
                save_tasks(tasks,"data/tasks.json")
        else:
            print("任务不存在，请重新输入")


    elif choice == "5":
        new_name = input("请输入任务名称：")
        new_cycle = input("请选择任务周期(daily/weekly/monthly):")
        if new_cycle == "daily":
            new_target = 1
        else:
            new_target = int(input("请输入目标次数："))
        new_reminder = format_time("请输入提醒时间：")
        new_deadline = format_time("请输入每日截止时间：")
        new_task = {
            "name" : new_name,
            "cycle" : new_cycle,
            "target" : new_target,
            "reminder" : new_reminder,
            "deadline" : new_deadline
        }
        if create_task(tasks,new_task):
            save_tasks(tasks,"data/tasks.json")
        else:
            print("创建错误")


    elif choice == "6":
        break
    else:
        print("无效操作，请重新选择！")
        continue
