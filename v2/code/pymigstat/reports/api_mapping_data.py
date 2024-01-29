from itertools import product

from datamodels.loaders import load_api_mappings
from reports.update_report_data import percent
from taxonomy.constants import *


class APIMappingDataItem:

    def __init__(self, source_pe: str, target_pe: str):
        self.source_pe = source_pe
        self.target_pe = target_pe
        self.lib_pairs: set[str] = set()
        self.properties_api_mappings: dict[str, set[str]] = {prop: set() for prop in ALL_PROPS_WITH_NO_PROPS}
        self.mappings: set[str] = set()


class APIMappingData:
    def __init__(self):
        dims = ALL_PES + [NO_PE, TOTAL]
        pe_pair_data = {(src, tgt): APIMappingDataItem(src, tgt) for src, tgt in product(dims, dims)}
        cardinality_data = {cardinality: 0 for cardinality in ALL_CARDINALITIES}

        self._pe_pair_data: dict[any, APIMappingDataItem] = pe_pair_data
        self._cardinality_data = cardinality_data
        self._non_function_libpairs = set()

        """
        Number of mappings that can have properties.
        Excludes imports and mappings that only removes only adds
        """
        self._mapping_applies_property_count = 0

        self.load()

    def load(self):

        for mapping in load_api_mappings():
            mapping_id = mapping.mapping_id
            all_program_elements = set(mapping.source_program_elements + mapping.target_program_elements)
            is_import = (IMP in all_program_elements)
            is_addition_or_removal = (not mapping.source_program_elements or not mapping.target_program_elements)

            if not is_import:
                self._cardinality_data[mapping.cardinality] += 1

            applies_prop = not (is_import or is_addition_or_removal)
            if applies_prop:
                self._mapping_applies_property_count += 1

            if all_program_elements.intersection(NON_FUNC_OR_IMP_PES):
                self._non_function_libpairs.add(mapping.pair_id)

            for s_pe, t_pe in product(mapping.source_program_elements or {NO_PE},
                                      mapping.target_program_elements or {NO_PE}):
                src_tgt_obj = self._pe_pair_data[(s_pe, t_pe)]
                src_total_obj = self._pe_pair_data[(s_pe, TOTAL)]
                tgt_total_obj = self._pe_pair_data[(TOTAL, t_pe)]
                total_total_obj = self._pe_pair_data[(TOTAL, TOTAL)]

                if applies_prop:
                    for prop in mapping.properties:
                        src_tgt_obj.properties_api_mappings[prop].add(mapping_id)
                        src_total_obj.properties_api_mappings[prop].add(mapping_id)
                        tgt_total_obj.properties_api_mappings[prop].add(mapping_id)
                        total_total_obj.properties_api_mappings[prop].add(mapping_id)

                src_tgt_obj.mappings.add(mapping_id)
                src_total_obj.mappings.add(mapping_id)
                tgt_total_obj.mappings.add(mapping_id)
                total_total_obj.mappings.add(mapping_id)

                src_tgt_obj.lib_pairs.add(mapping.pair_id)
                src_total_obj.lib_pairs.add(mapping.pair_id)
                tgt_total_obj.lib_pairs.add(mapping.pair_id)
                total_total_obj.lib_pairs.add(mapping.pair_id)

            print()

    def lip_pair_count(self, source_pe, target_pe):
        return len(self._pe_pair_data[(source_pe, target_pe)].lib_pairs)

    def prop_count(self, source_pe, target_pe, prop):
        return len(self._pe_pair_data[(source_pe, target_pe)].properties_api_mappings[prop])

    def cardinality_count(self, cardinality):
        return self._cardinality_data[cardinality]

    def api_mapping_count(self, source_pe, target_pe):
        return len(self._pe_pair_data[(source_pe, target_pe)].mappings)

    def prop_percent(self, source_pe, target_pe, prop):
        prop_count = self.prop_count(source_pe, target_pe, prop)
        total_api_mappings = self.api_mapping_count(source_pe, target_pe)
        if source_pe == TOTAL and target_pe == TOTAL:
            mapping_count = self._mapping_applies_property_count
        elif source_pe == TOTAL and target_pe != TOTAL:
            mapping_count = total_api_mappings - self.api_mapping_count(NO_PE, target_pe)
        elif source_pe != TOTAL and target_pe == TOTAL:
            mapping_count = total_api_mappings - self.api_mapping_count(source_pe, NO_PE)
        else:
            mapping_count = total_api_mappings

        return percent(prop_count, mapping_count)

    def non_function_libpairs_count(self):
        return len(self._non_function_libpairs)
