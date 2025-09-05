import math
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import genshin  # your package
import plotly.express as px
import time

# --- Page settings ---
st.set_page_config(
    page_title="Genshin Impact Wish Calculator",
    page_icon="✨",
    layout="wide"
)

# --- Title ---
st.markdown("# 🌟 Genshin Impact Wish Calculator")
st.markdown("Plan your **primogems** and simulate probabilities for **characters** and **weapons**")
st.image("banner.png", width=600) # use_container_width=True

# =====================
# Sidebar Inputs
# =====================
with st.sidebar:
    st.markdown("## 📝 Inputs")

    primos = st.number_input(
        "Current Primogems",
        min_value=0,
        value=2000,
        help="The amount of primogems you currently have."
    )
    wishes = st.number_input(
        "Current Wishes",
        min_value=0,
        value=50,
        help="The number of Intertwined Fates (promotional wishes) you already own."
    )
    paimon_bargains = st.number_input(
        "Paimon Bargains Coins",
        min_value=0,
        value=25,
        help="Starglitter coins you can use for buying fates."
    )
    crystals = st.number_input(
        "Crystals",
        min_value=0,
        value=0,
        help="Genesis Crystals available (will be converted to primogems)."
    )

    st.markdown("## 📅 Target Date")
    target_date = st.date_input(
        "Select the date",
        help="Choose the day when you want to pull."
    )
    day, month, year = target_date.day, target_date.month, target_date.year
 
    current_pity_char = st.number_input(
       "Current Character Pity",
       min_value=0,
       max_value=89,
       value=11,
       help="How many wishes since your last 5★ on the character banner."
    )
    current_pity_weapon = st.number_input(
        "Current Weapon Pity",
        min_value=0,
        max_value=79,
        value=0,
        help="How many wishes since your last 5★ on the weapon banner."
    )
 
    fifty_origin_char = st.checkbox(
        "Character banner 50/50 already lost?",
        value=False,
        help="Check if your next character 5★ is guaranteed."
    )
    fifty_origin_weapon = st.checkbox(
        "Weapon banner guarantee used?",
        value=False,
        help="Check if you're already guaranteed a weapon from the banner (no epitomized path)."
    )
 
    order_text = st.text_area(
        "Order of pulls (comma separated)",
        value="character,weapon,character,character,character",
        help="Desired sequence of banners you want to pull (e.g. character, weapon, character)."
    )
 
    capture = st.number_input(
        "Capturing Radiance index",
        min_value=0,
        max_value=3,
        value=0,
        help="Number of 50/50 lost in a row (max 3)"
    )


    # Advanced settings
    with st.expander("⚙️ Advanced Settings"):
        tries = st.number_input(
            "Monte Carlo Tries",
            min_value=1000,
            max_value=1000000,
            value=100000,
            step=1000,
            help="Number of random simulations used to estimate probabilities (higher = more accurate but slower)."
        )

# =====================
# Main Section
# =====================
if st.button("✨ Calculate!"):
    # --- Compute current primogems ---
    currently_primos = primos + (wishes + math.trunc(paimon_bargains / 5)) * 160 + crystals
    st.markdown("## 📈 Current Totals")
    st.write(f"Current protos = {currently_primos}")
    st.write(f"Current wishes = {math.trunc(currently_primos / 160)}")

    # --- Final primogems/wishes ---
    final_day = genshin.gacha.giveFinalday(day, month, year)
    protos = genshin.gacha.datesMatrix(final_day, currently_primos)[0]
    final_wishes = round(protos / 160)
    st.success(f"🎯 On {day}/{month}/{year}, you will have around **{final_wishes} wishes**")

    # --- Probabilities ---
    order = [x.strip() for x in order_text.split(",")]
    current_pity = [current_pity_char, current_pity_weapon]
    fifty_origin = [fifty_origin_char, fifty_origin_weapon]

    
    with st.spinner("Calculating probabilities... ✨"):
        gold_num_prob_output = genshin.gacha.full_5star_wishing(
            final_wishes,
            tries,
            current_pity,
            fifty_origin,
            order,
            capture=capture
        )
        time.sleep(1)  # optional, just to show spinner

    Y_axis = [x / tries * 100 for x in gold_num_prob_output]
    X_axis = range(len(gold_num_prob_output))
    colors = ["black"] + ["violet" if item == "character" else "cyan" for item in order]

    # --- Layout with 2 columns: table + plot ---
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("## 📋 Probability Table")
        stages = [f"{i} promotional" for i in range(len(Y_axis))]

        # Build pulling result column
        C_count = -1
        R_count = 0
        pulling_result = []
        for i in range(len(Y_axis)):
            if i == 0:
                pulling_result.append("CXR0")
            elif i-1 < len(order):
                if order[i-1] == 'character':
                    C_count += 1
                elif order[i-1] == 'weapon':
                    R_count += 1
                pulling_result.append(f"C{C_count}R{R_count}")
            else:
                # beyond the order, keep max limits
                pulling_result.append(f"C{min(C_count,6)}R{min(R_count,5)}")
    
        # Build table HTML
        table_html = "<table style='font-size:20px; border-collapse: collapse;'>"
        table_html += "<tr><th style='padding:4px; text-align:center; width:200px;'>Stage</th>"
        table_html += "<th style='padding:4px; text-align:center; width:200px;'>Pulling Result</th>"
        table_html += "<th style='padding:4px; text-align:center; width:200px;'>Probability (%)</th></tr>"
    
        for i, val in enumerate(Y_axis):
            table_html += f"<tr><td style='padding:4px; text-align:center;'>{stages[i]}</td>"
            table_html += f"<td style='padding:4px; text-align:center;'>{pulling_result[i]}</td>"
            table_html += f"<td style='padding:4px; text-align:center;'>{round(val)}%</td></tr>"
    
        table_html += "</table>"
    
        st.markdown(table_html, unsafe_allow_html=True)

    with col2:
        st.markdown("## 📊 Wish Outcomes Plot")

        # Ensure your Y_axis and order are correct
        x_labels = [f"{i} promo" for i in range(len(Y_axis))]
        
        stage_labels = []
        for i in range(len(Y_axis)):
            if i == 0:
                stage_labels.append("No promotional pulled")
            elif i-1 < len(order):
                if order[i-1] == "character":
                    stage_labels.append("Promotional character")
                else:
                    stage_labels.append("Promotional weapon")
            else:
                stage_labels.append("Other")


        # Define exact mapping from label → color
        color_map = {
            "No promotional pulled": "black",
            "Promotional character": "violet",
            "Promotional weapon": "cyan",
            "Other": "gray"
        }
        
        # Create the bar chart
        fig = px.bar(
            x=x_labels,
            y=Y_axis,
            color=stage_labels,
            color_discrete_map=color_map,
            #{"black":"black", "violet":"violet", "cyan":"cyan", "gray":"gray"},
            labels={"x":"Stage", "y":"Probability (%)"},
            #title="Wish Outcomes",
            category_orders={"x": x_labels}  # <-- enforce correct left-to-right order
        )
        #fig.update_layout(showlegend=False)
        fig.update_layout(
            height=500,  # taller chart
            xaxis=dict(
                title_font=dict(size=18),   # x-axis label font size
                tickfont=dict(size=14)      # x-axis tick numbers
            ),
            yaxis=dict(
                title_font=dict(size=18),   # y-axis label font size
                tickfont=dict(size=14)      # y-axis tick numbers
            )
        )
        fig.update_yaxes(range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)


st.markdown("<p style='text-align: center; font-size:12px; color:gray;'>Made by Ruben</p>", unsafe_allow_html=True)

