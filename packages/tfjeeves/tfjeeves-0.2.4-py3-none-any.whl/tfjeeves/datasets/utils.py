from pathlib import Path
from typing import Union

import pandas as pd
import tensorflow as tf

PathOrStr = Union[Path, str]


@tf.function
def read_image(*, filepath: str, img_width: int, img_height: int) -> tf.Tensor:
    """
    """
    img = tf.io.read_file(filepath)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, (img_width, img_height))
    return img


def validate_folder(*, folderpath: PathOrStr) -> Path:
    """
    """
    if Path(folderpath).exists():
        print(f"{folderpath} exists!")
        return Path(folderpath)
    else:
        raise ValueError(f"folderpath: {str(folderpath)} doesn't exist!")


def disk2df(source: PathOrStr, target: PathOrStr = "output.csv") -> None:
    """
    """
    source = validate_folder(folderpath=source)
    # labels_all = [path.parts[-1] for path in list(source.glob('*'))]

    imgs_n_labels = [
        (path.resolve().as_posix(), path.parts[-2]) for path in list(source.glob("*/*"))
    ]
    imgs_n_labels = (
        pd.DataFrame(imgs_n_labels, columns=["img", "label"])
        .sample(frac=1)
        .reset_index(drop=True)
    )
    imgs_n_labels.to_csv(target, sep=",", header=True, index=False)


def disk2df_cifar100_superclass(source: PathOrStr, target: PathOrStr):
    """
    """
    source = validate_folder(folderpath=source)
    imgs_n_labels = [
        (path.resolve().as_posix(), path.parts[-3])
        for path in list(source.glob("*/*/*"))
    ]
    imgs_n_labels = (
        pd.DataFrame(imgs_n_labels, columns=["img", "label"])
        .sample(frac=1)
        .reset_index(drop=True)
    )
    imgs_n_labels.to_csv(target, sep=",", header=True, index=False)


# if __name__=="__main__":
# disk2df_cifar100_superclass("../../assets/cifar100superclass/train", "cifar100superclass_train.csv")
# disk2df_cifar100_superclass("../../assets/cifar100superclass/test", "cifar100superclass_test.csv")

# disk2df("../../assets/cifar10/train", "cifar10_train.csv")
# disk2df("../../assets/cifar10/val", "cifar10_val.csv")
# disk2df("../../assets/cifar10/test", "cifar10_test.csv")

# disk2df("../../assets/cifar100/train", "cifar100_train.csv")
# disk2df("../../assets/cifar100/val", "cifar100_val.csv")
# disk2df("../../assets/cifar100/test", "cifar100_test.csv")

# disk2df("../../assets/shop5/train", "shop5_train.csv")
# disk2df("../../assets/shop5/val", "shop5_val.csv")
# disk2df("../../assets/shop5/test", "shop5_test.csv")


@tf.function
def read_image_wrapper_df(self, payload):
    """
    """
    return (
        read_image(
            filepath=payload[0], IMG_WIDTH=self.IMG_WIDTH, IMG_HEIGHT=self.IMG_HEIGHT
        ),
        tf.map_fn(
            fn=tf.strings.to_number,
            elems=tf.strings.split(payload[1], "-"),
            dtype=tf.float32,
        ),
    )
