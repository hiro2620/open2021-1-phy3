from logging import getLogger, basicConfig, INFO
from itertools import product

from matplotlib.figure import Figure

from animator import Animator
from lambda_handler import LambdaHandler

basicConfig(level=INFO)
logger = getLogger(__name__)

mns = [(1, 0), (1, 1), (2, 0), (2, 1), (2, 2),
       (3, 0), (3, 1), (3, 2), (3, 3), (4, 1)]


class CustomAnimator(Animator):
    def __init__(self, wave_source_points, **kwargs) -> None:
        super().__init__(wave_source_points=wave_source_points, **kwargs)
        self.lambda_handler = LambdaHandler(
            self.fps * 2.5, self.fps * 1.1, mns=mns)
        self.lambda_desc = None

    def get_lambda(self) -> float:
        l = self.lambda_handler(self.current_frame)
        self.lambda_desc = self.lambda_handler.get_description()
        return l

    def plot(self, t) -> Figure:
        fig = super().plot(t)
        self.ax.set_title(
            f"λ={format(self.wave_lambda, '.3f')} {self.lambda_desc}")
        return fig


def main() -> None:
    wave_sources = [i for i in product(range(-1, 2), repeat=2)]
    assert len(wave_sources) == 9

    animator = CustomAnimator(wave_sources, fps=30,
                              time_duration=25, grid_range=6, wave_v=0.2)
    animator.save(path="anim.mp4")


if __name__ == "__main__":
    main()
