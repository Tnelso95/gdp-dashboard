import streamlit as st
import numpy as np

# Function to calculate Swing Length
def calc_swing_length(time_to_contact, bat_speed):
    return (time_to_contact / 1.3636) * bat_speed

# Function to calculate Swing Acceleration
def calc_swing_acceleration(bat_speed, swing_length):
    return 0.03343 * (bat_speed ** 2 / swing_length)

# Function to calculate Swing Score
def calc_swing_score(swing_acceleration, min_swing_acc=15, max_swing_acc=30):
    score = 20 + ((swing_acceleration - min_swing_acc) / (max_swing_acc - min_swing_acc)) * 60
    return max(min(score, 80), 20)  # Ensure score is within the 20-80 range

# Function to calculate Euclidean distance
def euclidean_distance(x1, y1, z1, x2, y2, z2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)

# Function to assign color category based on input values and cluster centroids
def assign_color_category(bat_speed, swing_acceleration, attack_angle):
    clusters = {
        "Orange": [73.3, 24.03, 8.84],
        "Purple": [71.2, 24.66, 8.41],
        "Red": [69.9, 22.21, 10.39],
        "Grey": [69.3, 22.21, 14.47],
        "Green": [65.9, 22.29, 8.47],
        "Pink": [68.7, 20.48, 10.34],
        "Brown": [68.9, 22.47, 6.33],
        "Blue": [64.4, 20.4, 8.99]
    }

    distances = {color: euclidean_distance(bat_speed, swing_acceleration, attack_angle, *coords)
                 for color, coords in clusters.items()}
    return min(distances, key=distances.get)

# Define descriptions and expected metrics for each category
category_info = {
    "Orange": {
        "description": "Aaron Judge, Shohei Ohtani, Yordan Alvarez\n"
                       "Very efficient to the ball and finds success in utilizing the high bat speed to hit pitches out in front for power. This group may be plagued by a high whiff rate.",
        "metrics": "wOBA: .323, Whiff Pct: 25.9, Barrel Pct: 11.51, Batting Avg: .245, ISO: .185"
    },
    "Purple": {
        "description": "Juan Soto, Bobby Witt Jr., Gunnar Henderson\n"
                       "This group is the most efficient to the ball and is full of complete hitters that can hit for average and power. Hitters in this group who struggle likely are finding their efficiency by hitting balls too deep.",
        "metrics": "wOBA: .318, Whiff Pct: 23.22, Barrel Pct: 9.37, Batting Avg: .245, ISO: .168"
    },
    "Red": {
        "description": "Trea Turner, Jesse Winker, Patrick Wisdom\n"
                       "This cluster consists of slightly longer than average swings that take longer than average from start to impact, but generally benefit from hitting the ball in front of the plate. These longer swings may result in too many whiffs.",
        "metrics": "wOBA: .312, Whiff Pct: 24.65, Barrel Pct: 9.22, Batting Avg: .241, ISO: .172"
    },
    "Grey": {
        "description": "Max Muncy, Christian Encarnacion-Strand, Brandon Lowe\n"
                       "Relatively normal swings in the context of bat speed and swing length, but follow a very uppercut path. These swings find production through power, while hitting for a low average and whiffing often.",
        "metrics": "wOBA: .300, Whiff Pct: 28.06, Barrel Pct: 10.16, Batting Avg: .216, ISO: .171"
    },
    "Green": {
        "description": "Steven Kwan, Mookie Betts, Josh Smith\n"
                       "This group consists of slow to average bat speeds but all very efficient swings. They find success in strong utilization of bat to ball skills and may struggle with too steep of an attack angle.",
        "metrics": "wOBA: .298, Whiff Pct: 18.45, Barrel Pct: 4.81, Batting Avg: .242, ISO: .111"
    },
    "Pink": {
        "description": "Jose Altuve, Cody Bellinger, Marcus Semien\n"
                       "This group has high variance with its best hitters finding success by elevating the ball to the pull side, thanks to a point of contact well in front of the plate. The hitters who struggle in this group are due to their high swing length being a product of a truly long swing, not a point of contact that results in pulled fly balls.",
        "metrics": "wOBA: .293, Whiff Pct: 24.27, Barrel Pct: 7.92, Batting Avg: .221, ISO: .150"
    },
    "Brown": {
        "description": "Brenton Doyle, Yandy Diaz, Kevin Kiermaier\n"
                       "Slightly slower swings with a very flat attack angle. If these swings are successful it’s likely because of a strong contact-oriented approach. They don’t whiff much but may struggle to hit for power.",
        "metrics": "wOBA: .284, Whiff Pct: 20.49, Barrel Pct: 5.10, Batting Avg: .235, ISO: .113"
    },
    "Blue": {
        "description": "Charlie Blackmon, Cavan Biggio, Nicky Lopez\n"
                       "This group generally struggles, with a low bat speed and not getting to that bat speed quickly. The hitters who find success are doing so through a contact-oriented approach with the margin for error being razor thin.",
        "metrics": "wOBA: .273, Whiff Pct: 19.75, Barrel Pct: 3.43, Batting Avg: .222, ISO: .093"
    }
    # Add other categories here...
}

# Streamlit app code
st.title('Swing Metrics Calculator')

# Input sliders
bat_speed = st.slider('Bat Speed:', 50.0, 90.0, 65.0)
attack_angle = st.slider('Attack Angle:', -5.0, 25.0, 0.0)
time_to_contact = st.slider('Time to Contact:', 0.1, 0.2, 0.15)

# Calculate swing length, acceleration, score, and color category
swing_length = calc_swing_length(time_to_contact, bat_speed)
swing_acceleration = calc_swing_acceleration(bat_speed, swing_length)
swing_score = calc_swing_score(swing_acceleration)
color_category = assign_color_category(bat_speed, swing_acceleration, attack_angle)

# Display the results
st.write(f"Bat Speed: {bat_speed}")
st.write(f"Attack Angle: {attack_angle}")
st.write(f"Time to Contact: {time_to_contact}")
st.write(f"Swing Length: {swing_length:.2f}")
st.write(f"Swing Acceleration: {swing_acceleration:.2f}")
st.write(f"Swing Score: {swing_score:.2f}")
st.write(f"Color Category: {color_category}")
st.write(f"Description: {category_info[color_category]['description']}")
st.write(f"Expected Metrics: {category_info[color_category]['metrics']}")
