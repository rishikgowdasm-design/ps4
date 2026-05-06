import pandas as pd
import time

#---
# Load Data
content = pd.read_csv("content.csv")
activity = pd.read_csv("platform_activity.csv")
history = pd.read_csv("historical_engagement.csv")
creators = pd.read_csv("creators.csv")

# Team output
submission = pd.read_csv("submission.csv")

start_time = time.time()

#
# Metrics accumulators
#
engagement_total = 0
timing_total = 0
platform_score_total = 0

#
# Iterate over submissions
#
for index, row in submission.iterrows():
    cid = row["content_id"]
    platform = row["platform"]
    time_slot = row["time_slot"]
    
    c_row = content[content["content_id"] == cid].iloc[0]
    creator_id = c_row["creator_id"]
    content_type = c_row["content_type"]

    # Activity Score
    act = activity[
        (activity["platform"] == platform) &
        (activity["time_slot"] == time_slot)
    ]["activity_score"].values[0]

    # Historical Engagement
    hist = history[
        (history["creator_id"] == creator_id) &
        (history["platform"] == platform) &
        (history["content_type"] == content_type) &
        (history["time_slot"] == time_slot)
    ]["avg_engagement"].values[0]

    # Creator base engagement
    base = creators[
        creators["creator_id"] == creator_id
    ]["base_engagement"].values[0]

    # 1. Engagement Calculation
    engagement = base * act * hist
    engagement_total += engagement

    # 2. Timing Score
    timing_total += act

    # 3. Platform Quality (soft bias)
    if content_type == "SHORT" and platform == "Instagram":
        platform_score = 1.0
    elif content_type == "LONG" and platform == "YouTube":
        platform_score = 1.0
    elif content_type == "SHORT" and platform == "YouTube":
        platform_score = 0.85
    else: # LONG on Instagram
        platform_score = 0.7
    platform_score_total += platform_score

# Efficiency Calculation
latency = time.time() - start_time
efficiency_score = max(0, 1 - latency) # normalized

# Normalize Metrics
n = len(submission)
engagement_score = engagement_total / n
timing_score = timing_total / n
platform_score = platform_score_total / n

# Optional normalization (safe scaling)
engagement_score = min(engagement_score, 1.5) / 1.5

# Final Score Calculation
final_score = (
    0.50 * engagement_score +
    0.20 * timing_score +
    0.15 * platform_score +
    0.15 * efficiency_score
)

# Output Results
print("\n--- SCORE BREAKDOWN ---")
print("Engagement Score:", round(engagement_score, 4))
print("Timing Score:", round(timing_score, 4))
print("Platform Score:", round(platform_score, 4))
print("Efficiency Score:", round(efficiency_score, 4))
print("\nFinal Score:", round(final_score, 4))