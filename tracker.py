import sys
import json
import os
FILENAME = "tasks.json"

def  load_tasks():
    if os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python task_tracker.py [add|list|remove] [task]")
        return
    command = sys.argv[1]
    tasks = load_tasks()

    if command == "add" and len(sys.argv) > 2:
        new_task = {
            "id": len(tasks) + 1,
            "description": sys.argv[2],
            "status": "todo"
        }
        tasks.append(new_task)
        save_tasks(tasks)
        print(f"Task added successfully (ID: {new_task['id']})")
    
    elif command == "list":
        # Check if a specific status was requested (e.g., 'list done')
        filter_status = sys.argv[2] if len(sys.argv) > 2 else None
        
        filtered_tasks = tasks
        if filter_status:
            filtered_tasks = [t for t in tasks if t["status"] == filter_status]
        
        if not filtered_tasks:
            print(f"No tasks found with status: {filter_status if filter_status else 'any'}")
            return

        for task in filtered_tasks:
            print(f"[{task['id']}] {task['description']} ({task['status']})")
        

    elif command == "update" and len(sys.argv) > 3:
        # sys.argv[2] is the ID, sys.argv[3] is the new status (e.g., 'done')
        task_id = int(sys.argv[2])
        new_status = sys.argv[3]
        
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                save_tasks(tasks)
                print(f"Task {task_id} updated to '{new_status}'")
                return
        print(f"Error: Task with ID {task_id} not found.")

    elif command == "delete" and len(sys.argv) > 2:
        task_id = int(sys.argv[2])
        # This line keeps every task EXCEPT the one with the matching ID
        original_count = len(tasks)
        tasks = [t for t in tasks if t["id"] != task_id]
        
        if len(tasks) < original_count:
            save_tasks(tasks)
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task with ID {task_id} not found.")
if __name__ == "__main__":
    main()
