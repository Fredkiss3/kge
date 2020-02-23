
from kge import *
import time


class FrameCounter(Empty):
    # UPDATE FPS
    fps = 0
    dt = time.monotonic()
    n = 0
    total = 0

    # FIXED UPDATE FPS
    f_fps = 0
    f_dt = time.monotonic()
    f_n = 0
    f_t = 0

    # # RENDER UPDATE FPS
    # r_fps = 0
    # r_dt = 0
    # r_n = 0
    # r_t = 0

    def on_update(self, ev: events.Update, _):

        now = time.monotonic()
        if now - self.dt >= 1:
            self.n += 1
            self.total += self.fps
            print(f"UPDATE FPS : {self.fps}")
            print(f"AVERAGE UPDATE FPS : {self.total / self.n}\n")

            self.dt = time.monotonic()
            self.fps = 0

        self.fps += 1

    def on_fixed_update(self, ev: events.FixedUpdate, _):

        now = time.monotonic()
        if now - self.f_dt >= 1:
            self.f_n += 1
            self.f_t += self.f_fps
            print(f"FIXED UPDATE FPS : {self.f_fps}")
            print(f"AVERAGE FIXED UPDATE FPS : {self.f_t / self.f_n}\n")
            self.f_dt = time.monotonic()
            self.f_fps = 0

        self.f_fps += 1

    # def on_rendered(self, ev: events.Rendered, _):
    #
    #     now = time.monotonic()
    #     if now - self.r_dt >= 1:
    #         self.r_n += 1
    #         self.r_t += self.r_fps
    #         print(f"RENDER FPS : {self.r_fps}")
    #         print(f"AVERAGE RENDER FPS : {self.r_t / self.r_n}\n")
    #
    #         self.r_dt = time.monotonic()
    #         self.r_fps = 0
    #
    #     self.r_fps += 1
