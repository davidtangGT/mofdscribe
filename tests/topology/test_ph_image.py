# -*- coding: utf-8 -*-
from mofdscribe.topology.ph_image import PHImage


def test_phimage(hkust_structure, irmof_structure):
    phi = PHImage()
    for structure in [hkust_structure, irmof_structure]:
        features = phi.featurize(structure)
        assert len(features) == 20 * 20 * 4 * 3

    assert len(phi.feature_labels()) == 20 * 20 * 4 * 3


def test_phimage_fit(hkust_structure, irmof_structure):
    phi = PHImage()
    phi.fit([hkust_structure, irmof_structure])

    assert len(phi.max_B) == len(phi.max_P) == 4
    assert phi.max_B[0] == phi.max_B[3] == 0
    assert 3.4 < phi.max_B[1] < 3.5

    assert 3.4 < phi.max_P[0] < 3.5