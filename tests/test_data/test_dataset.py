import pytest
import torch
from torch.utils.data import DataLoader
from pathlib import Path

from learn_former.data.dataset import get_dataloaders, get_dataset


def test_get_dataset(learn_former_root_dir: Path):

    dataset_dir = learn_former_root_dir / "data/datasets"

    dataset = get_dataset(storage_dir=dataset_dir, dataset_name="wmt16")

    assert "train" in dataset


def test_get_dataloaders(learn_former_root_dir: Path):

    dataset_dir = learn_former_root_dir / "data/datasets"
    dataset = get_dataset(storage_dir=dataset_dir, dataset_name="wmt16")

    dataloaders = get_dataloaders(dataset, batch_size=1, num_workers=0)
    train_loader, val_loader, test_loader = dataloaders

    x_train = next(iter(train_loader))
    x_val = next(iter(val_loader))
    x_test = next(iter(test_loader))

    x = x_train["de"]
    y = x_train["en"]

    assert isinstance(x, list)


def test_get_dataloaders_batch(learn_former_root_dir: Path):

    dataset_dir = learn_former_root_dir / "data/datasets"
    dataset = get_dataset(storage_dir=dataset_dir, dataset_name="wmt16")

    dataloaders = get_dataloaders(dataset, batch_size=1, num_workers=0)
    train_loader, val_loader, test_loader = dataloaders

    x_train = next(iter(train_loader))
    x_val = next(iter(val_loader))
    x_test = next(iter(test_loader))

    x = x_train["de"]
    y = x_train["en"]

    assert isinstance(x, list)


def test_dataloader_for_loop(learn_former_root_dir: Path):

    dataset_dir = learn_former_root_dir / "data/datasets"
    dataset = get_dataset(storage_dir=dataset_dir, dataset_name="wmt16")

    dataloaders = get_dataloaders(dataset, batch_size=1, num_workers=0)
    train_loader, val_loader, test_loader = dataloaders

    for batch in val_loader:
        x = batch["de"]
        y = batch["en"]

        assert isinstance(x, list)
        assert isinstance(y, list)

        break