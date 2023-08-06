from abc import ABC, abstractmethod
from re import finditer
from typing import List, Union


from .text import Text


class Highlighter(ABC):
    def __call__(self, text: Union[str, Text]) -> Text:
        """Highlight a str or Text instance.
        
        Args:
            text (Union[str, ~Text]): Text to highlight.
        
        Raises:
            TypeError: If not called with text or str.
        
        Returns:
            Text: A test instance with highlighting applied.
        """
        if isinstance(text, str):
            highlight_text = Text(text)
        elif isinstance(text, Text):
            highlight_text = text.copy()
        else:
            raise TypeError(f"str or Text instance required, not {text!r}")
        self.highlight(highlight_text)
        return highlight_text

    @abstractmethod
    def highlight(self, text: Text) -> None:
        """Apply highlighting in place to text.
        
        Args:
            text (~Text): A text object highlight.
        """


class NullHighlighter(Highlighter):
    """A highlighter object that doesn't highlight.
    
    May be used to disable highlighting entirely.
    
    """

    def highlight(self, text: Text) -> None:
        pass


class RegexHighlighter(Highlighter):
    """Applies highlighting from a list of regular expressions."""

    highlights: List[str] = []
    base_style: str = ""

    def highlight(self, text: Text) -> None:
        """Highlight :class:`rich.text.Text` using regular expressions.
        
        Args:
            text (~Text): Text to highlighted.
        
        """
        str_text = str(text)
        base_style = self.base_style
        stylize = text.stylize
        for highlight in self.highlights:
            for match in finditer(highlight, str_text):
                _span = match.span
                for name, _ in match.groupdict().items():
                    start, end = _span(name)
                    if start != -1:
                        stylize(start, end, f"{base_style}{name}")


class ReprHighlighter(RegexHighlighter):
    """Highlights the text typically produced from ``__repr__`` methods."""

    base_style = "repr."
    highlights = [
        r"(?P<brace>[\{\[\(\)\]\}])",
        r"(?P<tag_start>\<)(?P<tag_name>\w*)(?P<tag_contents>.*?)(?P<tag_end>\>)",
        r"(?P<attrib_name>\w+?)=(?P<attrib_value>\"?\w+\"?)",
        r"(?P<bool_true>True)|(?P<bool_false>False)|(?P<none>None)",
        r"(?P<number>\-?[0-9]+\.?[0-9]*)",
        r"(?P<number>0x[0-9a-f]*)",
        r"(?P<path>(\/\w+)+\/)",
        r"(?P<filename>\/\w*\..{3,4})\s",
        r"(?P<str>b?\'\'\'.*?\'\'\'|b?\'.*?\'|b?\"\"\".*?\"\"\"|b?\".*?\")",
        r"(?P<url>https?:\/\/\S*)",
    ]


if __name__ == "__main__":  # pragma: no cover
    from .console import Console

    console = Console()

    highlighter = ReprHighlighter()

    console.print(
        highlighter(
            '''"""hello True""" print("foo", egg=5) <div class=foo bar=4>  <div class="foo"> [1, 2, 3,4] a=None qwewe True False'''
        )
    )

    from .default_styles import MARKDOWN_STYLES
    from pprint import PrettyPrinter

    pp = PrettyPrinter(indent=4, compact=False)

    # console.print(highlighter(pp.pformat(MARKDOWN_STYLES)))

    t = Text('''"""hello True""" <div class=foo>''')

    t.stylize(9, 13, "bold")

    t.stylize(0, 16, "red not bold important")

    console.print(t)
