import os
import sys

import pytest

# Add parent directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import src.phishing as p


def test_employee_click_loss():
    # Test that output has correct format
    result = p.employee_click_loss(n_days=30,
                                   n_phishing_emails_per_week=5,
                                   click_rate=0.1,
                                   loss_per_click=100,
                                   random_seed=42)
    assert isinstance(result, dict)
    assert "time_intervals" in result
    assert "event_times" in result
    assert "event_days" in result
    assert "click_rates" in result
    assert "emails_opened" in result
    assert "loss" in result

    # Test that loss is 0 when click rate is 0
    result = p.employee_click_loss(n_days=30,
                                   n_phishing_emails_per_week=5,
                                   click_rate=0,
                                   loss_per_click=100,
                                   random_seed=42)
    assert len(result["emails_opened"]) == 0
    assert result["loss"] == 0

    # Test that loss is maximal when click rate is 1
    result = p.employee_click_loss(n_days=30,
                                   n_phishing_emails_per_week=5,
                                   click_rate=1,
                                   loss_per_click=100,
                                   random_seed=42)
    assert len(result["emails_opened"]) == len(result["event_days"])
    assert result["loss"] == len(result["event_days"]) * 100


def test_company_click_loss():
    result = p.company_click_loss(n_employees=10,
                                  n_days=30,
                                  n_phishing_emails_per_week=5,
                                  click_rate=1,
                                  loss_per_click=100,
                                  random_seed=42,
                                  n_simulations=100)
    assert isinstance(result, dict)
    assert "company_loss" in result
    assert "plot" in result
    assert len(result["company_loss"]) == 100


if __name__ == '__main__':
    pytest.main()
