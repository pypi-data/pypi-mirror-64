"""
This module contains predicates which influence what counts as a match
If the predicate (function) returns True, the match will be ignored
"""
import operator


def compose(f, g):
    return lambda doc, start, end: f(g(doc, start, end))


def neg(f):
    # function negatin, ex. neg(preceeded_by_pos(pos))
    return compose(operator.not_, f)


def succeeded_by_phrase(phrase):
    return lambda doc, start, end: doc[end:].text.lower().startswith(phrase.lower())


def preceded_by_phrase(phrase):
    return lambda doc, start, end: doc[:start].text.lower().endswith(phrase.lower())

# backward compatibility
def preceeded_by_phrase(phrase):
    raise DeprecationWarning
    print("Use 'preceded_by_phrase' instead.")
    return preceded_by_phrase(phrase)


def succeeded_by_pos(pos):
    return lambda doc, start, end: doc[end].pos_ == pos


def preceded_by_pos(pos):
    return lambda doc, start, end: doc[start - 1].pos_ == pos

# backward compatibility
def preceeded_by_pos(pos):
    raise DeprecationWarning
    print("Use 'preceded_by_pos' instead.")
    return preceded_by_pos(pos)


def succeeded_by_dep(dep):
    return lambda doc, start, end: doc[end].dep_ == dep


def preceded_by_dep(dep):
    return lambda doc, start, end: doc[start - 1].dep_ == dep

# backward compatibility
def preceeded_by_dep(dep):
    raise DeprecationWarning
    print("Use 'preceded_by_dep' instead.")
    return preceded_by_dep(dep)


def surrounded_by_phrase(phrase):
    def _surrounded_by_hook(doc, start, end):
        preceeds = doc[:start].text.lower().endswith(phrase.lower())
        follows = doc[end:].text.lower().startswith(phrase.lower())
        return preceeds and follows

    return _surrounded_by_hook


def part_of_compound():
    def _word_is_part_of_compound_hook(doc, start, end):
        head = doc[start]
        is_compound = head.dep_ == "compound"
        is_part_of_compound = any(
            [t.dep_ == "compound" and t.head == head for t in doc]
        )
        return is_compound or is_part_of_compound

    return _word_is_part_of_compound_hook


def succeeded_by_num():
    return lambda doc, start, end: doc[end].like_num or doc[end].pos_ == "NUM" or doc[end].is_digit


def succeeded_by_currency():
    return lambda doc, start, end: doc[end].is_currency