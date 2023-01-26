from core.Constants import MigrationKey, LibPairKey
from db.Db import DataItem
from query.Query import Query
from query.Result import Result, ResultDisplayOption


class Summary(Query):
    def run(self):
        migs: list[DataItem] = self.db.get_list(MigrationKey)
        all_lib_pairs: list[DataItem] = self.db.get_list(LibPairKey)
        sources = {lp["source"] for lp in all_lib_pairs}
        targets = {lp["target"] for lp in all_lib_pairs}
        libs = sources.union(targets)
        domains = {lp["domain"] for lp in all_lib_pairs}
        repos = {mg["repo"] for mg in migs}
        commits = {mg["commit"] for mg in migs}
        lib_pairs_having_migs = {mg["pair_id"] for mg in migs}

        migs_having_code_changes = set()
        lib_pairs_having_code_changes = set()
        repos_having_code_changes = set()
        commits_having_code_changes = set()

        file_count = 0
        segments_count = 0
        for mg in migs:
            cc_in_mig = len(mg["code_changes"])
            if cc_in_mig:
                migs_having_code_changes.add(mg["id"])
                lib_pairs_having_code_changes.add(mg["pair_id"])
                repos_having_code_changes.add(mg["repo"])
                commits_having_code_changes.add(mg["commit"])
                file_count += cc_in_mig
                segments_count += sum(len(cc["lines"]) for cc in mg["code_changes"])

        result = {
            "analogous library pairs": len(all_lib_pairs),
            "unique libraries": len(libs),
            "unique source libraries": len(sources),
            "unique target libraries": len(targets),
            "unique library domains": len(domains),
            "migrations": len(migs),
            "client repositories having migrations": len(repos),
            "library pairs having migrations": len(lib_pairs_having_migs),
            "migration commits": len(commits),
            "migrations having code changes": len(migs_having_code_changes),
            "library pairs having code changes": len(lib_pairs_having_code_changes),
            "client repositories having code changes": len(repos_having_code_changes),
            "commits having code changes": len(commits_having_code_changes),
            "modified files": file_count,
            "modified code segments": segments_count
        }

        return Result([result], ResultDisplayOption.DATA_ONLY)
