"""
Manacher's Algorithm allows us to find the longest palindromic substring
in O(n) (i.e. linear) time and O(1) constant space.

More info:
- https://cp-algorithms.com/string/manacher.html
- https://notes.gratus.ca/On+Data+Structures/2+Manacher's+Algorithm

Below is a simple implementation.


"""


def manacher(s: str) -> str:
    """
    Simple implementation of Manachar's Algorithm
    """

    def _modify_string(s: str):
        ms = "#".join(list(s))
        return f"@#{ms}#$"

    ms = _modify_string(s)

    l = 0
    r = 0
    p = [0] * len(ms)
    pmax = 0
    pmaxi = 0
    for i in range(1, len(ms) - 1):
        mirror = l + r - i

        if i < r:
            p[i] = min(r - i, p[mirror])

        while ms[i + 1 + p[i]] == ms[i - 1 - p[i]]:
            p[i] += 1

        if i + p[i] > r:
            l = i - p[i]
            r = i + p[i]

        if pmax < p[i]:
            pmax = p[i]
            pmaxi = i

    msp = f"{ms[(pmaxi-pmax): pmaxi]}{ms[pmaxi:(pmaxi+pmax)]}".replace("#", "")
    return msp


def _alt(s: str):
    """
    Naive implementation, expanding from the center.
    """

    def expand(s, left, right):
        c_max = ""
        while left >= 0 and right < len(s) and s[left] == s[right]:
            c_max = s[left : right + 1]
            left -= 1
            right += 1
        return c_max

    a_max = ""
    for i in range(len(s)):
        i_max_odd = expand(s, i, i)
        i_max_even = expand(s, i, i + 1)

        if len(i_max_odd) > len(i_max_even):
            i_max = i_max_odd
        else:
            i_max = i_max_even

        if len(i_max) > len(a_max):
            a_max = i_max

    return a_max


def _prep():
    """
    Returns a deterministic string >10k chars with at least one palindrome.
    """
    # Start with a clear palindrome
    result = "racecar " * 1000

    # Add repetitive content to reach 10k+ characters
    base_text = "The quick brown fox jumps over the lazy dog. " * 50
    numbers = "".join(str(i) + " " for i in range(10000))
    alphabet = "abcdefghijklmnopqrstuvwxyz" * 100

    # Combine everything for a deterministic result
    result += base_text + numbers + alphabet

    # Add another obvious palindrome at the end
    result += " noon radar level"
    return result


def run_manacher():
    """
    Runs Manacher Algorithm
    """
    manacher(_prep())


def run_alt():
    """
    Run alternative, naive implementation
    """
    _alt(_prep())


def test():
    """
    Test to validate that both implementations produce
    the same result.
    """
    s = _prep()

    value_1 = manacher(s)
    value_2 = _alt(s)

    assert value_1 == value_2

    print("TEST PASSED")
