"""Blue Matrix package — sensor normalization bridge."""

from .matrix import BlueMatrix, SensorReading, MatrixSnapshot
from .channels import ChannelSpec, Modality, default_channel_registry
from .adapters import PneumaFrameAdapter, DictAdapter, StubHardwareAdapter
from .filters import MovingAverage, ExponentialSmoothing, SpikeReject, ChannelFilterPipeline

__all__ = [
    "BlueMatrix",
    "SensorReading",
    "MatrixSnapshot",
    "ChannelSpec",
    "Modality",
    "default_channel_registry",
    "PneumaFrameAdapter",
    "DictAdapter",
    "StubHardwareAdapter",
    "MovingAverage",
    "ExponentialSmoothing",
    "SpikeReject",
    "ChannelFilterPipeline",
]
