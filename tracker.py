import sys
import json
import os
FILENAME = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]


def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        return json.load(f)
    
def save_tasks(tasks):
    with open(FILENAME, "w") as f:
        json.dump(tasks, f)


def print_help():
    print("Usage: python task_tracker.py [command] [args]")
    print("Commands:")
    print("  add <description>          Add a new task (status defaults to todo)")
    print("  list [status]              List all tasks, optionally filtered by status")
    print("  update <id> <status>       Update a task's status")
    print("  delete <id>                Delete a task")
    print("  help                       Show this help message")
    print("")
    print("Valid statuses:")
    for status in VALID_STATUSES:
        print(f"  - {status}")


def main():
    if len(sys.argv) < 2:
        print_help()
        return
    command = sys.argv[1]
    tasks = load_tasks()

    if command == "help":
        print_help()
        return

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
        
        if filter_status and filter_status not in VALID_STATUSES:
            print(f"Error: Invalid status '{filter_status}'. Valid statuses are: {', '.join(VALID_STATUSES)}")
            return
        
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

        if new_status not in VALID_STATUSES:
            print(f"Error: Invalid status '{new_status}'. Valid statuses are: {', '.join(VALID_STATUSES)}")
            return
        
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                save_tasks(tasks)
                print(f"Task {task_id} updated to '{new_status}'")
                return
        print(f"Error: Task with ID {task_id} not found.")

    elif command in ["mark-in-progress", "mark-done"] and len(sys.argv) > 2:
        task_id = int(sys.argv[2])
        new_status = "in-progress" if command == "mark-in-progress" else "done"
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = new_status
                save_tasks(tasks)
                print(f"Task {task_id} marked as {new_status}")
                return

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
    else:
        print_help()

if __name__ == "__main__":
    main()
