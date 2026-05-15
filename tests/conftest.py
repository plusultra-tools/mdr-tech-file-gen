"""Shared pytest fixtures for mdr-tech-file-gen tests."""
from __future__ import annotations

import pytest

from mdr_techfile.spec import (
    DeviceSpec,
    Iec62304SafetyClass,
    RiskClass,
    SoftwareLifecycle,
    SoupEntry,
)


@pytest.fixture
def samd_class_iia() -> DeviceSpec:
    """Fixture: Class IIa SaMD device (SmartGlucose Predictor)."""
    return DeviceSpec(
        id="SGP-001",
        name="SmartGlucose Predictor v1.0",
        manufacturer="GlucoTech GmbH",
        version="1.0",
        intended_use=(
            "Intended to predict blood glucose level trends in adults (≥18 years) "
            "with Type 1 or Type 2 diabetes mellitus using continuous glucose monitor "
            "readings and patient-reported meal data. Intended for use by the patient "
            "under the supervision of a healthcare professional. Not intended for acute "
            "hypoglycaemia management or insulin dosing decisions."
        ),
        intended_users=["healthcare professional", "layperson (patient)"],
        intended_environments=["home care", "ambulatory care"],
        risk_class=RiskClass.IIA,
        classification_rules_applied=["Rule 11"],
        software=True,
        lifecycle=SoftwareLifecycle(
            iec62304_safety_class=Iec62304SafetyClass.B,
            version_control_system="git 2.x",
            change_control_sop="SOP-CC-001 v2.0",
        ),
        soup_register=[
            SoupEntry(
                name="numpy",
                version="1.26.4",
                purpose="Numerical array operations for glucose trend calculation.",
                anomaly_list_reviewed=True,
            ),
            SoupEntry(
                name="scikit-learn",
                version="1.4.1",
                purpose="Machine learning model training and inference.",
                anomaly_list_reviewed=False,
            ),
        ],
        contraindications=[
            "Not for use in patients under 18 years of age.",
            "Not validated for use during pregnancy.",
            "Not a substitute for clinical blood glucose measurement.",
        ],
        clinical_claims=[
            "Predicts blood glucose trends ≥30 minutes ahead "
            "with MARD ≤15% in the target population.",
        ],
        notified_body="TÜV SÜD",
        udi_di=None,
        basic_udi_di=None,
    )


@pytest.fixture
def hardware_class_i() -> DeviceSpec:
    """Fixture: Class I hardware device (non-software, simple)."""
    return DeviceSpec(
        id="HW-001",
        name="SimpleThermometer v2",
        manufacturer="MedTools S.L.",
        version="2.0",
        intended_use=(
            "Non-invasive oral thermometer for measurement of body temperature in "
            "adults and children. For use by laypersons in home care settings."
        ),
        intended_users=["layperson"],
        intended_environments=["home care"],
        risk_class=RiskClass.I,
        classification_rules_applied=["Rule 1"],
        software=False,
        lifecycle=None,
        contraindications=[],
        clinical_claims=[],
    )


@pytest.fixture
def samd_class_iii() -> DeviceSpec:
    """Fixture: Class III SaMD device (high risk)."""
    return DeviceSpec(
        id="HRS-001",
        name="CardioAlert v1.0",
        manufacturer="HeartSafe BV",
        version="1.0",
        intended_use=(
            "Software intended to detect life-threatening cardiac arrhythmias from "
            "real-time ECG data and trigger emergency alerts. For use by healthcare "
            "professionals in hospital ICU settings."
        ),
        intended_users=["healthcare professional"],
        intended_environments=["hospital ICU"],
        risk_class=RiskClass.III,
        classification_rules_applied=["Rule 11"],
        software=True,
        lifecycle=SoftwareLifecycle(
            iec62304_safety_class=Iec62304SafetyClass.C,
        ),
        contraindications=["Not for use in patients with permanent pacemakers."],
        clinical_claims=[
            "Detects ventricular fibrillation with sensitivity ≥99% and specificity ≥95%.",
        ],
        notified_body="BSI Group",
    )
