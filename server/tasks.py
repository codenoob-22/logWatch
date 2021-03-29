from .consumers import broadcase_updates

def get_updates():
    tail = Tail('logfile.txt')
    tail.register_callback(broadcase_updates)