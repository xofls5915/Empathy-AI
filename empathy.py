import math
def theta(D):
    return 4 + 0.2*D


def ceiling(D):
    return max(0,1-0.04*D)


def empathy(I,R,D):

    return ceiling(D)/(1+math.exp(-(I*R-theta(D))))