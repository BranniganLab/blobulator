"""
blobulator

Edge Detection for Protein Sequences
"""

__version__ = "0.1.0"
__author__ = "Grace Brannigan"
__credits__ = "Rutgers University - Camden"
__all__ = [
"amino_acids",
"compute_blobs",
"compute_snps",
"generate_colormaps",
]

from .amino_acids import *
from .compute_blobs import *
from .compute_snps import *
from .generate_colormaps import *