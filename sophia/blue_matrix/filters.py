"""
Простые фильтры временного ряда для Голубой Матрицы.
"""

from __future__ import annotations
from typing import List, Deque
from collections import deque


class MovingAverage:
    """Скользящее среднее фиксированного окна."""

    def __init__(self, window: int = 5):
        if window < 1:
            raise ValueError("window must be >= 1")
        self.window = window
        self._buf: Deque[float] = deque(maxlen=window)

    def push(self, value: float) -> float:
        self._buf.append(value)
        return sum(self._buf) / len(self._buf)

    def reset(self) -> None:
        self._buf.clear()


class ExponentialSmoothing:
    """Экспоненциальное сглаживание."""

    def __init__(self, alpha: float = 0.3):
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0, 1]")
        self.alpha = alpha
        self._value: float | None = None

    def push(self, value: float) -> float:
        if self._value is None:
            self._value = value
        else:
            self._value = self.alpha * value + (1.0 - self.alpha) * self._value
        return self._value

    def reset(self) -> None:
        self._value = None


class SpikeReject:
    """Отбрасывает выбросы относительно последнего принятого значения."""

    def __init__(self, max_delta: float = 0.35):
        self.max_delta = max_delta
        self._last: float | None = None

    def push(self, value: float) -> float:
        if self._last is None:
            self._last = value
            return value
        if abs(value - self._last) > self.max_delta:
            return self._last  # reject spike
        self._last = value
        return value

    def reset(self) -> None:
        self._last = None


class ChannelFilterPipeline:
    """Конвейер: spike reject → EMA → (опционально) MA."""

    def __init__(self, use_ma: bool = False, ma_window: int = 5, ema_alpha: float = 0.3):
        self.spike = SpikeReject()
        self.ema = ExponentialSmoothing(alpha=ema_alpha)
        self.ma = MovingAverage(window=ma_window) if use_ma else None

    def process(self, value: float) -> float:
        v = self.spike.push(value)
        v = self.ema.push(v)
        if self.ma is not None:
            v = self.ma.push(v)
        return v

    def reset(self) -> None:
        self.spike.reset()
        self.ema.reset()
        if self.ma is not None:
            self.ma.reset()
