crit_chance = 0.19
crit_power = 5.13

super_crit_chance = 0.03
super_crit_power = 2

crit_help = 1 + crit_chance * crit_power

real_super_crit_chance = crit_chance * super_crit_chance
super_crit_help = 1 + real_super_crit_chance * crit_power * super_crit_power


print(crit_help)

print(real_super_crit_chance)
print(super_crit_help)


bee_ability_rate = 1.24
bee_ability_pollen = 1.13

extra_bees = 50 * (bee_ability_rate + bee_ability_pollen - 1) - 50

print(extra_bees)

attack_total = 1252
attack_mult = 1.66


