import pandas as pd
from matplotlib import pyplot as plt

from complexity import MigLOC, NumAPIs, UniqueAPIs, UniqueMappings
from complexity.num_changes import NumChanges
from config import config
from datamodels.loaders import load_migs
from reports.update_report_data import update_report_data


class MigSizeStats:
    def __init__(self):
        self.mig_loc = MigLOC(False)
        self.num_apis = NumAPIs(False)
        self.num_changes = NumChanges(False)
        self.unique_apis = UniqueAPIs(False)
        self.unique_mappings = UniqueMappings(False)
        self.all_metrics = [
            self.mig_loc,
            self.num_apis,
            self.num_changes,
            self.unique_apis,
            self.unique_mappings,
        ]

        self.bar_metrics = self.all_metrics[:5]

        migs = list(mig for mig in load_migs() if not mig.is_import_only())
        results = {metric.name(): pd.DataFrame(metric.calculate(mig) for mig in migs) for metric in self.all_metrics}
        self.results: dict[str, pd.DataFrame] = results

        summary = {}
        for m in self.bar_metrics:
            metric_name = m.name()
            values = self.results[metric_name][m.key_property()]
            summary[f"{metric_name}Min"] = "{0:.0f}".format(values.min())
            summary[f"{metric_name}FirstQuartile"] = "{0:.0f}".format(values.quantile(.25))
            summary[f"{metric_name}Median"] = "{0:.0f}".format(values.quantile(.50))
            summary[f"{metric_name}ThirdQuartile"] = "{0:.0f}".format(values.quantile(.75))
            summary[f"{metric_name}Max"] = "{0:.0f}".format(values.max())
            summary[f"{metric_name}Mean"] = "{0:.0f}".format(values.mean())

        self.summary = summary

    def export_latex(self):
        update_report_data(self.summary)
        return self

    def export_csv(self):
        m_names = [m.name() for m in self.all_metrics]
        results = [self.results[m_name].rename(columns={
            "source": "source " + m_name,
            "target": "target " + m_name,
            "total": "total " + m_name}) for m_name in m_names
        ]

        merged = pd.merge(results[0], results[1], on='mig')
        for i in range(2, len(m_names)):
            merged = pd.merge(merged, results[i], on='mig')
            print(merged.columns)
        merged.to_csv(config.report_dir / "effort.csv", index=False)
        return self

    def bars(self, save_fig=False):
        fig, axs = plt.subplots(ncols=5, figsize=(12, 3))
        self._bars_for_metric(axs[0], self.mig_loc)
        self._bars_for_metric(axs[1], self.num_apis)
        self._bars_for_metric(axs[2], self.num_changes)
        self._bars_for_metric(axs[3], self.unique_apis)
        self._bars_for_metric(axs[4], self.unique_mappings)
        plt.tight_layout()
        if save_fig:
            plt.savefig(config.paper_dir / "img" / "charts" / "dev-effort-bar.pdf")

        plt.show()
        return self

    def _bars_for_metric(self, ax, m):
        m_name = m.name()
        chart_data = self.results[m_name].sort_values(m.key_property())
        self._show_summary_in_chart(ax, m_name)
        if len(m.properties()) > 1:
            colors = ["red", "green"]
            chart_data = chart_data[["source", "target"]]
            legend = True
        else:
            colors = ["blue"]
            legend = False
        chart_data.plot(kind="bar", logy=False, width=1, ax=ax, stacked=True, color=colors, legend=legend)
        ax.set_xticks([])
        ax.set_title(m_name)

    def _show_summary_in_chart(self, ax, m_name):
        median = self.summary[f"{m_name}Median"]
        mean = self.summary[f"{m_name}Mean"]
        ax.set_xlabel(f"median: {median}, mean: {mean}")

    def _violin_for_metric(self, ax, m):
        m_name = m.name()
        self._show_summary_in_chart(ax, m_name)
        m_data = self.results[m_name][m.key_property()]
        # m_data = m_data[np.abs(stats.zscore(m_data)) < 3]
        ax.violinplot(m_data, showextrema=True)
        ax.set_xticks([])
        # ax.set_xticklabels([f"min={m_data.min()} \n median={m_data.median()}\n max={m_data.max()}", ])
        ax.set_title(m_name)

    def violin(self):
        fig, axs = plt.subplots(ncols=5, figsize=(12, 3.5))
        fig.subplots_adjust(wspace=0.25)
        for i, metric in enumerate(self.all_metrics):
            self._violin_for_metric(axs[i], metric)


        plt.tight_layout()
        plt.savefig(config.paper_dir / "img" / "charts" / "dev-effort-violin.pdf")
        plt.show()
        return self


def mig_effort_stats():
    MigSizeStats().export_csv().export_latex().violin()


if __name__ == '__main__':
    mig_effort_stats()
