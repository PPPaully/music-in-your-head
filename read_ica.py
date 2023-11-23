import mne
import numpy as np
import json
from inspect import signature
from mne.io import fiff_open
from mne.io.meas_info import read_meas_info
from mne.io.tree import dir_tree_find
from mne.io.constants import FIFF
from mne.io.tag import read_tag

_KNOWN_ICA_METHODS = ("fastica", "infomax", "picard")

def _deserialize(str_, outer_sep=";", inner_sep=":"):
    """Aux Function."""
    out = {}
    for mapping in str_.split(outer_sep):
        k, v = mapping.split(inner_sep, 1)
        out[k] = json.loads(v)
    return out

def read_ica(ica_file_path):
    fid, tree, _ = fiff_open(ica_file_path)
    info, _ = read_meas_info(fid, tree, clean_bads=True)
    ica_data = dir_tree_find(tree, FIFF.FIFFB_MNE_ICA)
    if len(ica_data) == 0:
        ica_data = dir_tree_find(tree, 123)  # Constant 123 Used before v 0.11
        if len(ica_data) == 0:
            fid.close()
            raise ValueError("Could not find ICA data")
    my_ica_data = ica_data[0]
    ica_reject = None
    for d in my_ica_data["directory"]:
        kind = d.kind
        pos = d.pos
        if kind == FIFF.FIFF_MNE_ICA_INTERFACE_PARAMS:
            tag = read_tag(fid, pos)
            ica_init = tag.data
        elif kind == FIFF.FIFF_MNE_ROW_NAMES:
            tag = read_tag(fid, pos)
            ch_names = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_WHITENER:
            tag = read_tag(fid, pos)
            pre_whitener = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_PCA_COMPONENTS:
            tag = read_tag(fid, pos)
            pca_components = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_PCA_EXPLAINED_VAR:
            tag = read_tag(fid, pos)
            pca_explained_variance = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_PCA_MEAN:
            tag = read_tag(fid, pos)
            pca_mean = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_MATRIX:
            tag = read_tag(fid, pos)
            unmixing_matrix = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_BADS:
            tag = read_tag(fid, pos)
            exclude = tag.data
        elif kind == FIFF.FIFF_MNE_ICA_MISC_PARAMS:
            tag = read_tag(fid, pos)
            ica_misc = tag.data
        elif kind == FIFF.FIFF_MNE_EPOCHS_REJECT_FLAT:
            tag = read_tag(fid, pos)
            ica_reject = json.loads(tag.data)["reject"]

    fid.close()

    ica_init, ica_misc = [_deserialize(k) for k in (ica_init, ica_misc)]
    n_pca_components = ica_init.pop("n_pca_components")
    current_fit = ica_init.pop("current_fit")
    max_pca_components = ica_init.pop("max_pca_components")
    method = ica_misc.get("method", "fastica")

    if method in _KNOWN_ICA_METHODS:
        ica_init["method"] = method

    print("Now restoring ICA solution ...")

    # make sure dtypes are np.float64 to satisfy fast_dot
    def f(x):
        return x.astype(np.float64)

    ica_init = {
        k: v for k, v in ica_init.items() if k in signature(mne.preprocessing.ICA.__init__).parameters
    }
    ica_init['method'] = 'infomax'
    ica_init['fit_params'] = dict(extended=True)
    ica_init['n_components'] = 61
    ica = mne.preprocessing.ICA(**ica_init)
    ica.current_fit = current_fit
    ica.ch_names = ch_names.split(":")
    if n_pca_components is not None and not isinstance(n_pca_components, int_like):
        n_pca_components = np.float64(n_pca_components)
    ica.n_pca_components = n_pca_components
    ica.pre_whitener_ = f(pre_whitener)
    ica.pca_mean_ = f(pca_mean)
    ica.pca_components_ = f(pca_components)
    ica.n_components_ = unmixing_matrix.shape[0]
    ica._max_pca_components = max_pca_components
    ica._update_ica_names()
    ica.pca_explained_variance_ = f(pca_explained_variance)
    ica.unmixing_matrix_ = f(unmixing_matrix)
    ica._update_mixing_matrix()
    ica.exclude = [] if exclude is None else list(exclude)
    ica.info = info
    if "n_samples_" in ica_misc:
        ica.n_samples_ = ica_misc["n_samples_"]
    if "labels_" in ica_misc:
        labels_ = ica_misc["labels_"]
        if labels_ is not None:
            ica.labels_ = labels_
    if "method" in ica_misc:
        ica.method = ica_misc["method"]
    if "n_iter_" in ica_misc:
        ica.n_iter_ = ica_misc["n_iter_"]
    if "fit_params" in ica_misc:
        ica.fit_params = ica_misc["fit_params"]
    ica.reject_ = ica_reject
    
    return ica