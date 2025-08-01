import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("energy_data_india.csv")

st.title(" Indian Residential Energy Dashboard")

# Sidebar Filters
region = st.sidebar.selectbox("Select Region", ["All"] + sorted(df["Region"].dropna().unique().tolist()))

if region != "All":
    df = df[df["Region"] == region]

st.subheader("Household Energy Consumption Overview")
st.write(df.head())  # Display top 5 records

# Metrics
avg_energy = df["Monthly_Energy_Consumption_kWh"].mean()
total_energy = df["Monthly_Energy_Consumption_kWh"].sum()

st.metric(" Average Monthly Consumption (kWh)", f"{avg_energy:.2f}")
st.metric(" Total Energy Consumption (kWh)", f"{total_energy:.0f}")

# Energy vs Income
st.subheader(" Income vs Energy Consumption")
fig1, ax1 = plt.subplots()
sns.scatterplot(data=df, x="Monthly_Income_INR", y="Monthly_Energy_Consumption_kWh", hue="Region", ax=ax1)
ax1.set_xlabel("Monthly Income (INR)")
ax1.set_ylabel("Monthly Energy Consumption (kWh)")
st.pyplot(fig1)

# Appliance Contribution
st.subheader("🔌 Appliance Usage vs Energy Consumption")
appliances = ["Appliance_AC", "Appliance_Fan", "Appliance_Light", "Fridge", "Washing_Machine", "EV_Charging"]
selected_appliance = st.selectbox("Select Appliance", appliances)

fig2, ax2 = plt.subplots()
sns.barplot(x=df[selected_appliance], y=df["Monthly_Energy_Consumption_kWh"], ax=ax2)

ax2.set_xlabel(f"No. of {selected_appliance.replace('_', ' ')} Appliances")

ax2.set_ylabel("Monthly Energy Consumption (kWh)")
st.pyplot(fig2)

# Smart Recommendations
st.subheader(" Smart Recommendations")
for _, row in df.iterrows():
    if row["Monthly_Energy_Consumption_kWh"] > 250:
        st.warning(f" Household ID {row['Household_ID']}- High usage detected! Recommend switching to solar panels and LED bulbs.")
    elif  row["EV_Charging"] == 1:
        st.info(f" Household ID {row['Household_ID']}- Consider installing a dedicated EV meter for better billing efficiency.")
