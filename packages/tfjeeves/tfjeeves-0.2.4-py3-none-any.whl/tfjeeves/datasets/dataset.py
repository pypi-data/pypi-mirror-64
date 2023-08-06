import random
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd
import tensorflow as tf
from loguru import logger

PathOrStr = Union[Path, str]
StrList = Sequence[str]

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


class Dataset(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __len__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError


class ImageDataset(Dataset):
    def __init__(
        self,
        id: str = f"experiment-{str(datetime.now().strftime('ymd_%Y_%m_%d-hms_%H_%M_%S'))}",
        logger=logger,
    ):
        """
        This class exposes several methods to create a dataset from raw input data.
        """
        self.id = id
        self.logger = logger

    def __len__(self) -> int:
        return self.length

    def __str__(self) -> str:
        return f"ImageDataset @ {self.path.as_posix()}"

    @tf.function
    def read_image(
        self, *, filepath: PathOrStr, img_width: int, img_height: int
    ) -> tf.Tensor:
        """
        Reads image file from a path, resizes it and returns a tensor
        """
        img = tf.io.read_file(filepath)
        img = tf.image.decode_jpeg(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)  # puts data in [0, 1) range
        img = tf.image.resize(img, (img_width, img_height))
        return img

    def from_folder(
        self, path: PathOrStr = ".", extensions: StrList = None
    ) -> "ImageDataset":
        """Create an `ImageDataset` using images in `path` with correct `extensions`
        """
        path = Path(path)
        if path.is_dir() and path.exists():
            self.path = path
            imgs_n_labels = [
                (path.as_posix(), path.parts[-2]) for path in list(path.glob("*/*"))
            ]
            random.shuffle(imgs_n_labels)
            self.images, self.targets = zip(*imgs_n_labels)
            self.length = len(imgs_n_labels)
            self.CLASS_NAMES = sorted(np.unique([item.name for item in path.glob("*")]))
            self.class_map = tf.lookup.StaticHashTable(
                initializer=tf.lookup.KeyValueTensorInitializer(
                    keys=tf.constant(self.CLASS_NAMES),
                    values=tf.constant(list(range(len(self.CLASS_NAMES)))),
                ),
                default_value=tf.constant(-1),
                name="class_weight",
            )
            self.n_classes = len(self.CLASS_NAMES)
            self.logger.info("########## ImageDataset update status ##########")
            self.logger.info(
                f"ImageDataset {self.id} updated from_folder {str(self.path)}"
            )
            self.logger.info(f"Length of updated ImageDataset: {self.length}")
            self.logger.info(f"No of classes in updated ImageDataset: {self.n_classes}")
            self.logger.info(f"Class names in updated ImageDataset: {self.CLASS_NAMES}")
            self.logger.info("#################################################")
            return self
        else:
            raise ValueError(f"{path} is not a valid directory.")
        return self

    def from_csv(
        self, path: PathOrStr = ".", extensions: StrList = None
    ) -> "ImageDataset":
        """
        Create an `ImageDataset` using images in the csv with correct `extensions`
        """
        path = Path(path)
        if path.exists():
            self.path = path
            df = pd.read_csv(path)
            try:
                # random.shuffle(imgs_n_labels) ?
                self.images = df["img"].to_list()
                self.targets = df["label"].to_list()
                self.CLASS_NAMES = np.sort(np.array(list(df["label"].unique())))
                self.length = len(self.images)
                self.n_classes = len(self.CLASS_NAMES)
                self.logger.info("########## ImageDataset update status ##########")
                self.logger.info(
                    f"ImageDataset {self.id} updated from_csv {str(self.path)}"
                )
                self.logger.info(f"Length of updated ImageDataset: {self.length}")
                self.logger.info(
                    f"No of classes in updated ImageDataset: {self.n_classes}"
                )
                self.logger.info(
                    f"Class names in updated ImageDataset: {self.CLASS_NAMES}"
                )
                self.logger.info("#################################################")
                return self
            except:
                raise ValueError(
                    f"The csv has incorrect format (expecting `img` and `label` columns)"
                )
                # Change to col0:img, col1:label?
        else:
            raise ValueError(f"{path} does not exist!")

    def show_batch(self) -> "ImageDataset":
        return self

    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, np.array]:
        """
        Reads in the payload of image file and label, and returns image and label data suitable for training
        """
        return (
            self.read_image(
                filepath=payload[0], img_width=img_width, img_height=img_height,
            ),
            payload[1] == np.array(self.CLASS_NAMES),
        )


class ImageDatasetRegression(ImageDataset):
    def from_df(self, df: pd.DataFrame) -> "ImageDatasetRegression":
        try:
            self.images = df["path"].tolist()
            self.targets = df["target"].tolist()
            self.n_targets = len(df["target"].iloc[0].split("-"))
            self.length = len(self.images)
            self.logger.info(f"########## ImageDataset update status ##########")
            self.logger.info(f"Length of updated ImageDataset: {self.length}")
            self.logger.info(f"No of targets in updated ImageDataset: {self.n_targets}")
            self.logger.info("#################################################")
            return self
        except KeyError:
            logger.exception(
                f"Input dataFrame should contain both image `path` and `target` columns"
            )

    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, np.array]:
        return (
            self.read_image(
                filepath=payload[0], img_width=img_width, img_height=img_height
            ),
            tf.map_fn(
                fn=tf.strings.to_number,
                elems=tf.strings.split(payload[1], "-"),
                dtype=tf.float32,
            ),
        )


class ImageDatasetTriplet(ImageDataset):
    @tf.function
    def read_image_wrapper(
        self, payload: Tuple[str, str], img_width: int, img_height: int
    ) -> Tuple[tf.Tensor, tf.Tensor]:
        """
        Reads in the payload of image file and label, and returns image and label data suitable for training
        """
        return (
            self.read_image(
                filepath=payload[0], img_width=img_width, img_height=img_height,
            ),
            self.class_map.lookup(payload[1]),
        )
