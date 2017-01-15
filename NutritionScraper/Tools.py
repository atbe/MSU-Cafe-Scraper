import itertools

def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append('%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def get_ascii_portion(input_str):
    out = ""
    print(input_str)
    for ch in input_str:
        print(ord(ch))
    #     if is_ascii(ch):
    #         out ++ ch
    return out

def is_ascii(s):
    try:
        s.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

