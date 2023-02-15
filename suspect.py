from typing import Self, Set, Iterable
from copy import copy


class Suspect:
    suspects: dict[str, Self] = {}
    total_points = 0
    human_interactions: bool = True

    def __init__(
        self,
        name: str,
        accusations: Iterable[str],
        liars: Iterable[str],
        truths: Iterable[str],
        safes: Iterable[str],
    ) -> None:
        """
        Args:
            accusers (Iterable[str]): Who they accuse.
            liars (Iterable[str]): Who they say are lying.
            truths (Iterable[str]): Who they say are telling the truth.
            safes (Iterable[str]): Who they say are not the suspect.
        """
        self.name = name

        self.accusations = set(accusations)
        self.liars = set(liars)
        self.truths = set(truths)
        self.safes = set(safes)
        
        self._points = 0
  
        self.percent = 0

        Suspect.suspects[self.name] = self

    @property
    def points(self):
        return self._points
    
    @points.setter
    def points(self, points):
        self.__class__.total_points += points - self._points
        self._points = points

    @property
    def accusers(self) -> dict[str, Self]:
        return {suspect.name: suspect for suspect in self.suspects.values() for accuse in suspect.accusations if accuse == self.name}
    
    @property
    def lies(self) -> dict[str, Self]:
        return {suspect.name: suspect for suspect in self.suspects.values() for lie in suspect.liars if lie == self.name}
    
    @property
    def truth(self) -> dict[str, Self]:
        return {suspect.name: suspect for suspect in self.suspects.values() for truth in suspect.truths if truth == self.name}

    @property
    def safe(self) -> dict[str, Self]:
        return {suspect.name: suspect for suspect in self.suspects.values() for safe in suspect.safes if safe == self.name}

    def simplify_truths(self) -> None:
        for truth in self.truth.values():
            for accuse in truth.accusations:
                self.accusations.add(accuse)
            for lie in truth.liars:
                self.liars.add(lie)
            for safe in truth.safes:
                self.safes.add(safe)
            for truth in truth.truths:
                self.truths.add(truth)

    def simplify_lies(self) -> None:
        for lie in self.lies.values():
            for accuse in lie.accusations:
                self.safes.add(accuse)
            for truth in lie.truths:
                self.liars.add(truth)
            for safe in lie.safes:
                self.accusations.add(safe)
            for lie in lie.liars:
                self.truths.add(lie)
                
    @classmethod 
    def get(cls):
        # Simplify truths and lies.
        for suspect in cls.suspects.values():
            while True:
                old_accuses = suspect.accusations
                old_safes = suspect.safes
                new_accuses = copy(old_accuses)
                new_safes = copy(old_safes)
                
                suspect.simplify_truths()
                suspect.simplify_lies()

                if cls.human_interactions:
                    try:
                        suspect.safes.remove(suspect.name)
                    except KeyError:
                        pass
                    try:
                        suspect.accusations.remove(suspect.name)
                    except KeyError:
                        pass
                
                # Goes until doesn't change anything
                if old_accuses == new_accuses and old_safes == new_safes:
                    break
                
        # Point Calculations
        for suspect in cls.suspects.values():
            suspect.points = len(suspect.accusers) - len(suspect.safe)
            
        # Percent Calculations
        for suspect in cls.suspects.values():
            if suspect._points > 0:
                suspect.percent = suspect._points / cls.total_points * 100
            else:
                negative_value = -(suspect._points / cls.total_points * 10)
                split_value = negative_value / len(cls.suspects.values())
                for suspect_ in cls.suspects.values():
                    suspect_.percent -= split_value
                suspect.percent = 0.0

        the_suspect = list(cls.suspects.values())[0]
        for suspect in cls.suspects.values():            
            if suspect.points > the_suspect.points:
                the_suspect = suspect
            
            elif suspect.points == the_suspect.points:
                if cls.human_interactions:
                    amount = 10 * (len(the_suspect.accusations) - len(suspect.accusations))
                    the_suspect.percent += amount
                    non_zero = [suspect_ for suspect_ in cls.suspects.values() if suspect_.percent != 0]
                    split_value = amount / len(non_zero)
                    for suspect_ in non_zero:
                        suspect_.percent -= split_value
                        if suspect_.percent < 0:
                            suspect_.percent = 0.0
                        elif suspect_.percent > 100:
                            suspect_.percent = 100.0

                if len(suspect.accusations) > len(the_suspect.accusations):
                    the_suspect = suspect
                    
        lst = list(cls.suspects.values())
        lst.sort(key=lambda x: x.percent)
        for suspect in lst:
            print('Name:', suspect.name, '|', str(suspect.percent) + '%', 'the Suspect')
            print('Points:', suspect.points)
            print('Accusers:', set(suspect.accusers.keys()))
            print('Safe:', set(suspect.safe.keys()))
            print('Accusations:', suspect.accusations)
            print('Safes:', suspect.safes)
            print('---------------------------')
                
        return the_suspect.name

    @classmethod
    def reset(cls):
        cls.suspects = {}


# n = Suspect('Noah',      set(),            {'Linda'},     set(),       {'Fred'})
# l = Suspect('Linda',     {'Elizabeth'}, set(),            {'Fred'}, set())
# e = Suspect('Elizabeth', {'Linda'},     set(),            {'Noah'}, set())
# f = Suspect('Fred',      {'Noah'},      {'Elizabeth'},  set(),      set())

Suspect.human_interactions = False

a = Suspect('painter', {'roof'}, {'insulation', 'roof'}, set(), set())
a = Suspect('insulation', {'moister'}, {'insulation', 'roof'}, set(), set())
a = Suspect('roof', {'insulation'}, {'roof'}, set(), set())

print(Suspect.get())
