#!/usr/env/bin python3
class Novelty_map(list):
    def __init__(self,max_population):
        self.max_population = max_population
        self.min_distance_ever = list()
        super().__init__()

    def append(self,new):
        if not hasattr(new,'distance'):
            raise "new element has no distance method"

        news_distance_for_each = [new.distance(e) for e in self]
        new_min_distance = min(news_distance_for_each)

        if len(self) < self.max_population:
            super().append(new)
            self.min_distance_ever.append(new_min_distance)

        elif new_min_distance > min(self.min_distance_ever):
            #delete the element which has minimum_distance
            min_index = self.min_distance_ever.index(min(self.min_distance_ever))
            del self[min_index]
            del self.min_distance_ever[min_index]
            #append a new element and minimum distance
            self.append(new)
            self.append
