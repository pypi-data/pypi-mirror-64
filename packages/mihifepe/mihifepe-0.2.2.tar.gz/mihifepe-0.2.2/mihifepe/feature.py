"""Feature class"""
import anytree
import cityhash
import numpy as np

from mihifepe import constants


# pylint: disable = too-many-instance-attributes
class Feature(anytree.Node):
    """Class representing feature/feature group"""
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.parent_name = kwargs.get(constants.PARENT_NAME, "")
        self.description = kwargs.get(constants.DESCRIPTION, "")
        self.static_indices = kwargs.get(constants.STATIC_INDICES, [])
        self.temporal_indices = kwargs.get(constants.TEMPORAL_INDICES, [])
        self._rng_seed = kwargs.get(constants.RNG_SEED, cityhash.CityHash32(name))
        self.rng = None

    @property
    def rng_seed(self):
        """Get RNG seed"""
        return self._rng_seed

    @rng_seed.setter
    def rng_seed(self, seed):
        """Set RNG seed"""
        self._rng_seed = seed

    def initialize_rng(self):
        """Initialize random number generator for feature (used for shuffling perturbations)"""
        self.rng = np.random.RandomState(self._rng_seed)

    def uniquify(self, uniquifier):
        """Add uniquifying identifier to name"""
        assert uniquifier
        self.name = "{0}->{1}".format(uniquifier, self.name)

    @staticmethod
    def unpack_indices(str_indices):
        """Converts tab-separated string of indices to int list"""
        if not str_indices:
            return []
        return [int(idx) for idx in str_indices.split("\t")]

    @staticmethod
    def pack_indices(int_indices):
        """Converts int list of indices to tab-separated string"""
        return "\t".join([str(idx) for idx in int_indices])

    @staticmethod
    def size(feature):
        """Returns'size' of feature"""
        return len(feature.static_indices) + len(feature.temporal_indices)
