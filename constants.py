import os


def getCurrentDirectory():
    return os.getcwd()


def checkFolderExists(folder, path):
    return folder in os.listdir(path=path)


def createFolder(folder_name, path):
    os.mkdir(os.path.join(path, folder_name))

def checkFileExists(path, file):
    return file in os.listdir(path=path)

def createEmptyFile(path, file_name):
    with open(os.path.join(path, file_name), "w") as fp:
        pass