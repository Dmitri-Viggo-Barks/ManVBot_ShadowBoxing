import time


class CustomTimer:
    def __init__ (self) -> None:
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = 0
        self.paused = False


    def pause(self) -> None:
        if not self.paused:
            self.pause_start = time.time()
            self.paused = True
    
    
    def resume(self) -> None:
        if self.paused:
            self.paused_time += (time.time() - self.pause_start)
            self.paused = False

    
    def elapsed(self) -> float:
        if self.paused:
            return (self.pause_start - self.start_time - self.paused_time)
        
        return (time.time() - self.start_time - self.paused_time)

    
    def reset(self) -> None:
        self.__init__()



if __name__ == "__main__":
    pass