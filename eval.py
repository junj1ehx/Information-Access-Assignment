

def euclidean(u1, u2):
    try:
        value = sum((u1 - u2)**2)**0.5
    except ZeroDivisionError:
        value = 0
    return value


def cosine(u1, u2):
    denominator = (sum(u1*u1)*sum(u2*u2))**0.5
    try:
        value = sum(u1*u2)/denominator
    except ZeroDivisionError:
        value = 0
    return value


def pearson(u1, u2):
    mean1, mean2 = u1.mean(), u2.mean()
    denominator = (sum((u1-mean1)**2)*sum((u2-mean2)**2))**0.5
    try:
        value = sum((u1 - mean1) * (u2 - mean2)) / denominator
    except ZeroDivisionError:
        value = 0
    return value