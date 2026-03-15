import streamlit as st
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart Factory Sustainability Dashboard", layout="wide")

# Load ML model
model = joblib.load("metal_model.pkl")

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Factory Overview",
        "MetalGuard AI",
        "Energy Waste Analyzer",
        "Water Waste Analyzer",
        "Carbon Emission Analyzer",
        "AI Model Information",
        "Sustainability Report"
    ]
)

# ---------------------------------------------------
# FACTORY OVERVIEW
# ---------------------------------------------------

if page == "Factory Overview":

    st.title("Smart Textile Factory Monitoring Dashboard")

    st.subheader("Live Machine Sensor Monitoring (Simulated)")

    col1, col2, col3, col4 = st.columns(4)

    # Smooth realistic sensor values
    temp = np.random.normal(45, 3)
    vibration = np.random.normal(0.5, 0.1)
    power = np.random.normal(850, 80)
    humidity = np.random.normal(65, 5)

    temp = round(temp)
    vibration = round(vibration, 2)
    power = round(power)
    humidity = round(humidity)

    col1.metric("Machine Temperature", f"{temp} °C")
    col2.metric("Vibration Level", f"{vibration}")
    col3.metric("Power Consumption", f"{power} W")
    col4.metric("Humidity", f"{humidity} %")

    # Temperature alert logic
    if temp < 45:
        st.success("🟢 Machine Temperature Normal")
    elif temp < 55:
        st.warning("🟡 Temperature Slightly High")
    else:
        st.error("🔴 Temperature Critical")

    sensor_data = pd.DataFrame({
        "Temperature": [temp],
        "Vibration": [vibration],
        "Power": [power],
        "Humidity": [humidity]
    })

    fig, ax = plt.subplots()
    ax.bar(sensor_data.columns, sensor_data.iloc[0])
    ax.set_title("Live Machine Sensor Signals")
    st.pyplot(fig)

# ---------------------------------------------------
# METAL ANALYSIS
# ---------------------------------------------------

elif page == "MetalGuard AI":

    st.title("MetalGuard AI – Predictive Maintenance")

    signal = st.slider("Signal Strength", 0.0, 1.0, 0.6)
    magnetic = st.slider("Magnetic Response", 0.0, 1.0, 0.5)
    resistance = st.slider("Electrical Resistance", 5, 25, 12)
    frequency = st.slider("Frequency", 70, 200, 120)
    temp = st.slider("Temperature", 20, 50, 30)

    if st.button("Analyze Machine Component"):

        data = pd.DataFrame(
            [[signal, magnetic, resistance, frequency, temp]],
            columns=["signal", "magnetic", "resistance", "frequency", "temp"]
        )

        prediction = model.predict(data)

        st.success("Material Type Detected: " + prediction[0])

        if resistance > 18:
            st.error("🔴 Possible Corrosion Risk")
        elif signal > 0.9:
            st.warning("🟡 Micro Crack Risk")
        elif frequency > 160:
            st.warning("🟡 Material Fatigue Detected")
        else:
            st.success("🟢 Component Condition Normal")

        health = int(signal * 100)
        st.metric("Component Health Score", str(health) + "%")

# ---------------------------------------------------
# ENERGY ANALYZER
# ---------------------------------------------------

elif page == "Energy Waste Analyzer":

    st.title("Factory Energy Efficiency Analysis")

    total_power = st.number_input("Total Power Consumption (W)", 1000)
    useful_power = st.number_input("Useful Power (W)", 700)
    hours = st.slider("Operating Hours", 1, 24, 8)

    if st.button("Calculate Energy Waste"):

        total_energy = (total_power * hours) / 1000
        useful_energy = (useful_power * hours) / 1000

        waste = total_energy - useful_energy
        waste_percent = (waste / total_energy) * 100

        st.metric("Total Energy Used", str(round(total_energy, 2)) + " kWh/day")
        st.metric("Energy Waste", str(round(waste, 2)) + " kWh/day")

        if waste_percent < 20:
            st.success("🟢 Energy Efficiency Good")
        elif waste_percent < 40:
            st.warning("🟡 Moderate Energy Waste")
        else:
            st.error("🔴 High Energy Waste Detected")

        fig, ax = plt.subplots()
        ax.bar(["Useful", "Waste"], [useful_energy, waste])
        ax.set_title("Energy Usage Distribution")
        st.pyplot(fig)

# ---------------------------------------------------
# WATER ANALYZER
# ---------------------------------------------------

elif page == "Water Waste Analyzer":

    st.title("Water Usage Efficiency")

    current_water = st.number_input("Current Water Usage (L/day)", 10000)
    new_water = st.number_input("New Machine Water Usage (L/day)", 6000)
    machines = st.number_input("Number of Machines", 5)
    hours = st.slider("Operating Hours", 1, 24, 8)

    if st.button("Analyze Water Usage"):

        total_current = current_water * machines * hours / 8
        total_new = new_water * machines * hours / 8

        saved = total_current - total_new

        st.metric("Current Usage", str(round(total_current)) + " L/day")
        st.metric("New Usage", str(round(total_new)) + " L/day")
        st.metric("Water Saved", str(round(saved)) + " L/day")

        if saved > 5000:
            st.success("🟢 Excellent Water Savings")
        elif saved > 2000:
            st.warning("🟡 Moderate Water Improvement")
        else:
            st.error("🔴 Water Efficiency Low")

        fig, ax = plt.subplots()
        ax.bar(["Current", "New"], [total_current, total_new])
        ax.set_title("Water Consumption Comparison")
        st.pyplot(fig)

# ---------------------------------------------------
# CARBON ANALYZER
# ---------------------------------------------------

elif page == "Carbon Emission Analyzer":

    st.title("Carbon Emission Monitoring")

    power = st.number_input("Machine Power (kW)", 50.0)
    new_power = st.number_input("New Machine Power (kW)", 30.0)
    hours = st.slider("Operating Hours", 1, 24, 8)
    machines = st.number_input("Machines", 5)
    factor = st.number_input("CO2 factor", 0.475)

    if st.button("Calculate Carbon Emission"):

        current_energy = power * hours * machines
        new_energy = new_power * hours * machines

        current_carbon = current_energy * factor
        new_carbon = new_energy * factor
        saved = current_carbon - new_carbon

        st.metric("Current CO2", str(round(current_carbon, 2)) + " kg/day")
        st.metric("New CO2", str(round(new_carbon, 2)) + " kg/day")
        st.metric("CO2 Saved", str(round(saved, 2)) + " kg/day")

        if saved > 50:
            st.success("🟢 Strong CO₂ Reduction")
        elif saved > 20:
            st.warning("🟡 Moderate CO₂ Reduction")
        else:
            st.error("🔴 High Emissions Remaining")

        fig, ax = plt.subplots()
        ax.bar(["Current", "New"], [current_carbon, new_carbon])
        ax.set_title("Carbon Emissions Comparison")
        st.pyplot(fig)

# ---------------------------------------------------
# AI MODEL INFO
# ---------------------------------------------------

elif page == "AI Model Information":

    st.title("AI Model Information")

    st.write("Algorithm: Random Forest Classifier")
    st.write("Dataset: Synthetic machine sensor dataset (1000 rows)")
    st.write("Features used for prediction:")
    st.write("- Signal Strength")
    st.write("- Magnetic Response")
    st.write("- Electrical Resistance")
    st.write("- Frequency")
    st.write("- Temperature")

# ---------------------------------------------------
# FINAL REPORT
# ---------------------------------------------------

elif page == "Sustainability Report":

    st.title("Factory Sustainability Impact Summary")

    energy_saved = np.random.randint(50, 120)
    water_saved = np.random.randint(5000, 15000)
    carbon_saved = np.random.randint(40, 90)
    cost_saved = np.random.randint(200000, 500000)

    st.metric("Annual Energy Saved", str(energy_saved) + " MWh")
    st.metric("Annual Water Saved", str(water_saved) + " L")
    st.metric("CO2 Reduced", str(carbon_saved) + " tons")
    st.metric("Cost Savings", "₹" + str(cost_saved))

    fig, ax = plt.subplots()
    ax.bar(
        ["Energy", "Water", "CO2", "Cost"],
        [energy_saved, water_saved, carbon_saved, cost_saved]
    )
    ax.set_title("Factory Sustainability Impact")
    st.pyplot(fig)