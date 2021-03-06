#!/usr/bin/python3

'''Variants of memories.'''

import pickle
import os

class NoMemory(object):
    """Memory that recalls nothing."""

    def recall_destination_for_nature(self, klass):
        pass

    def recall_associated_hint(self, hint):
        pass

    def remember_destination_for_nature(self, klass, dest):
        """dest must be an absolute path, or None."""
        pass

    def remember_associated_hint(self, hint, substitution):
        pass

class SerializableMemory(object):
    """Memory that can be reconstituted from a serialization format."""

    def __init__(self):
        self.destinations_for_nature = dict()
        self.associated_hints = dict()

    @classmethod
    def deserialize(klass, pickled):
        """Constructs a new SerializableMemory out of a pickle with data."""
        d, a = pickle.loads(pickled, encoding="bytes")
        m = klass()
        m.destinations_for_nature = d
        m.associated_hints = a
        return m

    def serialize(self):
        """Serializes the data of the SerializableMemory to a string."""
        return pickle.dumps((self.destinations_for_nature, self.associated_hints))

    def recall_destination_for_nature(self, klass):
        return self.destinations_for_nature.get(klass)

    def recall_associated_hint(self, hint):
        return self.associated_hints.get(hint)

    def remember_destination_for_nature(self, klass, dest):
        """dest must be an absolute path, or None."""
        if dest is None and klass in self.destinations_for_nature:
            del self.destinations_for_nature[klass]
        if dest is not None:
            if dest != os.path.abspath(dest):
                raise ValueError("%r is not an absolute path" % dest)
            self.destinations_for_nature[klass] = dest

    def remember_associated_hint(self, hint, substitution):
        if substitution is None and hint in self.associated_hints:
            del self.associated_hints[hint]
        if substitution is not None:
            self.associated_hints[hint] = substitution
