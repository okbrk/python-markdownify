"""
Test whitelisting/blacklisting of specific tags.

"""
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter, markdownify, LSTRIP, RSTRIP, STRIP, STRIP_ONE
from .utils import md


def test_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=['a'])
    assert text == 'Some Text'


def test_do_not_strip():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', strip=[])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=['a'])
    assert text == '[Some Text](https://github.com/matthewwithanm)'


def test_do_not_convert():
    text = md('<a href="https://github.com/matthewwithanm">Some Text</a>', convert=[])
    assert text == 'Some Text'


def test_strip_document():
    assert markdownify("<p>Hello</p>") == "Hello"  # test default of STRIP
    assert markdownify("<p>Hello</p>", strip_document=LSTRIP) == "Hello\n\n"
    assert markdownify("<p>Hello</p>", strip_document=RSTRIP) == "\n\nHello"
    assert markdownify("<p>Hello</p>", strip_document=STRIP) == "Hello"
    assert markdownify("<p>Hello</p>", strip_document=None) == "\n\nHello\n\n"


def test_strip_document_tag():
    html = "<html><body><div><p>hello</p></div></body></html>"
    soup = BeautifulSoup(html, "html.parser")
    tag = soup.find("html")
    assert MarkdownConverter().convert_soup(soup) == "hello"
    assert MarkdownConverter().convert_soup(tag) == "hello"
    assert MarkdownConverter(strip_document=LSTRIP).convert_soup(tag) == "hello\n\n"
    assert MarkdownConverter(strip_document=RSTRIP).convert_soup(tag) == "\n\nhello"
    assert MarkdownConverter(strip_document=None).convert_soup(tag) == "\n\nhello\n\n"


def test_strip_pre():
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>") == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP) == "```\n  Hello\n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=STRIP_ONE) == "```\n  \n  Hello  \n  \n```"
    assert markdownify("<pre>  \n  \n  Hello  \n  \n  </pre>", strip_pre=None) == "```\n  \n  \n  Hello  \n  \n  \n```"


def bs4_options():
    assert markdownify("<p>Hello</p>", bs4_options="html.parser") == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options=["html.parser"]) == "Hello"
    assert markdownify("<p>Hello</p>", bs4_options={"features": "html.parser"}) == "Hello"
