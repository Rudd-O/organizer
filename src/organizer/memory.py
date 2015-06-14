#!/usr/bin/env python

'''Variants of memories.'''

import cPickle

class NoMemory(object):
    """Memory that recalls nothing."""

    def recall_destination_for_nature(self, klass):
        pass

    def recall_associated_hint(self, hint):
        pass

    def remember_destination_for_nature(self, klass, dest):
        pass

    def remember_associated_hint(self, hint, substitution):
        pass

class SerializableMemory(object):
    """Memory that can be reconstituted from a serialization format."""

    def __init__(self):
        self.destinations_for_nature = dict()
        self.associated_hints = dict()

    @classmethod
    def deserialize(klass, pickle):
        """Constructs a new SerializableMemory out of a pickle with data."""
        d, a = cPickle.loads(pickle)
        m = klass()
        m.destinations_for_nature = d
        m.associated_hints = a

    def serialize(self):
        """Serializes the data of the SerializableMemory to a string."""
        return cPickle.dumps((self.destinations_for_nature, self.associated_hints))

    def recall_destination_for_nature(self, klass):
        return self.destinations_for_nature.get(klass)

    def recall_associated_hint(self, hint):
        return self.associated_hints.get(hint)

    def remember_destination_for_nature(self, klass, dest):
        if dest is None and klass in self.destinations_for_nature:
            del self.destinations_for_nature[klass]
        if dest is not None:
            self.destinations_for_nature[klass] = dest

    def remember_associated_hint(self, hint, substitution):
        if substitution is None and hint in self.associated_hints:
            del self.associated_hints[hint]
        if substitution is not None:
            self.associated_hints[hint] = substitution
