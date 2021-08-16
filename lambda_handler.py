from logging import getLogger
import math
from functools import lru_cache

logger = getLogger(__name__)


@lru_cache(maxsize=None)
def la(m, n) -> float:
    return 1 / math.sqrt(m**2 + n**2)


class Transition:
    def __init__(self, start, stop, frame_duration) -> None:
        self.start = start
        self.stop = stop
        assert start != stop
        # increase -> True
        self.direction = self.start < self.stop

        self.duration = frame_duration
        self.delta_in_frame = (self.stop - self.start) / self.duration
        self.init_frame = None

        self.finished = False

    def __call__(self, frame) -> float:
        if self.finished:
            return self.stop

        if self.init_frame is None:
            self.init_frame = frame

        val = self.start + self.delta_in_frame * (frame - self.init_frame)
        if (self.stop > val) ^ self.direction:
            self.finished = True
            logger.info("finished transition")
            return self.stop
        else:
            return val


class LambdaHandler:
    def __init__(self, frame_duration, transit_frame_duration, base_lambda=1, mns=[(1, 0)]) -> None:
        self.duration = frame_duration
        self.transit_duration = transit_frame_duration
        self.base_lambda = base_lambda
        self.mns = mns
        assert len(self.mns) > 0
        self.current_mn = self.mns[0]
        self.last_update_frame = 0
        self.transition = None

        logger.info(f"duration={self.duration}")
        logger.info(f"transit_duration={self.transit_duration}")

    def get_description(self) -> str:
        if self.transition is not None and not self.transition.finished:
            return "in transition..."
        return f"(m,n)={self.current_mn}"

    def __call__(self, frame) -> float:
        if frame - self.last_update_frame > self.duration:
            c_i = self.mns.index(self.current_mn)
            if c_i == len(self.mns) - 1:
                logger.warning(f"reached last (m, n) {self.current_mn}")
            else:
                start = la(*self.current_mn)
                self.current_mn = self.mns[self.mns.index(self.current_mn) + 1]
                stop = la(*self.current_mn)
                self.transition = Transition(
                    start, stop, self.transit_duration)
                logger.info(f"lambda has been updated (m,n)={self.current_mn}")

            self.last_update_frame = frame

        if self.transition is None:
            return la(*self.current_mn)
        else:
            return self.transition(frame)
