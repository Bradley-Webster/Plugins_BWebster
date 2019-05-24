myProject = hiero.core.projects()[-1]



myProjectName = myProject.name()

myProjectPath = myProject.path()

myProjectDirectory = os.path.dirname(myProjectPath)



print myProjectDirectory

print '\nCurrent Directory:\n  ' + myProjectPath



newDirectory = myProjectDirectory + '/New_Folder_Path/' 

if not os.path.exists(newDirectory):

    os.makedirs(newDirectory)



copiedProject = newDirectory + myProjectName + '.hrox'

print '\nNew Project Directory path:\n  ' + copiedProject

myProject.saveAs(copiedProject)

