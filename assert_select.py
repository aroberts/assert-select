from lxml import html
import re

re_type = type(re.compile(''))

class Page(object):
    '''
    Represents an HTML page, probably rendered from a view, but could be
    sourced from anywhere
    '''

    def __init__(self, content=None, filename=None):
        if filename:
            self.root = html.parse(filename).getroot()
        else:
            self.root = html.fromstring(content)

    def css_select(self, selector):
        '''
        Takes a string as a CSS selector, and returns all the elements
        found by the selector.
        '''
        return self.root.cssselect(selector)

    def assert_select(self, selector, equality=True, message=None, **tests):
        '''
        Asserts that a css selector captures data from this Page, and 
        that that data passes the test presented by the equality specifier.

        (from rails:)
        The test may be one of the following:
            * true - Assertion is true if at least one element selected.
            * false - Assertion is true if no element selected.
            * String/Regexp - Assertion is true if the text value of 
              at least one element matches the string or regular expression.
            * Int - Assertion is true if exactly that number of
              elements are selected.
            * List of Int- Assertion is true if the number of selected
              elements is between the max and min of the list
            
        If no equality test specified, the assertion is true if at
        least one element selected.
        
        To perform more than one equality test, use the following keyword
        arguments:
            text - Narrow the selection to elements that have this text value (string or regexp).
            count - Assertion is true if the number of selected elements is equal to this value.
            minimum - Assertion is true if the number of selected elements is at least this value.
            maximum - Assertion is true if the number of selected elements is at most this value.
        '''

        # set up tests
        equality_type = type(equality)
        if equality_type == bool:
            if equality:
                tests['count'] = 0
            else:
                tests['minimum'] = 1
        elif equality_type == int:
            tests['count'] = equality
        elif equality_type in (str, re_type):
            tests['text'] = equality
        elif equality_type == list:
            tests['maximim'] = max(equality)
            tests['minimum'] = min(equality)
        else:
            raise TypeError("Couldn't understand equality: %s" % \
                            repr(equality))

        if 'count' in tests:
            tests['minimum'] = tests['maximum'] = tests['count']
        else:
            tests['minimum'] = tests.get('minimum', 1)

        elements = self.css_select(selector)
        if 'text' in tests:
            match_with = tests['text']
            if type(match_with) == str:
                filtered_elements = [e for e in elements
                                     if match_with in e.text_content()]
            else:
                filtered_elements = [e for e in elements
                                     if match_with.match(e.text_content())]

        else:
            filtered_elements = elements

        if not filtered_elements:
            message = message or "%s expected, but was %s" % (
                tests['text'],
                ''.join([e.text_content() for e in elements])
            )

        count_message = "%s elements expected, found %s"
        length = len(filtered_elements)
        count = tests.get('count', None)
        minimum = tests.get('minimum', None)
        maximum = tests.get('maximum', None)
        if count:
            message = message or count_message % (count, length)
            assert count == length, message
        else:
            if minimum:
                message = message or count_message % (
                    "at least %s" % minimum,
                    length
                )
                assert length >= minimum, message
            if maximum:
                message = message or count_message % (
                    "at most %s" % maximum,
                    length
                )
                assert length <= maximum, message

        return filtered_elements



