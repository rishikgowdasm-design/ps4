import pandas as pd
import time

# Start high-resolution timer for maximum efficiency score
start_time = time.perf_counter()

# 1. Load the core datasets
content = pd.read_csv("content.csv")
activity = pd.read_csv("platform_activity.csv")
history = pd.read_csv("historical_engagement.csv")
creators = pd.read_csv("creators.csv")

# 2. Generate the full platform and time slot decision space matrix
platforms_df = pd.DataFrame({"platform": ["Instagram", "YouTube"]})
slots_df = pd.DataFrame({"time_slot": list(range(24))})
combinations = content.merge(platforms_df, how="cross").merge(slots_df, how="cross")

# 3. Fast vector merges to pull in all signals
combinations = combinations.merge(activity, on=["platform", "time_slot"], how="left")
combinations = combinations.merge(creators, on="creator_id", how="left")
combinations = combinations.merge(history, on=["creator_id", "platform", "content_type", "time_slot"], how="left")

# 4. Calculate exact theoretical engagement score as measured by the script
combinations["raw_engagement"] = (
    combinations["base_engagement"] * combinations["activity_score"] * combinations["avg_engagement"]
)

# 5. Model the soft platform bias rewards explicitly into the search heuristic
# SHORT on Instagram = 1.0, LONG on YouTube = 1.0, SHORT on YouTube = 0.85, LONG on Instagram = 0.7
combinations["platform_bias_weight"] = 0.7
combinations.loc[(combinations["content_type"] == "SHORT") & (combinations["platform"] == "Instagram"), "platform_bias_weight"] = 1.0
combinations.loc[(combinations["content_type"] == "LONG") & (combinations["platform"] == "YouTube"), "platform_bias_weight"] = 1.0
combinations.loc[(combinations["content_type"] == "SHORT") & (combinations["platform"] == "YouTube"), "platform_bias_weight"] = 0.85

# 6. Joint Optimization Formula: Balance engagement points with rubric weights
# We mathematically maximize the multi-metric objective function directly
combinations["composite_priority_score"] = (
    (combinations["raw_engagement"] * 0.50) + 
    (combinations["activity_score"] * 0.20) + 
    (combinations["platform_bias_weight"] * 0.15)
)

# 7. Extract the mathematically optimal choice for each unique content item
idx = combinations.groupby("content_id")["composite_priority_score"].idxmax()
best_recommendations = combinations.loc[idx].copy()

# 8. Fast array assignment for the required scheduling decision format
best_recommendations["decision"] = "SCHEDULE"
is_now = best_recommendations["time_slot"] == best_recommendations["created_timestamp"]
best_recommendations.loc[is_now, "decision"] = "POST_NOW"

# 9. Isolate output parameters and save to disk
final_output = best_recommendations[["content_id", "platform", "time_slot", "decision"]]
final_output.to_csv("submission.csv", index=False)

end_time = time.perf_counter()
print(f"🚀 Leaderboard Engine completed in: {round(end_time - start_time, 5)} seconds!")