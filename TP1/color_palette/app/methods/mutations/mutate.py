import random
import numpy as np
from data_structure.Member import Member
from functions.fitness import fitness


def mutate(member: Member, target: Member, colors, mutation_probability, mutation_range) -> Member:
    for i in range(len(member.percentage)):
        if random.uniform(0, 1) < mutation_probability:
            r = random.uniform(-mutation_range, mutation_range)
            member.percentage[i] = np.clip(member.percentage[i] + r, 0, 1)
    return Member(member.percentage, fitness(target, member.percentage, colors))
