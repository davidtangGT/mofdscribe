# -*- coding: utf-8 -*-
from collections import defaultdict
from typing import List, Tuple, Union

import numpy as np
from loguru import logger
from matminer.featurizers.base import BaseFeaturizer
from pervect import PersistenceVectorizer
from pymatgen.core import IStructure, Structure

from ._tda_helpers import get_diagrams_for_structure


def _fit_transform_structures(
    transformers, structures, atom_types: Tuple[str], compute_for_all_elements: bool, min_size: int
):
    diagrams = defaultdict(lambda: defaultdict(list))
    for structure in structures:
        res = get_diagrams_for_structure(structure, atom_types, compute_for_all_elements, min_size)
        for element, element_d in res.items():
            for dim, dim_d in element_d.items():
                diagrams[element][dim].append(dim_d)

    results = defaultdict(lambda: defaultdict(list))
    for element, element_transformers in transformers.items():
        for dim, transformer in element_transformers.items():
            if len(diagrams[element][dim]) == 0:
                raise ValueError(f"{element} dimension {dim} has no diagrams")
            try:
                results[element][dim] = transformer.fit_transform(diagrams[element][dim])
            except Exception as e:
                logger.error(
                    f"Error fitting transformer: {element} {dim} {diagrams[element][dim]}", e
                )

    return transformers, results


def _transform_structures(
    transformers, structures, atom_types: Tuple[str], compute_for_all_elements: bool, min_size: int
):
    diagrams = defaultdict(lambda: defaultdict(list))
    for structure in structures:
        res = get_diagrams_for_structure(structure, atom_types, compute_for_all_elements, min_size)
        for element, element_d in res.items():
            for dim, dim_d in element_d.items():
                diagrams[element][dim].append(dim_d)

    results = defaultdict(lambda: defaultdict(list))

    for element, element_transformers in transformers.items():
        for dim, transformer in element_transformers.items():
            results[element][dim] = transformer.transform(diagrams[element][dim])

    return results


class PHVect(BaseFeaturizer):
    """
    Vectorizer for Persistence Diagrams (PDs) by approximating a training set
    of persistence diagrams with Gaussian mixture models.
    The vectorization of a diagram is then the weighted maximum likelihood estimate
    of the mixture weights for the learned components given the diagram.
    """

    def __init__(
        self,
        atom_types=(
            "C-H-N-O",
            "F-Cl-Br-I",
            "Cu-Mn-Ni-Mo-Fe-Pt-Zn-Ca-Er-Au-Cd-Co-Gd-Na-Sm-Eu-Tb-V-Ag-Nd-U-Ba-Ce-K-Ga-Cr-Al-Li-Sc-Ru-In-Mg-Zr-Dy-W-Yb-Y-Ho-Re-Be-Rb-La-Sn-Cs-Pb-Pr-Bi-Tm-Sr-Ti-Hf-Ir-Nb-Pd-Hg-Th-Np-Lu-Rh-Pu",
        ),
        compute_for_all_elements: bool = True,
        dimensions: Tuple[int] = (1, 2),
        min_size: int = 20,
        n_components: int = 20,
        apply_umap: bool = False,
        umap_n_components: int = 2,
        umap_metric: str = "hellinger",
        p: int = 1,
        random_state=None,
    ) -> None:
        atom_types = [] if atom_types is None else atom_types
        self.elements = atom_types
        self.atom_types = (
            list(atom_types) + ["all"] if compute_for_all_elements else list(atom_types)
        )
        self.compute_for_all_elements = compute_for_all_elements
        self.min_size = min_size
        self.dimensions = dimensions
        self.transformers = defaultdict(lambda: defaultdict(dict))
        for atom_type in self.atom_types:
            for dim in self.dimensions:
                self.transformers[atom_type][f"dim{dim}"] = PersistenceVectorizer(
                    n_components=n_components,
                    apply_umap=apply_umap,
                    umap_n_components=umap_n_components,
                    umap_metric=umap_metric,
                    p=p,
                    random_state=random_state,
                )
        self.n_components = n_components
        self.apply_umap = apply_umap
        self.umap_n_components = umap_n_components
        self.umap_metric = umap_metric
        self.p = p
        self.random_state = random_state
        self._fitted = False

    def _get_feature_labels(self) -> List[str]:
        labels = []
        for atom_type in self.atom_types:
            for dim in self.dimensions:
                for i in range(self.n_components):
                    labels.append(
                        f"ph_{atom_type}_{dim}_{i}" if self.apply_umap else f"ph_{atom_type}_{dim}"
                    )

        return labels

    def feature_labels(self) -> List[str]:
        return self._get_feature_labels()

    def featurize(self, structure: Union[Structure, IStructure]) -> np.ndarray:
        if not self._fitted:
            raise ValueError("Must call fit before featurizing")
        res = _transform_structures(
            self.transformers,
            [structure],
            self.elements,
            self.compute_for_all_elements,
            self.min_size,
        )
        compiled_results = self._reshape_results(res, 1)
        return compiled_results

    def fit(self, structures: Union[Structure, IStructure]) -> "PHVect":
        self.transformers, _fit_transform_structures(
            self.transformers,
            structures,
            self.elements,
            self.compute_for_all_elements,
            self.min_size,
        )
        self._fitted = True
        return self

    def _reshape_results(self, results, num_structures) -> np.ndarray:
        compiled_results = np.zeros((num_structures, len(self._get_feature_labels())))
        n_col = 0
        for _, element_results in results.items():
            for _, result in element_results.items():
                compiled_results[:, n_col : n_col + self.n_components] = result
                n_col += self.n_components
        return compiled_results

    def fit_transform(self, structures: Union[Structure, IStructure]) -> np.ndarray:
        self.transformers, results = _fit_transform_structures(
            self.transformers,
            structures,
            self.elements,
            self.compute_for_all_elements,
            self.min_size,
        )
        compiled_results = self._reshape_results(results, len(structures))
        return compiled_results

    def citations(self):
        return [
            "@article{perea2019approximating,"
            "title   = {Approximating Continuous Functions on Persistence Diagrams Using Template Functions},"
            "author  = {Jose A. Perea and Elizabeth Munch and Firas A. Khasawneh},"
            "year    = {2019},"
            "journal = {arXiv preprint arXiv: Arxiv-1902.07190}"
            "}",
            "@article{tymochko2019adaptive,"
            "title   = {Adaptive Partitioning for Template Functions on Persistence Diagrams},"
            "author  = {Sarah Tymochko and Elizabeth Munch and Firas A. Khasawneh},"
            "year    = {2019},"
            "journal = {arXiv preprint arXiv: Arxiv-1910.08506}"
            "}",
        ]

    def implementors(self):
        return ["Kevin Maik Jablonka"]