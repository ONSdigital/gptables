from dataclasses import dataclass
from typing import List

from gptables.core.gptable import FormatList


@dataclass
class Cover:
    """
    Stores cover sheet properties.

    Attributes
    ----------
    title : str
        Cover page title
    intro : List[str, list], optional
        Introductory text
    about : List[str, list], optional
        About/notes text
    contact : List[str, list], optional
        Contact details text
    cover_label : str
        Cover page tab label, defaults to "Cover"
    width: int
        Width of the column, defaults to 85
    """

    def __init__(
        self,
        title: str,
        intro: List = None,
        about: List = None,
        contact: List = None,
        cover_label: str = "Cover",
        width: int = 85,
    ) -> None:

        self.title = title
        self.intro = self._parse_formatting(intro)
        self.about = self._parse_formatting(about)
        self.contact = self._parse_formatting(contact)
        self.cover_label = cover_label
        self.width = width

        # TODO: Add input validation (e.g. empty list)

    @staticmethod
    def _parse_formatting(attribute) -> List:
        """Check attribute for a list. If there is a list then cast the list to a FormatList in attribute.

        Parameters
        ----------
        attribute : List[str, list]

        Returns
        -------
        List[str, FormatList]
        """

        if isinstance(attribute, list):
            attribute = [
                FormatList(text) if isinstance(text, list) else text
                for text in attribute
            ]
        return attribute
