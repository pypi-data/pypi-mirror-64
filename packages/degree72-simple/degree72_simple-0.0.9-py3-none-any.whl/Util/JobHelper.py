import os


def init_folder():  # init necessary folder
    if not os.path.exists('Log/'):
        os.mkdir('Log/')

    if not os.path.exists('Data/'):
        os.mkdir('Data/')

    if not os.path.exists('Records/'):
        os.mkdir('Records/')
