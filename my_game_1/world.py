from pygame.event import Event

from entities import new_entity


class World:
    def __init__(self):
        self._entities = {}
        self._systems = []

    def create_entity(self):
        entity_id = new_entity()
        self._entities[entity_id] = {}
        return entity_id

    def add_component(self, entity_id: int, component):
        self._entities[entity_id] = component

    def add_system(self, system):
        self._systems.append(system)

    def update(self, **kwargs):
        for system in self._systems:
            system.update(**kwargs)

