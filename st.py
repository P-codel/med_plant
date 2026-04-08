import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("Book3.csv")

# Title
st.title("🌿 Medicinal Plant Recommendation System")

st.markdown("This app helps you explore medicinal plants and their uses based on diseases and phytochemicals.")

# Sidebar
st.sidebar.header("Filter Options")

# Disease selection
disease = st.sidebar.selectbox("Select Disease", df["Disease"].unique())

# Filter data
filtered_df = df[df["Disease"] == disease]

# Show recommendations
st.subheader(f"🌱 Plants for {disease}")
st.dataframe(filtered_df)

# Plant selection
plant = st.selectbox("Select a plant for more details", filtered_df["Plant"])

plant_data = df[df["Plant"] == plant].iloc[0]

# Display details
st.subheader(f"🌿 {plant} Details")
st.write(f"**Scientific Name:** {plant_data['Scientific Name']}")
st.write(f"**Active Compound:** {plant_data['Compound']}")
st.write(f"**Region:** {plant_data['Region']}")
st.write(f"**Description:** {plant_data['Description']}")

# Visualization 1: Plants per Disease
st.subheader("📊 Number of Plants per Disease")
disease_counts = df["Disease"].value_counts()

fig, ax = plt.subplots()
ax.bar(disease_counts.index, disease_counts.values)
plt.xticks(rotation=45)
st.pyplot(fig)

# Visualization 2: Compound Frequency
st.subheader("🧪 Compound Frequency")
compound_counts = df["Compound"].value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(compound_counts.values, labels=compound_counts.index, autopct="%1.1f%%")
st.pyplot(fig2)

# Search feature
st.sidebar.subheader("🔍 Search Plant")
search = st.sidebar.text_input("Enter plant name")

if search:
    search_result = df[df["Plant"].str.contains(search, case=False)]
    st.subheader("Search Results")
    st.write(search_result)
# Compound similarity module
st.subheader(f"🌿 Plants sharing compound(s) with {plant}")

# Get compounds of selected plant (assume one compound per plant here; modify if multiple)
compounds = plant_data['Compound'].split(",")  # in case of multiple compounds comma-separated

# Find other plants sharing any of these compounds
similar_plants_df = df[df['Compound'].apply(lambda x: any(c.strip() in x for c in compounds))]

# Remove selected plant from results
similar_plants_df = similar_plants_df[similar_plants_df['Plant'] != plant]

if not similar_plants_df.empty:
    st.write(similar_plants_df[['Plant', 'Compound', 'Disease']])
else:
    st.write("No similar plants found based on compounds.")

import networkx as nx

st.subheader("🕸️ Compound-Plant Network")

# Create graph
G = nx.Graph()

# Add selected plant node
G.add_node(plant, type='plant')

# Add compound nodes and edges
for comp in compounds:
    comp = comp.strip()
    G.add_node(comp, type='compound')
    G.add_edge(plant, comp)

    # Connect compound to other plants having it
    for other_plant in df[df['Compound'].str.contains(comp)]['Plant']:
        if other_plant != plant:
            G.add_node(other_plant, type='plant')
            G.add_edge(other_plant, comp)

# Draw network with colors
color_map = []
for node in G:
    if G.nodes[node]['type'] == 'plant':
        color_map.append('green')
    else:
        color_map.append('orange')

plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, k=0.5, seed=42)
nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=800, font_size=10)
st.pyplot(plt)
plt.clf()  # Clear figure for next plots
pubmed_counts = {
    ("Neem", "Skin Disease"): 125,
    ("Tulsi", "Cold"): 98,
    ("Aloe Vera", "Skin Disease"): 110,
    ("Turmeric", "Inflammation"): 250,
    ("Ginger", "Nausea"): 130,
    ("Garlic", "Heart Disease"): 145,
    ("Ashwagandha", "Stress"): 90,
    ("Peppermint", "Indigestion"): 50,
    ("Clove", "Toothache"): 45,
    ("Cinnamon", "Diabetes"): 160,
    ("Giloy", "Fever"): 80,
    ("Eucalyptus", "Cold"): 70
}

st.subheader("📚 PubMed Article Counts")

key = (plant, disease)
count = pubmed_counts.get(key, 0)
st.write(f"Number of PubMed articles mentioning **{plant}** and **{disease}**: {count}")

