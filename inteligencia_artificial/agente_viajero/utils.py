from random import randint

class BaseClass:
    def calculate_distance(self, p: tuple, q: tuple) -> float:
        sqt_diff = 0
        for x, y in zip(p, q):
            sqt_diff += (x - y)**2
        dist = sqt_diff**0.5
        return dist
    

    def inversion_reprod(self, prev_winner: list) -> list:
        to_keep = randint(0,1)
        if to_keep==0: parent = prev_winner[1:]
        else: parent = prev_winner[:-1]

        first_point = randint(0, len(parent) - 1)
        end_point = randint(first_point + 1, len(parent))

        fragment = parent[first_point:end_point]
        inversion = fragment[::-1]

        child = parent[:first_point] + inversion + parent[end_point:]

        if to_keep==0: return prev_winner[:1] + child
        else: return child + prev_winner[-1:]


    def castling_reprod(self, parent: list) -> list:
        first_point = randint(0, len(parent) - 2)

        max_len_to_switch = len(parent[first_point:]) // 2
        len_to_switch = randint(1, max_len_to_switch)        

        first_point_end = first_point + len_to_switch

        end_point = randint(first_point_end, len(parent) - len_to_switch)
        end_point_end = end_point + len_to_switch

        child = parent[:first_point] 
        child += parent[end_point:end_point_end]
        child += parent[first_point_end:end_point]
        child += parent[first_point:first_point_end]
        child += parent[end_point_end:]
        return child