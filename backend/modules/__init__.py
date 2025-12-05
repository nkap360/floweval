"""
Modules Package
===============
Specialized modules for advanced functionality.

Contains:
- DeepEval synthesizer for golden generation
- Custom evaluation modules
- Integration modules
"""

from .deepeval_synthesizer import generate_goldens_from_documents

__all__ = [
    "generate_goldens_from_documents",
]
