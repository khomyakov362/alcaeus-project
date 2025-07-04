import os, stat


def handleRemoveReadonly(func, path, exc):
    """The functions rewrites readonly permissions on files.
        Witout it commands will not be able to delete .git files inside the book repo.
        Taken from the Stack Overflow answer https://stackoverflow.com/questions/2656322/shutil-rmtree-fails-on-windows-with-access-is-denied by Justin Peel."""


    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise
