from ecs.entity import new_entity


class World:
    def __init__(self):
        self._entities = {}
        self._systems = []

    def create_entity(self):
        eid = new_entity()
        self._entities[eid] = {}
        return eid

    def add_component(self, entity_id, component):
        self._entities[entity_id][type(component)] = component

    def get_component(self, entity_id, component_type):
        return self._entities[entity_id].get(component_type)

    def query(self, *component_types):
        results = []
        for eid, comps in self._entities.items():
            if all(ct in comps for ct in component_types):
                results.append((eid, *[comps[ct] for ct in component_types]))
        return results

    def remove_entity(self, entity_id):
        self._entities.pop(entity_id, None)

    def add_system(self, system):
        self._systems.append(system)

    def update(self, **kwargs):
        for system in self._systems:
            system.update(self, **kwargs)
