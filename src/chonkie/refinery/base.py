"""Base class for all Refinery classes."""

from abc import ABC, abstractmethod
from typing import List, Union

from chonkie.types import Chunk


class BaseRefinery(ABC):

    """Base class for all Refinery classes.

    Refinery classes are used to refine the Chunks generated from the
    Chunkers. These classes take in chunks and return refined chunks.
    Most refinery classes would be used to add additional context to the
    chunks generated by the chunkers.
    """

    def __init__(self, context_size: int = 0) -> None:
        """Initialize the Refinery."""
        if context_size < 0:
            raise ValueError("context_size must be non-negative")
        self.context_size = context_size

    @abstractmethod
    def refine(self, chunks: List[Chunk]) -> List[Chunk]:
        """Refine the given list of chunks and return the refined list."""
        raise NotImplementedError("Refine method must be implemented by subclasses")

    def refine_batch(self, chunks_batch: List[List[Chunk]]) -> List[List[Chunk]]:
        """Refine the given list of chunks and return the refined list."""
        return [self.refine(chunks) for chunks in chunks_batch]

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if the Refinery is available."""
        return True

    def __repr__(self) -> str:
        """Representation of the Refinery."""
        return f"{self.__class__.__name__}(context_size={self.context_size})"

    def __call__(
        self, chunks: Union[List[Chunk], List[List[Chunk]]]
    ) -> Union[List[Chunk], List[List[Chunk]]]:
        """Call the Refinery.

        Args:
            chunks: Either a list of Chunks or a list of lists of Chunks

        Returns:
            Refined chunks in the same format as input

        Raises:
            ValueError: If input type is not a list of Chunks or list of lists of Chunks

        """
        # If chunks is not a list or is empty, return chunks
        if not isinstance(chunks, list) or not chunks:
            return chunks

        # Check if it's a list of Chunks
        if isinstance(chunks[0], Chunk):
            return self.refine(chunks)

        # Check if it's a list of lists of Chunks
        if (
            isinstance(chunks[0], list)
            and chunks[0]
            and isinstance(chunks[0][0], Chunk)
        ):
            return self.refine_batch(chunks)

        raise ValueError(
            "Invalid input type for Refinery: must be List[Chunk] or List[List[Chunk]]"
        )
