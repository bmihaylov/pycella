def life_rules(proxy):
    s = sum(proxy.neighbors)
    if s < 2 or s > 3:
        return 0
    elif s == 3 and proxy[0, 0] == 0:
        return 1
    else:
        return proxy[0, 0]

def seeds_rules(proxy):
    s = sum(proxy.neighbors)
    if s == 2 and proxy[0, 0] == 0:
        return 1
    else:
        return 0

