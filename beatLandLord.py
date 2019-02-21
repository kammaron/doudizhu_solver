# -*- coding: UTF-8 -*-
# Author: Tim Wu
# Author: Carl King


class COMB_TYPE:
    PASS, SINGLE, PAIR, TRIPLE, TRIPLE_ONE, TRIPLE_TWO, FOURTH_TWO_ONES, FOURTH_TWO_PAIRS, STRIGHT, BOMB = range(10)


little_joker, big_joker = 18, 19
HAND_PASS = {'type':COMB_TYPE.PASS, 'main': 0, 'component':[]}


def get_all_hands(pokers):
    if not pokers:
        return []

    combs = [HAND_PASS]

    dic = counter(pokers)

    if little_joker in pokers and big_joker in pokers:
        combs.append({'type':COMB_TYPE.BOMB, 'main': big_joker, 'component': [big_joker, little_joker]})

    for poker in dic:
        if dic[poker] >= 1:
            combs.append({'type':COMB_TYPE.SINGLE, 'main':poker, 'component':[poker]})

        if dic[poker] >= 2:
            combs.append({'type':COMB_TYPE.PAIR, 'main':poker, 'component':[poker, poker]})

        if dic[poker] >= 3:
            combs.append({'type':COMB_TYPE.TRIPLE, 'main':poker, 'component':[poker, poker, poker]})
            for poker2 in dic:
                if ALLOW_THREE_ONE and dic[poker2] >= 1 and poker2 != poker:
                    combs.append({'type':COMB_TYPE.TRIPLE_ONE, 'main':poker, 'component': [poker, poker, poker, poker2]})
                if ALLOW_THREE_TWO and dic[poker2] >= 2 and poker2 != poker:
                    combs.append({'type':COMB_TYPE.TRIPLE_TWO, 'main':poker, 'component': [poker, poker, poker, poker2, poker2]})

        if dic[poker] == 4:
            combs.append({'type':COMB_TYPE.BOMB, 'main':poker, 'component': [poker, poker, poker, poker]})
            if ALLOW_FOUR_TWO:
                pairs = []
                ones = []
                for poker2 in dic:
                    if dic[poker2] == 1:
                        ones.append(poker2)
                    elif dic[poker2] == 2:
                        pairs.append(poker2)

                for i in range(len(ones)):
                    for j in range(i + 1, len(ones)):
                        combs.append({'type':COMB_TYPE.FOURTH_TWO_ONES, 'main':poker, \
                            'component':[poker, poker, poker, poker, ones[i], ones[j]]})

                for i in range(len(pairs)):
                    combs.append({'type':COMB_TYPE.FOURTH_TWO_ONES, 'main':poker, \
                        'component': [poker, poker, poker, poker, pairs[i], pairs[i]]})
                    for j in range(i + 1, len(pairs)):
                        combs.append({'type':COMB_TYPE.FOURTH_TWO_PAIRS, 'main':poker, \
                            'component': [poker, poker, poker, poker, pairs[i], pairs[i], pairs[j], pairs[j]]})

    for straight in create_straight(list(set(pokers)), 5):
        combs.append({'type':COMB_TYPE.STRIGHT * len(straight), 'main': straight[0], 'component': straight})

    return combs


def create_straight(list_of_nums, min_length):
    a = sorted(list_of_nums)
    lens = len(a)
    for start in range(0, lens):
        for end in range(start, lens):
            if a[end] - a[start] != end - start:
                break
            elif end - start >= min_length - 1:
                yield list(range(a[start], a[end] + 1))



def counter(pokers):
    dic = {}
    for poker in pokers:
        dic[poker] = pokers.count(poker)
    return dic



def can_beat(comb1, comb2):
    if not comb2 or comb2['type'] == COMB_TYPE.PASS:
        return False

    if not comb1 or comb1['type'] == COMB_TYPE.PASS:
        return True

    if comb1['type'] == comb2['type']:
        return comb2['main'] > comb1['main']
    elif comb2['type'] == COMB_TYPE.BOMB:
        return True
    else:
        return False


def make_bare_hand(pokers, hand):
    for poker in hand:
        pokers.remove(poker)


def make_hand(pokers, hand):
    poker_clone = pokers[:]
    for poker in hand['component']:
        poker_clone.remove(poker)
    return poker_clone



def hand_out(my_pokers, enemy_pokers, raider, last_hand = None, cache = {}):
    if not my_pokers:
        return True
        
    if not enemy_pokers:
        return False

    if last_hand is None:
        last_hand = HAND_PASS

    key = str((my_pokers, enemy_pokers, last_hand['component']))
    if key in cache:
        return cache[key]

    for current_hand in get_all_hands(my_pokers):
        if can_beat(last_hand, current_hand) or \
        (last_hand['type'] != COMB_TYPE.PASS and current_hand['type'] == COMB_TYPE.PASS):
            if not hand_out(enemy_pokers, make_hand(my_pokers, current_hand), raider, current_hand, cache):
                # print(True,' :', key)
                # print(key,current_hand)
                raider[key] = current_hand
                cache[key] = True
                return True

    # print(False, ':', key)
    cache[key] = False
    return False

def trans(c):
    return {
            't':10,
            'j':11,
            'q':12,
            'k':13,
            '1':14,
            '2':16,
            'w':18,
            'W':19
            }.get(c)

def get_input(vec):
    s = input()
    for i in range(len(s)):
        if s[i] >= '3' and s[i] <= '9':
            vec.append(int(s[i]))
        else:
            vec.append(trans(s[i]))


if __name__ == '__main__':
    import time
    start = time.clock()

    ALLOW_THREE_ONE = True
    ALLOW_THREE_TWO = True
    ALLOW_FOUR_TWO = True

    lord = []
    farmer = []
    print('input lord\'s cards')
    get_input(lord)
    print(lord)
    print('input farmer\'s cards')
    get_input(farmer)
    print(farmer)
    #print("first hand or not? 1 for first, 0 for not")
    #first = int(input())
    #if first == 0:
    #    to_beat=[]
    #    get_input(to_beat)
    #    combs = get_all_hands(to_beat)
    #    result = hand_out(farmer, lord, combs[1])
    #else:
    raider = {}
    result = hand_out(farmer, lord, raider)


    elapsed = (time.clock() - start)

    print("Result:", result)
    print("Elapsed:", elapsed)
    
    #finish the game
    last_hand = []
    while farmer:
        key = str((farmer, lord, last_hand))
        my_hand = raider[key]['component']
        print('please play:', str(my_hand))
        make_bare_hand(farmer, my_hand)
        if not farmer:
            break
        print('input lord\'s hand:')
        last_hand = []
        get_input(last_hand)
        make_bare_hand(lord, last_hand)

    print('finished!')


