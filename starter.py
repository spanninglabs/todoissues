import taskbook_pb2
import sys
import os
import array
import re
import gitfiles
import glob
from github import Github

# create a todo task for a found todo comment
def CreateTask(todo, todoFoundList, lines, index, filename):

    # insert the title of the task at 'index' in the FoundList
    todo.title = todoFoundList[index]

    # add metadata to the todo item.
    todo.meta.lineNumber = str(lines[index])
    todo.meta.filename = filename
    print(str(lines[index]) + '\n')

# First, collect the found list of todos by scanning the file
def ScanFile(fl):
    curr_file = os.path.join(fl)
    #print(curr_file)
    outfile = open(curr_file, "r")
    datalines = outfile.readlines()
    outfile.close()

    outfileComplete = open(curr_file, "r")
    data = outfileComplete.read()
    outfile.close()

    # regexps for single and multi line comments
    regSingle = "//TODO.*"
    # TODO regMulti = "\/\*TODO(.|\s)*\*\/" 

    # collect task results
    findsSingle = re.findall(regSingle, data)
    #findsMulti = re.findall(regMulti, data)

    # TODO clean up the name of the ticket by removing TODO

    # collect the line locations of the correpsonding tickets
    count = 0
    idsSingle = []
    idsMulti = []
    print(len(datalines))

    for line in datalines:
        count+=1
        if (re.search("//TODO", line) is not None):
            idsSingle.append(count)
        if (re.search("/\\*TODO", line) is not None):
            idsMulti.append(count)

    # merge the separate lists of tickets and their line ids
    ticketNames = findsSingle # TODO removed findsMulti here
    ticketLines = idsSingle + idsMulti
    return ticketNames, ticketLines

# read in existing list of tasks
task_book = taskbook_pb2.TodoList()
try:
    f = open(sys.argv[1], "rb")
    task_book.ParseFromString(f.read())
    f.close()
except IOError:
    print(sys.argv[1] + ": Could not open file")

# now call ScanFile() to get the tasks and their lines
fileCollection = glob.glob('Files' + '/**/*.sol', recursive=True)
#print(fileCollection)
for i in range(len(fileCollection)):
    ticketNames, ticketLines = ScanFile(fileCollection[i])

    # add all found tasks in the file
    for j in range(len(ticketNames)):
        CreateTask(task_book.todos.add(), ticketNames, ticketLines, j, fileCollection[i])

# write to the task book after adding the all the tasks
f = open(sys.argv[1], "wb")
f.write(task_book.SerializeToString())
f.close()

#_______________________________________________________#
token = os.getenv('GITHUB_TOKEN', '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')
g = Github(token)
repo = g.get_repo("spanninglabs/spanning")

# iterates through the list of todos and creates issues on git
def createIssues(todo_list, repo): 
    count = 0
    for todo in todo_list.todos:
        todoTitle = todo.title
        todoLinenumber = todo.meta.lineNumber
        todoFilename = todo.meta.filename
        count+=1
        
        i = repo.create_issue(
        title=todoTitle,
        body="Linenumber: " + todoLinenumber + "--"
               + "Filename: " + todoFilename)
        
    print(count)
        

# open todolist and create issues
todo_list = taskbook_pb2.TodoList()
f = open(sys.argv[1], "rb")
todo_list.ParseFromString(f.read())
f.close()
print("we get here")
#print(len(todo_list))
createIssues(todo_list, repo)





        