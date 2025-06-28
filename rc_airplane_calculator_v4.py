# -*- coding: utf-8 -*-
"""
RC Aircraft Control battery Estimator

This script calculates the estimated battery capacity required for an electric
RC aircraft's

by lucas-santos Adelphi 2021
"""
# --- Constants for LiPo Battery Characteristics ---
VOLTAGE_NOMINAL_PER_CELL = 3.7 
VOLTAGE_AVERAGE_PER_CELL = 3.6 
DEFAULT_PEUKERT_EXPONENT = 1.08

def get_numeric_input(prompt_message, allow_zero=False):
    """Gets a numeric input from the user, handling potential errors."""
    while True:
        try:
            value = float(input(prompt_message))
            if value > 0 or (allow_zero and value == 0):
                return value
            else:
                print("Error: Please enter a positive number.")
        except ValueError:
            print("Error: Invalid input. Please enter a number.")

def get_lipo_cell_input(prompt_message):
    """Gets a valid LiPo cell count (e.g., '3S', '6S', '12S') from the user."""
    while True:
        try:
            value_str = input(prompt_message).upper()
            if not value_str.endswith('S'):
                print("Error: Invalid format. Use 'S' at the end (e.g., '6S').")
                continue
            
            cell_count = int(value_str[:-1])
            if 3 <= cell_count <= 12:
                return cell_count, value_str
        except (ValueError, IndexError):
            print("Error: Invalid input. Enter a valid cell count (e.g., '6S').")


def calculate_flight_time_comparison():
    """
    Calculates flight time using four different refinement models and displays a comparison table.
    """
    print("\n--- Calculate Flight Time (with Refinement Comparison) ---")
    
    # --- Gather Inputs (Current-based) ---
    battery_capacity_mah = get_numeric_input("Enter battery capacity (mAh): ")
    cells, cells_str = get_lipo_cell_input("Enter LiPo cell count (3S to 12S): ")
    # CHANGED: Ask for current instead of power
    max_current_a = get_numeric_input("Enter max current draw (Amps): ")
    cruise_current_a = get_numeric_input("Enter average cruise current draw (Amps): ")
    max_power_duration_min = get_numeric_input("Enter estimated duration at max current (minutes): ", allow_zero=True)
    safety_margin_percent = get_numeric_input("Enter battery safety margin (% - e.g., 20): ")
    peukert_exponent = get_numeric_input(f"Enter Peukert exponent (or press Enter for default {DEFAULT_PEUKERT_EXPONENT}): ") if input("Do you want to specify a Peukert exponent? (y/n): ").lower() == 'y' else DEFAULT_PEUKERT_EXPONENT

    # --- Pre-calculations ---
    nominal_voltage = cells * VOLTAGE_NOMINAL_PER_CELL
    average_voltage = cells * VOLTAGE_AVERAGE_PER_CELL
    
    # NEW: Calculate power internally from the provided current and nominal voltage
    max_power_w = nominal_voltage * max_current_a
    cruise_power_w = nominal_voltage * cruise_current_a
    
    usable_capacity_ah_nominal = (battery_capacity_mah / 1000) * (1 - safety_margin_percent / 100)
    max_power_duration_h = max_power_duration_min / 60

    # --- Scenario 1: Base Model (Power-based, Nominal Voltage) ---
    # This scenario will reflect the user's direct input, as P/V_nom = (V_nom*I)/V_nom = I
    s1_max_current = max_current_a
    s1_cruise_current = cruise_current_a
    s1_max_power_consumption_ah = s1_max_current * max_power_duration_h
    s1_cruise_capacity_ah = usable_capacity_ah_nominal - s1_max_power_consumption_ah
    s1_cruise_time_min = (s1_cruise_capacity_ah / s1_cruise_current * 60) if s1_cruise_capacity_ah > 0 else 0
    s1_total_time_min = max_power_duration_min + s1_cruise_time_min

    # --- Scenario 2: Base Model + Peukert's Law ---
    s1_total_time_h = s1_total_time_min / 60
    s1_total_ah_consumed = (s1_max_current * max_power_duration_h) + (s1_cruise_current * (s1_cruise_time_min / 60))
    avg_discharge_current = s1_total_ah_consumed / s1_total_time_h if s1_total_time_h > 0 else s1_max_current
    
    one_c_rate = battery_capacity_mah / 1000
    capacity_ratio = (one_c_rate / avg_discharge_current) ** (peukert_exponent - 1) if avg_discharge_current > 0 else 1
    usable_capacity_ah_peukert = usable_capacity_ah_nominal * capacity_ratio
    
    s2_max_power_consumption_ah = s1_max_current * max_power_duration_h
    s2_cruise_capacity_ah = usable_capacity_ah_peukert - s2_max_power_consumption_ah
    s2_cruise_time_min = (s2_cruise_capacity_ah / s1_cruise_current * 60) if s2_cruise_capacity_ah > 0 else 0
    s2_total_time_min = max_power_duration_min + s2_cruise_time_min

    # --- Scenario 3: Base Model + Voltage Sag ---
    s3_max_current = max_power_w / average_voltage
    s3_cruise_current = cruise_power_w / average_voltage
    s3_max_power_consumption_ah = s3_max_current * max_power_duration_h
    s3_cruise_capacity_ah = usable_capacity_ah_nominal - s3_max_power_consumption_ah
    s3_cruise_time_min = (s3_cruise_capacity_ah / s3_cruise_current * 60) if s3_cruise_capacity_ah > 0 else 0
    s3_total_time_min = max_power_duration_min + s3_cruise_time_min
    
    # --- Scenario 4: Combined Model (Peukert + Voltage Sag) ---
    s4_max_power_consumption_ah = s3_max_current * max_power_duration_h
    s4_cruise_capacity_ah = usable_capacity_ah_peukert - s4_max_power_consumption_ah
    s4_cruise_time_min = (s4_cruise_capacity_ah / s3_cruise_current * 60) if s4_cruise_capacity_ah > 0 else 0
    s4_total_time_min = max_power_duration_min + s4_cruise_time_min

    # --- Display Results Table ---
    print("\n" + "="*80)
    print(f" Flight Time Comparison for a {battery_capacity_mah:.0f}mAh {cells_str} LiPo ".center(80, "="))
    print("="*80)
    
    headers = ["Metric", "Base Model", "+ Peukert", "+ Voltage Sag", "Combined Model"]
    print(f"{headers[0]:<20} | {headers[1]:^15} | {headers[2]:^15} | {headers[3]:^15} | {headers[4]:^15}")
    print("-"*80)

    results = {
        "Cruise Time (min)": [s1_cruise_time_min, s2_cruise_time_min, s3_cruise_time_min, s4_cruise_time_min],
        "Total Flight Time (min)": [s1_total_time_min, s2_total_time_min, s3_total_time_min, s4_total_time_min],
    }

    for label, values in results.items():
        print(f"{label:<20} | {values[0]:^15.1f} | {values[1]:^15.1f} | {values[2]:^15.1f} | {values[3]:^15.1f}")
        
    print("-"*80)
    
    # CHANGED: ESC recommendation based on user input current
    recommended_esc = max_current_a * 1.25
    print(f"INFO: Recommended ESC Rating (based on your input): ~{recommended_esc:.0f} A")
    print(f"INFO: Max current can reach ~{s3_max_current:.1f} A due to voltage sag to maintain power.")
    print("="*80 + "\n")


def calculate_battery_capacity():
    """
    Calculates the required battery capacity using the most accurate model (Peukert + Voltage Sag).
    """
    print("\n--- Calculate Required Battery (Advanced Model) ---")
    print("This calculation uses the most precise model to ensure a safe recommendation.")
    
    # Get inputs
    desired_time_min = get_numeric_input("Enter desired total flight time (minutes): ")
    cells, cells_str = get_lipo_cell_input("Enter LiPo cell count (3S to 12S): ")
    # CHANGED: Ask for current instead of power
    max_current_a = get_numeric_input("Enter max current draw (Amps): ")
    cruise_current_a = get_numeric_input("Enter average cruise current draw (Amps): ")
    max_power_duration_min = get_numeric_input("Enter estimated duration at max current (minutes): ", allow_zero=True)
    safety_margin_percent = get_numeric_input("Enter battery safety margin (% - e.g., 20): ")
    peukert_exponent = DEFAULT_PEUKERT_EXPONENT
    
    # NEW: Calculate power internally
    nominal_voltage = cells * VOLTAGE_NOMINAL_PER_CELL
    max_power_w = nominal_voltage * max_current_a
    cruise_power_w = nominal_voltage * cruise_current_a

    # Calculations based on the most demanding model (Voltage Sag)
    average_voltage = cells * VOLTAGE_AVERAGE_PER_CELL
    # The currents used for calculation are derived from power and average voltage
    calc_max_current = max_power_w / average_voltage
    calc_cruise_current = cruise_power_w / average_voltage

    flight_phase_duration_min = desired_time_min - max_power_duration_min
    if flight_phase_duration_min < 0:
        print("\nError: Desired time must be longer than max power duration.")
        return

    # Calculate consumption in Ah
    max_power_consumption_ah = calc_max_current * (max_power_duration_min / 60)
    cruise_consumption_ah = calc_cruise_current * (flight_phase_duration_min / 60)
    total_usable_ah = max_power_consumption_ah + cruise_consumption_ah

    # Estimate average current to apply Peukert's Law in reverse
    avg_current = total_usable_ah / (desired_time_min / 60) if desired_time_min > 0 else calc_max_current
    
    # Reverse Peukert
    one_c_rate_guess = total_usable_ah
    capacity_ratio = (one_c_rate_guess / avg_current) ** (peukert_exponent - 1) if avg_current > 0 else 1
    required_nominal_ah = total_usable_ah / capacity_ratio
    
    # Add safety margin
    final_required_ah = required_nominal_ah / (1 - safety_margin_percent / 100)
    final_required_mah = final_required_ah * 1000

    print("\n" + "="*50)
    print(f"To fly for {desired_time_min:.1f} min with a {cells_str} setup:")
    print(f"Recommended Minimum Battery: {final_required_mah:.0f} mAh")
    print("="*50)


def main():
    """Main function to run the calculator's user interface."""
    print("=========================================================")
    print("=   RC Airplane Flight Calculator (V4 - Current Input)  =")
    print("=========================================================")
    
    while True:
        print("\nChoose an option:")
        print("1: Calculate Flight Time (with comparison table)")
        print("2: Calculate Required Battery (uses most precise model)")
        print("3: Exit")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        if choice == '1':
            calculate_flight_time_comparison()
        elif choice == '2':
            calculate_battery_capacity()
        elif choice == '3':
            print("Exiting calculator. Happy flying!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
