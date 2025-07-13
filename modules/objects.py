class Task(): 
    def __init__(self, name: str, duedate: str, importance: bool = False):
        self.name = name
        self.duedate = duedate
        
class AllTasks(): 
    def __init__(self):
        self.tasks: list[Task] = []
    
    def addTask(self, task: Task):
        self.tasks.append(task)

    def printTasks(self):
        for item in self.tasks:
            print(f"{item.name:-<40} {item.duedate:-<10}")
