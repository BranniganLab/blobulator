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
]

from .amino_acids import *
from .compute_blobs import *
from .compute_snps import *