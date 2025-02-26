from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def update(self, obj_id, obj_data):
        """Mettre à jour un utilisateur avec les nouvelles données."""
        obj = self.get(obj_id)
        if not obj:
            return None  # L'utilisateur n'a pas été trouvé
        # Mettre à jour les informations de l'utilisateur
        obj.__dict__.update(obj_data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]