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