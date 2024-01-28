from datamodels.api_mapping import APIMappingSet
from datamodels.loaders import load_migs
from datamodels.migration import Migration
from taxonomy.constants import *


class LibPairDataItem:

    def __init__(self, id: str, source_lib: str, target_lib: str, migrations: list[Migration]):
        self.id = id
        self.source_lib = source_lib
        self.target_lib = target_lib
        self._migrations = []
        self._source_program_elements = set()
        self._target_program_elements = set()
        self._all_program_elements = set()
        self._properties = set()
        self._cardinalities = set()
        self._code_changes = []
        self._api_mappings = APIMappingSet()
        for mig in migrations:
            self.add_mig(mig)

    def has_program_elements(self, *pes: str):
        return self._all_program_elements.issuperset(pes)

    def has_properties(self, *props: str):
        return self._properties.issuperset(props)

    def all_program_elements(self):
        return self._all_program_elements

    def properties(self):
        return self._properties

    def cardinalities(self):
        return self._cardinalities

    def is_import_only(self):
        return self.all_program_elements().issubset({IMP, NO_PE})

    @classmethod
    def from_mig(cls, mig: Migration):
        return cls(mig.pair_id, mig.source, mig.target, [mig])

    def add_mig(self, mig: Migration):
        self._migrations.append(mig)
        ccs = mig.code_changes(include_imports=True)
        self._code_changes.append(ccs)

        for cc in ccs:
            self._source_program_elements.update(cc.source_program_elements or {NO_PE})
            self._target_program_elements.update(cc.target_program_elements or {NO_PE})
            if cc.can_have_properties():
                self._properties.update(cc.properties or {NO_PROP})

            if cc.cardinality != Not_Applicable:
                self._cardinalities.add(cc.cardinality)

        self._all_program_elements = self._source_program_elements.union(self._target_program_elements)
        self._api_mappings.merge_all(mig.api_mappings(include_imports=False))  # API mappings cannot be for imports


class LibPairDataSet:
    _index: dict[str, LibPairDataItem]

    def __init__(self):
        self._index = {}

    def load(self):
        for mig in load_migs():
            if mig.pair_id not in self._index:
                self._index[mig.pair_id] = LibPairDataItem.from_mig(mig)
            else:
                self._index[mig.pair_id].add_mig(mig)

        return self

    def __iter__(self):
        return iter(self._index.values())

    def __len__(self):
        return len(self._index)
