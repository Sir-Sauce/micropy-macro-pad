import time

#timer object for setting refresh rate
class Timer:
    def __init__(self) -> None:
        self.start_time = 0
        self.elapsed_time = 0
        self.is_running = False

    def start(self) -> None:
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            print("Timer started.")
        else:
            #restart instead if the timer is already running
            print("restarting timer")
            self.restart()

    def update(self):
        if self.is_running:
            current_time = time.time()
            self.elapsed_time += current_time - self.start_time
            return self.elapsed_time
            #self.start_time = current_time
            #print(f"Timer updated. Elapsed time: {self.elapsed_time} seconds.")

    def restart(self) -> None:
        self.elapsed_time = 0
        if self.is_running:
            self.start_time = time.time()
            #print("Timer restarted.")
        else:
            print("Timer not running. Start it using the 'start' method.")
