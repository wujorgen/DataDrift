import math

# pytest looks for test*.py or *test.py


def test_sqrt():
    num = 25
    assert math.sqrt(num) == 5


def testsquare():
    num = 7
    assert 7 * 7 == 40


def testequality():
    assert 10 == 11


def testnothing():
    assert None == None
