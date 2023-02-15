from typing import Self, Set
from copy import copy


class Suspect:
    suspects: dict[str, Self] = {}

    def __init__(
        self,
        name: str,
        accuses: set[str],
        lies: set[str],
        truths: set[str],
        safes: set[str],
    ) -> None:
        """
        `accuses (set[str])`: Who they are accusing.
        `lies (set[str])`: Who they say are lying.
        `truths (set[str])`: Who they say is telling the truth.
        `safes (set[str])`: Who they say is safe. (opposite of accusing)
        """
        self.name = name

        self.accuses = set(accuses)
        self.lies = set(lies)
        self.truths = set(truths)
        self.safes = set(safes)
        self.percent = 0

        Suspect.suspects[self.name] = self

    @classmethod
    def convert_references(cls, suspect_references: list[Self | str]) -> Set[Self]:
        suspects: set[Self] = set()
        for suspect in suspect_references:
            if isinstance(suspect, str):
                if suspect in cls.suspects:
                    suspects.add(cls.suspects[suspect])
            else:
                suspects.add(suspect)
        return suspects

    @property
    def accusers(self) -> Set[Self]:
        """Get all the current suspects that are accusing them."""
        return {suspect.name for suspect in self.suspects.values() for accuse in Suspect.convert_references(suspect.accuses) if accuse.name == self.name}

    @property
    def lied(self) -> Set[Self]:
        """Get all the current suspects that are saying they are lying."""
        return {suspect.name for suspect in self.suspects.values() for lie in Suspect.convert_references(suspect.lies) if lie.name == self.name}

    @property
    def truth(self) -> Set[Self]:
        """Get all the current suspects that say that they are telling the truth."""
        return {suspect.name for suspect in self.suspects.values() for truth in Suspect.convert_references(suspect.truths) if truth.name == self.name}

    @property
    def safe(self) -> Set[Self]:
        """Get all the current suspects that are saying they are safe. (opposite of accusing)"""
        return {suspect.name for suspect in self.suspects.values() for safe in Suspect.convert_references(suspect.safes) if safe.name == self.name}

    def simplify_truths(self) -> None:
        for truth in self.__class__.convert_references(self.truths):
            for accuse in truth.accuses:
                self.accuses.add(accuse)
            for lie in truth.lies:
                self.lies.add(lie)
            for safe in truth.safes:
                self.safes.add(safe)
            for truth in truth.truths:
                self.truths.add(truth)

    def simplify_lies(self) -> None:
        for lie in self.__class__.convert_references(self.lies):
            for accuse in lie.accuses:
                self.safes.add(accuse)
            for truth in lie.truths:
                self.lies.add(truth)
            for safe in lie.safes:
                self.accuses.add(safe)
            for lie in lie.lies:
                self.truths.add(lie)
                
    @classmethod 
    def get(cls):
        # Simplify
        for suspect in cls.convert_references(cls.suspects):
            while True:
                old_accuses = suspect.accuses
                old_safes = suspect.safes
                new_accuses = copy(old_accuses)
                new_safes = copy(old_safes)
                
                suspect.simplify_truths()
                suspect.simplify_lies()

                try:
                    suspect.safes.remove(suspect.name)
                except KeyError:
                    pass
                try:
                    suspect.accuses.remove(suspect.name)
                except KeyError:
                    pass

                if old_accuses == new_accuses and old_safes == new_safes:
                    break
                
        total_points = 1
        positives = len(cls.convert_references(cls.suspects))
        for suspect in cls.convert_references(cls.suspects):
            points = len(suspect.accusers) - len(suspect.safe)
            total_points += points
            
            if points > 0:
                suspect.percent = points / total_points * 100
            else:
                for suspect_ in cls.convert_references(cls.suspects):
                    x = len(cls.convert_references(cls.suspects)) - 1
                    print(points, '/' ,total_points)
                    print(-points / total_points * 100 / x, x)
                    suspect_.percent -= -(points / total_points * 10) / x
                suspect.percent = 0

        value = 0
        suspect_ = None
        first = True
        for suspect in cls.convert_references(cls.suspects):
            
            points = len(suspect.accusers) - len(suspect.safe)
            
            if len(suspect.accusers) - len(suspect.safe) > value or first:
                value = len(suspect.accusers) - len(suspect.safe)
                suspect_ = suspect
                first = False
            
            elif len(suspect.accusers) - len(suspect.safe) == value:
                if len(suspect.accusers) - len(suspect.safe) + len(suspect.accuses) > value + len(suspect_.accuses):
                    value = len(suspect.accusers) - len(suspect.safe)
                    suspect_ = suspect

            print(suspect.name, points, str(suspect.percent) + '%')
            print('Accusers:', suspect.accusers)
            print('Safe:', suspect.safe)
            print('Accusers:', suspect.accusers)
            print('Safe:', suspect.safe)
            print('---------------------------')
                
        return suspect_.name

    @classmethod
    def reset(cls):
        cls.suspects = {}


n = Suspect('Noah',      set(),            {'Linda'},     set(),       {'Fred'})
l = Suspect('Linda',     {'Elizabeth'}, set(),            {'Fred'}, set())
e = Suspect('Elizabeth', {'Linda'},     set(),            {'Noah'}, set())
f = Suspect('Fred',      {'Noah'},      {'Elizabeth'},  set(),      set())

# a = Suspect('painter', {'roof'}, {'insulation', 'roof'}, set(), set())
# a = Suspect('insulation', {'moister'}, {'insulation', 'roof'}, set(), set())
# a = Suspect('roof', {'insulation'}, {'roof'}, set(), set())


print(Suspect.get())
