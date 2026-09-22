"""Client impact and responsible-lending analytics."""

from .generate import SyntheticConfig, generate_dataset, validate_dataset, write_dataset
from .indicators import debt_service_ratio, income_change
from .outcomes import (
	client_outcomes,
	outcome_report,
	outcome_summary,
	subgroup_summary,
	write_outcome_report,
)
from .quality import quality_report, write_quality_report
from .uncertainty import bootstrap_median_interval, followup_coverage

__all__ = [
	"SyntheticConfig",
	"debt_service_ratio",
	"generate_dataset",
	"income_change",
	"client_outcomes",
	"bootstrap_median_interval",
	"followup_coverage",
	"outcome_summary",
	"outcome_report",
	"quality_report",
	"subgroup_summary",
	"write_outcome_report",
	"write_quality_report",
	"validate_dataset",
	"write_dataset",
]
