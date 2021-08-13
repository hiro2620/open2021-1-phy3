from logging import getLogger, DEBUG
from typing import Iterable

from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class Animator(object):

    def __init__(self, wave_source_points=[(-1, 0), (1, 0)], **kwargs) -> None:
        """
        Parameters
        ----------
        fps: int, default 10
        time_duration : float, default 5
        grid_range : float, default 5
        grid_interval : float, default 0.1
        z_bottom : float, default -3
        wave_v : float, default 1
        wave_amp : float, default 0.2
        wave_init_lambda : float, default 0.5
        """
        self.fps = kwargs.pop("fps", 10)
        self.max_frames = kwargs.pop(
            "time_duration", 5) * self.fps
        logger.info(f"max_frames={self.max_frames}")

        self.current_frame = 0
        self.wave_source_points = wave_source_points
        assert len(wave_source_points) > 0

        self.grid_range = kwargs.pop("grid_range", 5)
        self.grid_interval = kwargs.pop("grid_interval", 0.1)
        self.z_bottom = kwargs.pop("z-bottom", -3)

        self.wave_v = kwargs.pop("wave_v", 1) / self.fps
        self.wave_amp = kwargs.pop("wave_amp", 0.2)
        self.wave_init_lambda = kwargs.pop("wave_init_lambda", 0.5)

        self.last_update_lambda_frame = 0

        self.__fig = plt.figure(figsize=(9.6, 7.2), dpi=100)
        self.__ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_box_aspect((3, 3, 2))
        self.__ax.set_zlim(self.z_bottom, (len(
            self.wave_source_points) + 1) * self.wave_amp)
        self.ani = animation.FuncAnimation(
            self.fig, self.__plot, fargs=(self.plot,), frames=self.time_keeper, interval=1000/self.fps, save_count=self.max_frames, blit=True)

    @property
    def fig(self) -> Figure:
        return self.__fig

    @property
    def ax(self) -> Axes3D:
        return self.__ax

    @property
    def wave_freq(self) -> float:
        return self.wave_v / self.wave_lambda

    @property
    def wave_lambda(self) -> float:
        return self.get_lambda()

    def time_keeper(self) -> Iterable:
        while self.max_frames >= self.current_frame:
            yield self.current_frame
            self.current_frame += 1

        logger.info(f"finishied")
        return

    def get_lambda(self) -> float:
        return self.wave_init_lambda

    @staticmethod
    def __plot(frame, *fargs) -> Figure:
        return fargs[0](frame),

    def plot(self, t) -> Figure:
        logger.info(f'frame={t}')
        logger.info(f'freq={self.wave_freq * self.fps}')

        gr = self.grid_range
        gi = self.grid_interval
        x, y = np.meshgrid(
            np.arange(-gr, gr, gi),
            np.arange(-gr, gr, gi)
        )
        z = np.sum([self.calc_z(x, y, t, ws_pos)
                   for ws_pos in self.wave_source_points], axis=0)

        self.ax.cla()
        self.__ax.set_zlim(self.z_bottom, (len(
            self.wave_source_points) + 1) * self.wave_amp)
        self.ax.plot_surface(x, y, z, alpha=1, rstride=1, cstride=1,
                             linewidth=0.3, cmap='hsv')
        self.ax.contour(x, y, z, zdir='z', offset=self.ax.get_zlim()[0])

        self.ax.set_title(f"lambda={self.wave_lambda}")

        return self.__fig

    def calc_z(self, x, y, t, ws_pos) -> float:
        f = self.wave_freq
        return self.wave_amp * np.sin(2 * np.pi * (-np.sqrt((x - ws_pos[0])**2 + (y - ws_pos[1])**2)/self.wave_lambda + f * t))

    def save(self, path="anim.mp4") -> None:
        self.ani.save(path, writer="ffmpeg", fps=self.fps)


if __name__ == "__main__":
    Animator().save()
