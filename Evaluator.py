import cv2
from Target import Target


def evaluate(targets):
    print('评估')
    current_level = targets[0].level
    chosen = targets[0]
    for each in targets:
        if each.level < current_level:
            if chosen.number != -1:
                print('优先攻击', chosen.x, ',', chosen.y)
                return chosen
            else:
                chosen = each

        if each.number > chosen.number:
            chosen = each
    print('优先攻击', chosen.x, ',', chosen.y)
    return chosen

