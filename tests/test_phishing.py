import pytest

from src import phishing as p


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


if __name__ == '__main__':
    pytest.main()
