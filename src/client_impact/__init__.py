"""Client impact and responsible-lending analytics."""

from .client_voice import client_voice_summary, write_client_voice_report
from .financial_health import (
	FinancialHealthConfig,
	financial_health_report,
	financial_health_rows,
	financial_health_summary,
	support_review_flags,
	write_financial_health_report,
)
from .generate import SyntheticConfig, generate_dataset, validate_dataset, write_dataset
from .inclusion import (
	inclusion_by_district,
	inclusion_report,
	inclusion_rows,
	inclusion_summary,
	write_inclusion_report,
)
from .indicators import debt_service_ratio, income_change
from .outcomes import (
	client_outcomes,
	outcome_report,
	outcome_summary,
	subgroup_summary,
	write_outcome_report,
)
from .quality import quality_report, write_quality_report
from .uncertainty import (
	bootstrap_median_interval,
	followup_coverage,
	uncertainty_report,
	write_uncertainty_report,
)

__all__ = [
	"SyntheticConfig",
	"FinancialHealthConfig",
	"client_voice_summary",
	"debt_service_ratio",
	"generate_dataset",
	"income_change",
	"inclusion_by_district",
	"inclusion_report",
	"inclusion_rows",
	"inclusion_summary",
	"client_outcomes",
	"bootstrap_median_interval",
	"followup_coverage",
	"financial_health_rows",
	"financial_health_report",
	"financial_health_summary",
	"uncertainty_report",
	"write_uncertainty_report",
	"outcome_summary",
	"outcome_report",
	"quality_report",
	"subgroup_summary",
	"support_review_flags",
	"write_financial_health_report",
	"write_inclusion_report",
	"write_client_voice_report",
	"write_outcome_report",
	"write_quality_report",
	"validate_dataset",
	"write_dataset",
]
