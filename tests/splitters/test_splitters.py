# -*- coding: utf-8 -*-
"""Test splitters."""
from collections import Counter
from random import shuffle

import numpy as np
import pytest

from mofdscribe.datasets.core_dataset import CoREDataset
from mofdscribe.splitters.splitters import (
    LOCOCV,
    BaseSplitter,
    ClusterSplitter,
    ClusterStratifiedSplitter,
    DensitySplitter,
    HashSplitter,
    KennardStoneSplitter,
    TimeSplitter,
)

FEATURES = [
    "total_POV_gravimetric",
    "mc_CRY-chi-0-all",
    "mc_CRY-chi-1-all",
    "mc_CRY-chi-2-all",
    "mc_CRY-chi-3-all",
    "mc_CRY-Z-0-all",
    "mc_CRY-Z-1-all",
    "mc_CRY-Z-2-all",
    "mc_CRY-Z-3-all",
    "mc_CRY-I-0-all",
    "mc_CRY-I-1-all",
    "mc_CRY-I-2-all",
    "mc_CRY-I-3-all",
    "mc_CRY-T-0-all",
    "mc_CRY-T-1-all",
    "mc_CRY-T-2-all",
    "mc_CRY-T-3-all",
    "mc_CRY-S-0-all",
    "mc_CRY-S-1-all",
    "mc_CRY-S-2-all",
    "mc_CRY-S-3-all",
    "D_mc_CRY-chi-0-all",
    "D_mc_CRY-chi-1-all",
    "D_mc_CRY-chi-2-all",
    "D_mc_CRY-chi-3-all",
    "D_mc_CRY-Z-0-all",
    "D_mc_CRY-Z-1-all",
    "D_mc_CRY-Z-2-all",
    "D_mc_CRY-Z-3-all",
    "D_mc_CRY-I-0-all",
    "D_mc_CRY-I-1-all",
    "D_mc_CRY-I-2-all",
    "D_mc_CRY-I-3-all",
    "D_mc_CRY-T-0-all",
    "D_mc_CRY-T-1-all",
    "D_mc_CRY-T-2-all",
    "D_mc_CRY-T-3-all",
    "D_mc_CRY-S-0-all",
    "D_mc_CRY-S-1-all",
    "D_mc_CRY-S-2-all",
    "D_mc_CRY-S-3-all",
    "sum-mc_CRY-chi-0-all",
    "sum-mc_CRY-chi-1-all",
    "sum-mc_CRY-chi-2-all",
    "sum-mc_CRY-chi-3-all",
    "sum-mc_CRY-Z-0-all",
    "sum-mc_CRY-Z-1-all",
    "sum-mc_CRY-Z-2-all",
    "sum-mc_CRY-Z-3-all",
    "sum-mc_CRY-I-0-all",
    "sum-mc_CRY-I-1-all",
    "sum-mc_CRY-I-2-all",
    "sum-mc_CRY-I-3-all",
    "sum-mc_CRY-T-0-all",
    "sum-mc_CRY-T-1-all",
    "sum-mc_CRY-T-2-all",
    "sum-mc_CRY-T-3-all",
    "sum-mc_CRY-S-0-all",
    "sum-mc_CRY-S-1-all",
    "sum-mc_CRY-S-2-all",
    "sum-mc_CRY-S-3-all",
    "sum-D_mc_CRY-chi-0-all",
    "sum-D_mc_CRY-chi-1-all",
    "sum-D_mc_CRY-chi-2-all",
    "sum-D_mc_CRY-chi-3-all",
    "sum-D_mc_CRY-Z-0-all",
    "sum-D_mc_CRY-Z-1-all",
    "sum-D_mc_CRY-Z-2-all",
    "sum-D_mc_CRY-Z-3-all",
    "sum-D_mc_CRY-I-0-all",
    "sum-D_mc_CRY-I-1-all",
    "sum-D_mc_CRY-I-2-all",
    "sum-D_mc_CRY-I-3-all",
    "sum-D_mc_CRY-T-0-all",
    "sum-D_mc_CRY-T-1-all",
    "sum-D_mc_CRY-T-2-all",
    "sum-D_mc_CRY-T-3-all",
    "sum-D_mc_CRY-S-0-all",
    "sum-D_mc_CRY-S-1-all",
    "sum-D_mc_CRY-S-2-all",
    "sum-D_mc_CRY-S-3-all",
    "D_lc-chi-0-all",
    "D_lc-chi-1-all",
    "D_lc-chi-2-all",
    "D_lc-chi-3-all",
    "D_lc-Z-0-all",
    "D_lc-Z-1-all",
    "D_lc-Z-2-all",
    "D_lc-Z-3-all",
    "D_lc-I-0-all",
    "D_lc-I-1-all",
    "D_lc-I-2-all",
    "D_lc-I-3-all",
    "D_lc-T-0-all",
    "D_lc-T-1-all",
    "D_lc-T-2-all",
    "D_lc-T-3-all",
    "D_lc-S-0-all",
    "D_lc-S-1-all",
    "D_lc-S-2-all",
    "D_lc-S-3-all",
    "D_lc-alpha-0-all",
    "D_lc-alpha-1-all",
    "D_lc-alpha-2-all",
    "D_lc-alpha-3-all",
    "D_func-chi-0-all",
    "D_func-chi-1-all",
    "D_func-chi-2-all",
    "D_func-chi-3-all",
    "D_func-Z-0-all",
    "D_func-Z-1-all",
    "D_func-Z-2-all",
    "D_func-Z-3-all",
    "D_func-I-0-all",
    "D_func-I-1-all",
    "D_func-I-2-all",
    "D_func-I-3-all",
    "D_func-T-0-all",
    "D_func-T-1-all",
    "D_func-T-2-all",
    "D_func-T-3-all",
    "D_func-S-0-all",
    "D_func-S-1-all",
    "D_func-S-2-all",
    "D_func-S-3-all",
    "D_func-alpha-0-all",
    "D_func-alpha-1-all",
    "D_func-alpha-2-all",
    "D_func-alpha-3-all",
    "sum-D_lc-chi-0-all",
    "sum-D_lc-chi-1-all",
    "sum-D_lc-chi-2-all",
    "sum-D_lc-chi-3-all",
    "sum-D_lc-Z-0-all",
    "sum-D_lc-Z-1-all",
    "sum-D_lc-Z-2-all",
    "sum-D_lc-Z-3-all",
    "sum-D_lc-I-0-all",
    "sum-D_lc-I-1-all",
    "sum-D_lc-I-2-all",
    "sum-D_lc-I-3-all",
    "sum-D_lc-T-0-all",
    "sum-D_lc-T-1-all",
    "sum-D_lc-T-2-all",
    "sum-D_lc-T-3-all",
    "sum-D_lc-S-0-all",
    "sum-D_lc-S-1-all",
    "sum-D_lc-S-2-all",
    "sum-D_lc-S-3-all",
    "sum-D_lc-alpha-0-all",
    "sum-D_lc-alpha-1-all",
    "sum-D_lc-alpha-2-all",
    "sum-D_lc-alpha-3-all",
    "sum-D_func-chi-0-all",
    "sum-D_func-chi-1-all",
    "sum-D_func-chi-2-all",
    "sum-D_func-chi-3-all",
    "sum-D_func-Z-0-all",
    "sum-D_func-Z-1-all",
    "sum-D_func-Z-2-all",
    "sum-D_func-Z-3-all",
    "sum-D_func-I-0-all",
    "sum-D_func-I-1-all",
    "sum-D_func-I-2-all",
    "sum-D_func-I-3-all",
    "sum-D_func-T-0-all",
    "sum-D_func-T-1-all",
    "sum-D_func-T-2-all",
    "sum-D_func-T-3-all",
    "sum-D_func-S-0-all",
    "sum-D_func-S-1-all",
    "sum-D_func-S-2-all",
    "sum-D_func-S-3-all",
    "sum-D_func-alpha-0-all",
    "sum-D_func-alpha-1-all",
    "sum-D_func-alpha-2-all",
    "sum-D_func-alpha-3-all",
]


@pytest.mark.parametrize("sample_frac", (0.2, 0.5, 1.0))
@pytest.mark.parametrize("shuffle", (True, False))
def test_base_splitter(sample_frac, shuffle):
    ds = CoREDataset()
    group_pool = ["A", "B", "C"]
    groups = np.random.choice(group_pool, size=len(ds))

    class MySplitter(BaseSplitter):
        def _get_groups(self):
            return groups

    splitter = MySplitter(ds, sample_frac=sample_frac, shuffle=shuffle)

    train_idx, test_idx = splitter.train_test_split()
    if sample_frac < 1:
        assert len(train_idx) + len(test_idx) < len(ds)
    groups_train = set(groups[train_idx])
    groups_test = set(groups[test_idx])
    assert groups_train & groups_test == set()


@pytest.mark.parametrize("sample_frac", (0.2, 0.5, 1.0))
def test_hash_splitter(sample_frac):
    """Ensure that the splits add up to the total number of structures and are non-overlapping."""
    ds = CoREDataset()
    hs = HashSplitter(ds, hash_type="undecorated_scaffold_hash", sample_frac=sample_frac)

    for train, test in hs.k_fold(k=5):

        assert set(train) & set(test) == set()

        if sample_frac < 1:
            assert len(train) + len(test) < len(ds)
        else:
            assert len(set(list(train) + list(test))) == len(ds)

    splits = hs.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])


def test_time_splitter():
    """Ensure that the splits add up to the total number of structures and are non-overlapping."""
    ds = CoREDataset()
    ts = TimeSplitter(ds)

    for train, test in ts.k_fold(k=5):

        assert set(train) & set(test) == set()
        assert len(set(list(train) + list(test))) == len(ds)

    splits = ts.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])


def test_density_splitter():
    """Ensure that the splits add up to the total number of structures and are non-overlapping."""
    ds = CoREDataset()

    dens_splitter = DensitySplitter(ds)
    for train, test in dens_splitter.k_fold(k=5):

        assert set(train) & set(test) == set()
        assert len(set(list(train) + list(test))) == len(ds)

    splits = dens_splitter.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])

    groups = dens_splitter._get_groups()

    set0 = set(groups[splits[0]])
    set1 = set(groups[splits[1]])
    set2 = set(groups[splits[2]])

    assert set0 & set1 == set()
    assert set1 & set2 == set()
    assert set0 & set2 == set()

    splits = dens_splitter.train_test_split(
        frac_train=0.5,
    )
    groups = dens_splitter._get_groups()

    set0 = set(groups[splits[0]])
    set1 = set(groups[splits[1]])


def test_kennard_stone_splitter():
    """Ensure that the splits add up to the total number of structures and are non-overlapping."""
    ds = CoREDataset()
    # To make sure that the test does not take too long, we only use a small subset of the dataset.
    ds._df = ds._df.iloc[:500]
    ds._structures = ds._structures[:500]

    fps = KennardStoneSplitter(
        ds,
        feature_names=FEATURES,
    )
    for train, test in fps.k_fold(k=5):
        assert set(train) & set(test) == set()
        assert len(set(list(train) + list(test))) == len(ds)

    splits = fps.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])


def test_cluster_splitter():
    """Ensure that the splits add up to the total number of structures and are non-overlapping."""
    ds = CoREDataset()
    # To make sure that the test does not take too long, we only use a small subset of the dataset.
    ds._df = ds._df.iloc[:500]
    ds._structures = ds._structures[:500]

    fps = ClusterSplitter(
        ds,
        feature_names=FEATURES,
    )
    for train, test in fps.k_fold(k=5):

        assert len(set(list(train) + list(test))) == len(ds)
        assert set(train) & set(test) == set()

    splits = fps.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])


def test_cluster_stratified_splitter():
    """Ensure that the splits add up to the total number of structures and are non-overlapping.

    Also make sure that the class ratios are indeed approximately stratified.
    """
    ds = CoREDataset()

    fps = ClusterStratifiedSplitter(ds, feature_names=FEATURES, n_clusters=2)
    for train, test in fps.k_fold(k=5):

        assert len(set(list(train) + list(test))) == len(ds)
        assert set(train) & set(test) == set()

        # also make sure that the class ratios roughly make sense
        train_groups = fps._stratification_groups[train]
        test_groups = fps._stratification_groups[test]

        assert len(set(train_groups)) == len(set(test_groups)) == 2
        train_counter = Counter(train_groups)
        test_counter = Counter(test_groups)
        assert np.abs(train_counter[0] / train_counter[1] - test_counter[0] / test_counter[1]) < 10

    splits = fps.train_valid_test_split(frac_train=0.5, frac_valid=0.3)
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[1]) > len(splits[2])


def test_locov():
    """Ensure that the splits add up to the total number of structures and are non-overlapping.

    Also make sure that the class ratios are indeed approximately stratified.
    """
    ds = CoREDataset()
    # To make sure that the test does not take too long, we only use a small subset of the dataset.
    ds._df = ds._df.iloc[:1000]
    ds._structures = ds._structures[:1000]

    fps = LOCOCV(ds, feature_names=FEATURES)
    for train, test in fps.k_fold(k=5):

        assert len(set(list(train) + list(test))) == len(ds)
        assert set(train) & set(test) == set()
        assert len(train) > len(test)
    splits = fps.train_valid_test_split()
    assert len(splits) == 3
    assert len(splits[0]) > len(splits[2]) > len(splits[1])
