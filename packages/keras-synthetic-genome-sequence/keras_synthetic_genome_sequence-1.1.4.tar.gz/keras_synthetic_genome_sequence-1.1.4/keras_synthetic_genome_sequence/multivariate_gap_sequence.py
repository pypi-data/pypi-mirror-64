"""Keras Sequence that returns tuples of nucleotide sequences, one with multivariate synthetic gaps and the other without as ground truth."""
from typing import Union, Dict, Tuple
import pandas as pd
import numpy as np
from keras_bed_sequence import BedSequence
from keras_mixed_sequence.utils import NumpySequence
from .utils import generate_synthetic_gaps
from numba import types
from numba.typed import Dict


class MultivariateGapSequence(BedSequence):
    """
    Keras Sequence that returns tuples of nucleotide sequences,
    one with multivariate synthetic gaps and the other without as ground truth.
    """

    def __init__(
        self,
        assembly: str,
        bed: Union[pd.DataFrame, str],
        gaps_mean: np.ndarray,
        gaps_covariance: np.ndarray,
        gaps_threshold: float = 0.4,
        batch_size: int = 32,
        verbose: bool = True,
        seed: int = 42,
        elapsed_epochs: int = 0,
        genome_kwargs: Dict = None
    ):
        """Return new GapSequence object.

        Parameters
        ----------------------------
        assembly: str,
            Genomic assembly from ucsc from which to extract sequences.
            For instance, "hg19", "hg38" or "mm10".
        bed: Union[pd.DataFrame, str],
            Either path to file or Pandas DataFrame containing minimal bed columns,
            like "chrom", "chromStart" and "chromEnd".
        gaps_mean: np.ndarray,
            Mean of the multivariate Gaussian distribution to use for generating
            the gaps in the sequences. Length of the sequences must match with
            length of the mean vector.
        gaps_covariance: np.ndarray,
            Covariance matrix of the multivariate Gaussian distribution to use
            for generating the gaps in the sequences.
            Length of the sequences must match with length of the mean vector.
        gaps_threshold: float,
            Threshold for casting the multivariate Gaussian distribution to
            a binomial multivariate distribution.
        batch_size: int = 32,
            Batch size to be returned for each request.
            By default is 32.
        verbose: bool = True,
            Whetever to show a loading bar.
        seed: int = 42,
            Starting seed to use if shuffling the dataset.
        elapsed_epochs: int = 0,
            Number of elapsed epochs to init state of generator.
        genome_kwargs: Dict = None,
            Parameters to pass to the Genome object.

        Returns
        --------------------
        Return new GapSequence object.
        """
        super().__init__(
            assembly=assembly,
            bed=bed,
            batch_size=batch_size,
            verbose=verbose,
            seed=seed,
            elapsed_epochs=elapsed_epochs,
            genome_kwargs=genome_kwargs,
        )
        if len(gaps_mean) != self.window_length:
            raise ValueError(
                "Mean len({mean_len}) does not match bed file window len({window_len}).".format(
                    mean_len=len(gaps_mean),
                    window_len=self.window_length,
                )
            )
        if len(gaps_covariance) != self.window_length:
            raise ValueError(
                "Covariance len({covariance_len}) does not match bed file window len({window_len}).".format(
                    covariance_len=len(gaps_covariance),
                    window_len=self.window_length,
                )
            )
        
        gaps_coordinates = generate_synthetic_gaps(
            gaps_mean,
            gaps_covariance,
            self.samples_number,
            chunk_size=50000,
            threshold=gaps_threshold,
            seed=seed
        )
        gaps_dictionary = {}
        for x, y in gaps_coordinates:
            if x not in gaps_dictionary:
                gaps_dictionary[x] = []
            gaps_dictionary[x].append(y)
            
        for key in gaps_dictionary:
            gaps_dictionary[key] = np.array(gaps_dictionary[key], dtype=int)
        
        self._cacheable_gaps_coordinates = gaps_dictionary
        self._gaps_coordinates = None
        
        # Rendering the starting gaps index, which
        # will be shuffled alongside the bed file.
        self._gaps_index = NumpySequence(
            np.arange(self.samples_number, dtype=np.int),
            batch_size=batch_size,
            seed=seed,
            elapsed_epochs=elapsed_epochs,
            dtype=np.int
        )

    def _init_gaps_coordinates(self):
        # Rendering the gaps coordinates
        self._gaps_coordinates = Dict.empty(
            key_type=types.int_,
            value_type=types.int_[:],
        )
        self._gaps_coordinates.update(self._cacheable_gaps_coordinates)

    def on_train_start(self, *args, **kwargs):
        super().on_train_start()
        self._init_gaps_coordinates()

    @property
    def batch_size(self) -> int:
        """Return batch size to be rendered."""
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size: int):
        """Set batch size to given value."""
        self._batch_size = batch_size
        self._gaps_index.batch_size = batch_size

    def on_epoch_end(self):
        """Shuffle private bed object on every epoch end."""
        super().on_epoch_end()
        self._gaps_index.on_epoch_end()

    def __getitem__(self, idx):
        if self._gaps_coordinates is None:
            self._init_gaps_coordinates()
        return super().__getitem__(idx)
