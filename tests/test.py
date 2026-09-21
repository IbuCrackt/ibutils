from time import sleep
import ibutils
a = 100

a /= 2
with open("./log_file.txt", "a") as filele:
    print(a, a, a, file=filele)

load_bar_window = ibutils.LoadBar(200, auto_time_estimation=True)
load_bar_window.set_progress(0)

sleep(2)
for i in range(1, 200):
    load_bar_window.add_progress()
    sleep(1)

load_bar_window.close()
