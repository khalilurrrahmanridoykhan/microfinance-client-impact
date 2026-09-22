"""Client impact and responsible-lending analytics."""

from .generate import SyntheticConfig, generate_dataset, validate_dataset, write_dataset
from .indicators import debt_service_ratio, income_change
from .quality import quality_report

__all__ = [
	"SyntheticConfig",
	"debt_service_ratio",
	"generate_dataset",
	"income_change",
	"quality_report",
	"validate_dataset",
	"write_dataset",
]
