import sys
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import Union

import tensorflow as tf
from loguru import logger

from . import ImageDataset

fmt = "[[{time:YYYY-MM-DD at HH:mm:ss}][elapsed: {elapsed}][{level}][{file}][{function}][{line}][{message}]]"
logger.remove()
logger.add(
    sink=sys.stdout,
    format=fmt,
    level="INFO",
    backtrace=True,
    diagnose=True,
    serialize=False,
)

PathOrStr = Union[Path, str]


class Dataloader:
    def __init__(
        self,
        batch_size: int,
        img_height: int,
        img_width: int,
        shuffle_buffer_size: int,
        gpu_count: int,
        num_parallel_calls: int,
        id: str = f"experiment-{str(datetime.now().strftime('ymd_%Y_%m_%d-hms_%H_%M_%S'))}",
        logger=logger,
    ) -> None:
        """
        Creates a data loader from an ImageDataset instance, creates random batches to train the model.
        """
        self.gpu_count = gpu_count
        self.num_parallel_calls = num_parallel_calls
        self.shuffle_buffer_size = shuffle_buffer_size
        self.batch_size = batch_size
        self.img_height = img_height
        self.img_width = img_width
        self.input_shape = (img_height, img_width, 3)
        self.logger = logger

    def __call__(self, *, dataset: ImageDataset, cache_path: PathOrStr) -> "Dataloader":
        """
        Converts the dataloader instance into a callable
        """
        self.dataset = dataset
        cache_path = Path(cache_path)
        self.cache_path = cache_path

        self.logger.info("##### Dataloader creation summary #####")
        self.logger.info(f"ImageDataset used: {self.dataset.id}")
        self.logger.info("#######################################")

        self.loader = (
            tf.data.Dataset.from_tensor_slices(
                list(zip(self.dataset.images, self.dataset.targets))
            )
            .map(
                partial(
                    self.dataset.read_image_wrapper,
                    img_height=self.img_height,
                    img_width=self.img_width,
                ),
                num_parallel_calls=self.num_parallel_calls,
            )
            .cache(self.cache_path.as_posix())
            .shuffle(buffer_size=self.shuffle_buffer_size)
            .repeat()
            .batch(self.batch_size * self.gpu_count)
            .prefetch(buffer_size=self.num_parallel_calls)
        )
        return self

    def __str__(self) -> str:
        return f"Dataloader for Dataset: {self.dataset}"
