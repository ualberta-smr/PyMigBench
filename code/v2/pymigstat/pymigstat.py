from reports.big_combination_stats import big_combination_stats
from reports.code_change_summary import code_change_summary
from reports.data_stats import data_stats
from reports.export_constant_data import export_constant_data
from reports.mig_effort_stats import mig_effort_stats
from reports.api_mapping_stats import program_elements_stats_in_libpairs
from reports.migration_summary import migration_summary
from reports.update_report_data import clean_report_data
from taxonomy.combine_rounds import combine_rounds
from taxonomy.export_yaml import export_yaml

if __name__ == '__main__':
    clean_report_data()
    export_yaml()
    combine_rounds(True, False)
    data_stats()
    export_constant_data()
    program_elements_stats_in_libpairs()
    mig_effort_stats()
    big_combination_stats()
    code_change_summary()
    migration_summary()
