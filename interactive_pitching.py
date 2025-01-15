import streamlit as st
import pandas as pd
# import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


url = "https://raw.githubusercontent.com/tacos2718/Interactive-Pitching/refs/heads/main/20241101-Matador%20Field-Private-1_unverified.csv"

data = pd.read_csv(url)
# print(data.head)

st.title("Pitching Report")



################################################################################################


# Filter options for the "Pitcher" column
with st.sidebar:
    st.title('Filters')
    pitchers = data['Pitcher'].dropna().unique()
    selected_pitcher = st.selectbox("Select a Pitcher", ["All"] + list(pitchers))


# Filter the data by the selected pitcher
if selected_pitcher != "All":
    filtered_data = data[data['Pitcher'] == selected_pitcher]
else:
    filtered_data = data



################################################################################################

# Create the Plate Location scatterplot
st.subheader("Scatterplot of Plate Location")
fig, ax = plt.subplots(figsize=(8, 6))
scatter = sns.scatterplot(
    data=filtered_data,
    x="PlateLocSide",
    y="PlateLocHeight",
    hue="TaggedPitchType",
    palette="viridis",
    alpha=0.8
)
ax.set_xlim(-4, 4)
ax.set_ylim(-1, 5)
ax.set_title("Scatterplot: PlateLocHeight vs PlateLocSide")
ax.set_xlabel("PlateLocSide")
ax.set_ylabel("PlateLocHeight")
ax.legend(title="TaggedPitchType", bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
st.pyplot(fig)



################################################################################################

# Pie Chart of "TaggedPitchType"
st.subheader("Distribution of Pitch Type")

# Group and count "TaggedPitchType" for the filtered data

tagged_pitch_counts = (
    filtered_data["TaggedPitchType"]
    .dropna()  # Remove any NaN values
    .value_counts()  # Get counts for each category
    .reset_index()  # Convert to DataFrame
)
# Rename columns explicitly
tagged_pitch_counts.columns = ["TaggedPitchType", "Count"]


# Create the pie chart
fig_pie, ax_pie = plt.subplots(figsize=(6, 6))
ax_pie.pie(
    tagged_pitch_counts["Count"],
    labels=tagged_pitch_counts["TaggedPitchType"],
    autopct='%1.1f%%',
    startangle=90,
    colors=sns.color_palette("pastel", len(tagged_pitch_counts)),
    wedgeprops={"edgecolor": "k"},
)
ax_pie.set_title("Pitch Type Distribution")

# Display the pie chart
st.pyplot(fig_pie)


################################################################################################

# Create the Release Location scatterplot
st.subheader("Scatterplot of Release Location")
fig2, ax2 = plt.subplots(figsize=(8, 6))
scatter2 = sns.scatterplot(
    data=filtered_data,
    x="RelSide",
    y="RelHeight",
    hue="TaggedPitchType",
    palette="viridis",
    alpha=0.8
)
ax2.set_xlim(-4, 4)
ax2.set_ylim(0, 7)
ax2.set_title("Scatterplot: RelHeight vs RelSide")
ax2.set_xlabel("RelSide (ft)")
ax2.set_ylabel("RelHeight (ft)")
ax2.legend(title="TaggedPitchType", bbox_to_anchor=(1.05, 1), loc='upper left')

# Display the plot
st.pyplot(fig2)


################################################################################################

# Table of TaggedPitchType vs PitchCall with Total column
st.subheader("Pitch Call by Pitch Type")

if not filtered_data.empty:
    # Create a pivot table (contingency table)
    table_data = filtered_data.pivot_table(
        index="TaggedPitchType",  # Rows
        columns="PitchCall",     # Columns
        values="Pitcher",        # Use any column to count occurrences
        aggfunc="count",         # Count occurrences
        fill_value=0             # Replace NaN with 0
    )

    # Add a Total column
    table_data["Total"] = table_data.sum(axis=1)
    

    # Display the table using Streamlit
    st.dataframe(table_data)
else:
    st.write("No data available for the selected pitcher.")
