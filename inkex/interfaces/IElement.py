from abc import ABC, abstractmethod

from lxml import etree


class IBaseElement(ABC, etree.ElementBase):
    """Abstraction for BaseElement to avoid circular imports"""

    @abstractmethod
    def get_id(self, as_url=0):
        """Returns the element ID. If not set, generates a unique ID."""
        raise NotImplementedError


class ISVGDocumentElement(IBaseElement):
    """Abstraction for SVGDocumentElement"""
