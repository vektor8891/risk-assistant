# Estimated loss due to clicking on phishing emails for a single employee
def employee_click_loss(n_days, n_phishing_emails_per_week, click_rate, loss_per_click, random_seed=None):
    import numpy as np
    import random as rn

    # Check inputs
    assert n_days > 0, "Days must be positive"
    assert n_phishing_emails_per_week >= 0, "Phishing emails must not be negative"
    assert click_rate >= 0, "Click rate must not be negative"
    assert click_rate <= 1, "Click rate must not be greater than 1"
    assert loss_per_click >= 0, "Loss per click must not be negative"

    # Set the random seed if provided
    if random_seed is not None:
        np.random.seed(random_seed)

    # Define the parameters for the exponential distribution
    lambda_ = n_phishing_emails_per_week / 7  # convert rate to days

    # Generate the time intervals between phishing emails
    time_intervals = np.random.exponential(scale=1 / lambda_, size=int(lambda_ * n_days * 1.1))

    # Calculate the email arrival times as the cumulative sum of time intervals
    event_times = np.cumsum(time_intervals)

    # Select those event times that are within the time horizon
    valid_times = [event_time for event_time in event_times if event_time <= n_days]

    # Calculate which days the emails arrived
    event_days = np.round(valid_times).astype(int)

    # Replicate probabilities
    click_rates = np.full(len(event_days), click_rate)

    # Select which emails the employee opened
    emails_opened = [event_day for event_day, click_rate in zip(event_days, click_rates) if rn.random() < click_rate]

    # Calculate loss
    loss = len(emails_opened) * loss_per_click

    return {"time_intervals": time_intervals, "event_times": event_times, "event_days": event_days,
            "click_rates": click_rates, "emails_opened": emails_opened, "loss": loss}


# Simulate total loss due to clicking on phishing emails for the company
def company_click_loss(n_employees, n_days, n_phishing_emails_per_week, click_rate, loss_per_click, n_simulations,
                       random_seed=None):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker

    # Check inputs
    assert n_employees > 0, "Employee number must be positive"

    # Calculate total loss
    company_loss = []
    for simulation in range(n_simulations):
        total_loss = 0
        for employee in range(n_employees):
            employee_loss = employee_click_loss(n_days=n_days, n_phishing_emails_per_week=n_phishing_emails_per_week,
                                                click_rate=click_rate, loss_per_click=loss_per_click,
                                                random_seed=random_seed)
            total_loss += employee_loss['loss']
        company_loss.append(total_loss)

    # Plot histogram
    fig = plt.figure()
    plt.hist(company_loss)
    plt.xlabel('Total loss (USD)')
    plt.ylabel('Frequency')
    plt.title('Phishing Risk Simulation')

    # Show loss in thousands or millions
    def millions_formatter(x, pos):
        return f'{x / 1_000_000:.1f}M'

    def thousands_formatter(x, pos):
        return f'{x / 1_000:.0f}K'

    if max(company_loss) > 1e6:
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(millions_formatter))
    else:
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(thousands_formatter))

    return {"company_loss": company_loss, "plot": fig}


# show widgets


# show interactive widgets for user
def show_widgets_notebook():
    import ipywidgets as widgets
    import IPython.display as display
    import matplotlib.pyplot as plt

    # Custom CSS styling for the loader
    loader_style = """
    <style>
    .loader {
      border: 16px solid #f3f3f3;
      border-top: 16px solid #3498db;
      border-radius: 50%;
      width: 120px;
      height: 120px;
      animation: spin 2s linear infinite;
      margin: auto;
      margin-top: 20px;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    </style>
    """

    # Create inputs
    style = {'description_width': 'initial'}
    employee_input = widgets.IntText(description='Employees:', value=100, style=style)
    years_input = widgets.IntSlider(description='Time horizon (years):', min=1, max=10, value=1, style=style)
    phishing_input = widgets.IntSlider(description='Phishing emails per week:', min=1, max=10, value=1, style=style)
    click_rate_input = widgets.IntSlider(description='Click rate (%):', min=0, max=100, value=10, step=5, style=style)
    loss_per_click_input = widgets.IntText(description='Loss per click (USD):', value=1000, style=style)

    # Add buttons
    button_run = widgets.Button(description='Run Simulation', button_style='info')
    button_restart = widgets.Button(description='Restart', button_style='danger')

    def button_run_callback(b):
        loader = display.HTML('<div class="loader"></div>')
        display.display(loader)
        company_loss = company_click_loss(n_employees=employee_input.value, n_days=years_input.value * 365,
                                          n_phishing_emails_per_week=phishing_input.value,
                                          click_rate=click_rate_input.value / 100,
                                          loss_per_click=loss_per_click_input.value, n_simulations=1000)
        display.clear_output()
        print(f"employees:       {employee_input.value}")
        print(f"time horizon:    {years_input.value} years")
        print(f"phishing emails: {phishing_input.value}/week/employee")
        print(f"click rate:      {click_rate_input.value}%")
        print(f"loss per click:  {loss_per_click_input.value} USD")
        display.display(button_restart)
        plt.show(company_loss["plot"])

    def button_restart_callback(b):
        display.clear_output()
        display.display(display.HTML(loader_style), employee_input, years_input, phishing_input, click_rate_input,
                        loss_per_click_input, button_run)

    button_run.on_click(button_run_callback)
    button_restart.on_click(button_restart_callback)

    # Display the input widgets
    display.display(display.HTML(loader_style), employee_input, years_input, phishing_input, click_rate_input,
                    loss_per_click_input, button_run)


def show_widgets_lab():
    import ipywidgets as widgets
    import IPython.display as display
    import matplotlib.pyplot as plt

    global loader_style
    global employee_input
    global years_input
    global phishing_input
    global click_rate_input
    global loss_per_click_input

    output = widgets.Output()

    style = {'description_width': 'initial'}
    employee_input = widgets.IntText(description='Employees:', value=100, style=style)
    years_input = widgets.IntSlider(description='Time horizon (years):', min=1, max=10, value=1, style=style)
    phishing_input = widgets.IntSlider(description='Phishing emails per week:', min=1, max=10, value=1, style=style)
    click_rate_input = widgets.IntSlider(description='Click rate (%):', min=0, max=100, value=10, step=5, style=style)
    loss_per_click_input = widgets.IntText(description='Loss per click (USD):', value=1000, style=style)

    def print_loss(_):
        with output:
            display.clear_output()
            print("Simulation running. Please wait...")
            company_loss = company_click_loss(n_employees=employee_input.value, n_days=years_input.value * 365,
                                              n_phishing_emails_per_week=phishing_input.value,
                                              click_rate=click_rate_input.value / 100,
                                              loss_per_click=loss_per_click_input.value, n_simulations=1000)
            display.clear_output()

            plt.show(company_loss["plot"])

    button = widgets.Button(description='Run Simulation', button_style='info')
    button.on_click(print_loss)

    display.display(employee_input)
    display.display(years_input)
    display.display(phishing_input)
    display.display(click_rate_input)
    display.display(loss_per_click_input)
    display.display(button)
    display.display(output)
