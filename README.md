# RC Airplane Flight & Battery Calculator

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)

A comprehensive Python-based command-line tool for RC (Radio-Controlled) airplane hobbyists to estimate flight time and required battery capacity with a high degree of accuracy by modeling real-world physical effects.

This calculator goes beyond simple linear estimates by providing a comparison table that shows how factors like Peukert's Law and battery voltage sag impact your flight performance.

---

## Features

-   **Two Calculation Modes:**
    1.  **Calculate Flight Time:** Input your aircraft and battery specs to see how long you can fly.
    2.  **Calculate Required Battery:** Input your desired flight time to get a recommendation for the minimum battery capacity needed.
-   **Advanced Physics Models:** Instead of a single number, the tool generates a comparison table showing results for four different calculation models:
    -   A simple **Base Model**.
    -   A model including the **Peukert Effect** (efficiency loss at high discharge rates).
    -   A model simulating **Voltage Sag** under load.
    -   A **Combined Model** that provides the most realistic estimate.
-   **Current-Based Input:** Designed for hobbyists who know their system's current draw (in Amps) from using a wattmeter or clamp meter.
-   **Built-in Rules of Thumb:** For users who may not have all the data, the tool's documentation includes helpful estimates for cruise current and max power duration.
-   **ESC Sizing:** Automatically recommends a suitable ESC (Electronic Speed Controller) rating based on your maximum current draw.

---

## Why This Calculator? The Science of Flight Time

A simple flight time calculation (`Time = Battery Capacity / Current Draw`) is often inaccurate because it ignores how batteries and power systems behave in the real world. This tool refines the calculation by considering two key factors:

1.  **Peukert's Law:** A battery's effective capacity decreases as the discharge rate increases. You get fewer usable Amp-hours from your battery when flying at full throttle compared to cruising gently.
2.  **Voltage Sag:** A LiPo battery's voltage drops under load. To maintain the same flight power (`Power = Voltage × Current`), the system must draw more current as the voltage sags. This accelerates battery drain, especially towards the end of the flight.

By modeling these effects, this calculator provides a much more realistic and safe estimate of your aircraft's endurance.

---

## Installation & Usage

No installation is required. You only need Python 3.7+ installed on your system.

1.  **Save the Code:** Save the `rc_airplane_calculator_v4.py` file to a directory on your computer.
2.  **Open a Terminal:** Open a command prompt, PowerShell (Windows), or Terminal (macOS/Linux).
3.  **Navigate to the Directory:** Use the `cd` command to navigate to the folder where you saved the file.
    ```bash
    cd path/to/your/folder
    ```
4.  **Run the Script:** Execute the script using the following command:
    ```bash
    python rc_airplane_calculator_v4.py
    ```
5.  **Follow the Menu:** The script will launch and present a menu. Choose an option and enter the requested values.

---

## Understanding the Inputs

To get the most accurate results, provide the best data you can. Here’s what each input means:

-   **`Battery Capacity (mAh)`:** The advertised capacity of your LiPo battery (e.g., `5000`).
-   **`LiPo Cell Count (S)`:** The cell count of your battery (e.g., `6S`). This determines the system voltage.
-   **`Max Current Draw (Amps)`:** The peak current your power system draws, typically at full throttle. This is best measured with a wattmeter.
-   **`Average Cruise Current (Amps)`:** The current your aircraft draws during stable, level flight, usually between 50-70% throttle.

    > **Rule of Thumb:** If you don't know your cruise current, a reasonable estimate for many sport and trainer aircraft is approximately **40-50% of the max current**. For example, if your max current is `80A`, a good starting estimate for cruise current would be `32A` to `40A`.
    >
    > **Aeronautical Context:** An aircraft's power requirement is dictated by drag. Drag is highest during takeoff and full-throttle vertical climbs due to high "induced drag" from the wings working hard to generate lift. In cruise, the aircraft is at a more efficient angle of attack, minimizing total drag and thus requiring less power (and current) to maintain speed. The 40-50% range often reflects this aerodynamic "sweet spot."

-   **`Duration at Max Current (minutes)`:** The amount of time you expect to spend at full throttle during a typical flight.
    
    > **Rule of Thumb:** If you are unsure, consider the duration of your takeoff sequence. For most sport flyers, this might be a short burst of 5-30 seconds (`0.08` to `0.5` minutes).

-   **`Battery Safety Margin (%)`:** The percentage of battery capacity you want to leave in the pack after landing. It is highly recommended to use **20%-10%** to preserve the health and lifespan of your LiPo batteries. Never discharge a LiPo completely.
-   **`Peukert Exponent`:** A value that describes how battery capacity changes with discharge rate.
    > **Recommendation:** If you don't know this value, simply press **Enter** to use the default of **`1.08`**, which is a conservative and safe estimate for most modern LiPo packs.

---

## Understanding the Output: The Comparison Table

The primary feature of this tool is the comparison table, which shows how each refinement affects the flight time estimate.

| Metric                  | Base Model                                     | + Peukert                                       | + Voltage Sag                                   | Combined Model                                |
| ----------------------- | ---------------------------------------------- | ----------------------------------------------- | ----------------------------------------------- | --------------------------------------------- |
| **What it represents** | An ideal "perfect world" calculation.          | Models efficiency loss at high currents.        | Models the need for more current as voltage drops. | **The most realistic estimate.** |
| **The Physics** | `Time = Capacity / Current`                      | Effective capacity is reduced under high load.  | Power is constant, so `I = P / V`. As `V` drops, `I` must rise. | Both effects are calculated together.         |
| **Expected Result** | The most optimistic (longest) flight time.     | Shorter flight time than Base Model.            | Shorter flight time than Base Model.            | The most conservative (shortest) flight time. |

By looking at the **Combined Model**, you get the safest and most accurate prediction for your real-world flight time.

---

## Contributing

Feedback, bug reports, and pull requests are welcome! If you have ideas for further refinements, feel free to open an issue to discuss them.
