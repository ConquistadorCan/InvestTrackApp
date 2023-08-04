import os
def getDatabaseFiles():
    databaseFiles = []
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file.endswith('.db'):
                databaseFiles.append(os.path.join(root, file))
    return databaseFiles

databaseFiles = getDatabaseFiles()
print(databaseFiles)