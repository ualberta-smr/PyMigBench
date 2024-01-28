from datamodels.loaders import load_migs
from latex.utils import format_int, escape
from reports.update_report_data import update_report_data, percent


def export_constant_data():
    v2_mig_count = 0
    v2_cc_count = 0
    v2_repos = set()
    v2_lps = set()
    v2_libs = set()
    v2_domains = set()
    for mig in load_migs():
        v2_mig_count += 1
        v2_cc_count += len(mig.code_changes(include_imports=True))
        v2_repos.add(mig.repo)
        v2_lps.add(mig.pair_id)
        v2_libs.add(mig.source)
        v2_libs.add(mig.target)
        v2_domains.add(mig.domain)

    v1_mig_count = 75
    data = {
        "candidateSalmMigs": "1,269",
        "libPairsWithSameImportNameCount": "2",
        "VOneCCCount": "375",
        "VOneMigCount": str(v1_mig_count),
        "VOneRepoCount": "57",
        "VOneLPCount": "34",
        "VOneLibCount": "55",
        "VOneDomainCount": "11",
        "VTwoCCCount": format_int(v2_cc_count),
        "VTwoMigCount": format_int(v2_mig_count),
        "VTwoRepoCount": format_int(len(v2_repos)),
        "VTwoLPCount": format_int(len(v2_lps)),
        "VTwoLibCount": format_int(len(v2_libs)),
        "VTwoDomainCount": format_int(len(v2_domains)),
    }

    # data copied from spreadsheet
    data.update({
        "RoundOneMigCount": format_int(13),
        "RoundTwoMigCount": format_int(19),
        "RoundThreeMigCount": format_int(20),
        "RoundFourMigCount": format_int(259),
        "RoundOneCCCount": format_int(78),
        "RoundTwoCCCount": format_int(186),
        "RoundThreeCCCount": format_int(87),
        "RoundFourCCCount": format_int(1233),
        "RoundOneRepoCount": format_int(13),
        "RoundTwoRepoCount": format_int(19),
        "RoundThreeRepoCount": format_int(20),
        "RoundFourRepoCount": format_int(249),
        "RoundOneLPCount": format_int(12),
        "RoundTwoLPCount": format_int(14),
        "RoundThreeLPCount": format_int(12),
        "RoundFourLPCount": format_int(116),
        "RoundOneLibCount": format_int(21),
        "RoundTwoLibCount": format_int(23),
        "RoundThreeLibCount": format_int(24),
        "RoundFourLibCount": format_int(174),
        "RoundOneDomainCount": format_int(3),
        "RoundTwoDomainCount": format_int(7),
        "RoundThreeDomainCount": format_int(9),
        "RoundFourDomainCount": format_int(24),
    })

    data.update({
        "RequiredSALMSampleSize": format_int(296),
        "ActualSALMSampleSize": format_int(311),
        "SALMLabeledDomainPercent": escape("100%"),
        "SALMLabeledLPPercent": percent(131, 199)
    })
    # the below data can be generated using filter_migration_data.py file
    data.update({
        "SALMTotalMigCount": format_int(1559),
        "SALMTotalRepoCount": "1,291",
        "SALMTotalLPCount": "199",
        "SALMTotalLibCount": "265",
        "SALMTotalDomainCount": "25",
        "GrandTotalMigCount": "1,634",
        "GrandTotalRepoCount": "1,338",
        "GrandTotalLPCount": "224",
        "GrandTotalLibCount": "296",
        "GrandTotalDomainCount": "36"
    })

    update_report_data(data)


if __name__ == '__main__':
    export_constant_data()
