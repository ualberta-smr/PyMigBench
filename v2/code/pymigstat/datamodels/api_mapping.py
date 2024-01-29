from __future__ import annotations

from typing import Iterable


def mapping_id(source_lib, target_lib, source_apis, target_apis):
    source_part = ",".join(sorted(source_apis)) + "@" + source_lib
    target_part = ",".join(sorted(target_apis)) + "@" + target_lib
    return source_part + "->" + target_part


class APIMapping:
    def __init__(self, source_lib: str, target_lib: str, source_apis, target_apis, source_program_elements,
                 target_program_elements, cardinality, properties):
        self.source_lib = source_lib
        self.target_lib = target_lib
        self.source_apis = source_apis
        self.target_apis = target_apis
        self.source_program_elements = source_program_elements
        self.target_program_elements = target_program_elements
        self.cardinality = cardinality
        self.properties = set(properties)
        self.pair_id = "__".join([self.source_lib, self.target_lib])
        self.mapping_id = mapping_id(self.source_lib, self.target_lib, self.source_apis, self.target_apis)

    def __str__(self):
        return self.mapping_id


# Do not try to convert it to a regular set because it changes the object (update properties)
class APIMappingSet:
    def __init__(self):
        self._index: dict[str, APIMapping] = {}

    def merge_all(self, items: Iterable[APIMapping]):
        for item in items:
            self.merge(item)

    def merge(self, item: APIMapping):
        copy = APIMapping(item.source_lib, item.target_lib, item.source_apis, item.target_apis,
                          item.source_program_elements, item.target_program_elements, item.cardinality, item.properties)
        id = copy.mapping_id
        if id in self._index:
            copy.properties.update(self._index[id].properties)

        self._index[id] = copy

    def __iter__(self):
        return iter(self._index.values())

    def __len__(self):
        return len(self._index)
