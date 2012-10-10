from assert_select import Page

from nose.tools import *

import re

class TestAssertSelect(object):

    def setup(self):
        self.full_page = Page(filename="test/test.html")
        self.fragment = Page(filename="test/fragment.html")

        with file("test/fragment.html") as f:
            self.string = Page(content=f.read())

    def test_page_init_full_page(self):
        assert self.full_page

    def test_page_init_fragment(self):
        assert self.fragment

    def test_css_select(self):
        nodes = self.fragment.css_select("div.secondary strong")
        assert_equals(len(nodes), 2)
        for node in nodes:
            print type(node)
            assert_equals(node.name, "strong")

    def test_assert_select_string_defaults(self):
        strongs = self.string.assert_select("strong")
        assert_equals(len(strongs), 2)

    def test_assert_select_defaults(self):
        strongs = self.fragment.assert_select("strong")
        assert_equals(len(strongs), 2)

    def test_as_count(self):
        self.fragment.assert_select("strong", 2)
        try:
            self.fragment.assert_select("strong", 3)
        except AssertionError, e:
            assert_in("3", e.message)
            assert_in("found 2", e.message)

    def test_as_range(self):
        self.fragment.assert_select("strong", [2,5])
        try:
            self.fragment.assert_select("strong", [3,5])
        except AssertionError, e:
            assert_in("at least 3", e.message)
            assert_in("found 2", e.message)

        try:
            self.fragment.assert_select("strong", [0,1])
        except AssertionError, e:
            assert_in("at most 1", e.message)
            assert_in("found 2", e.message)
    
    def test_as_text(self):
        nodes = self.fragment.assert_select("strong", "public")
        assert_equals(len(nodes), 1)

    def test_as_text_via_string(self):
        nodes = self.string.assert_select("strong", "public")
        assert_equals(len(nodes), 1)

    def test_as_true(self):
        self.string.assert_select("div.main p", True)

    def test_as_count_0(self):
        try:
            self.string.assert_select("div.main p", 0)
        except AssertionError:
            return
        assert 0, "Should have raised exception"

    def test_as_false(self):
        self.string.assert_select("div.main p a", False)

    def test_as_regex(self):
        nodes = self.fragment.assert_select("strong", re.compile("(public|private)"))
        assert_equals(len(nodes), 2)

