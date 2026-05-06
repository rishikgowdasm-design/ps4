import pandas as pd

# Load the data you just generated
content = pd.read_csv("content.csv")
activity = pd.read_csv("platform_activity.csv")
history = pd.read_csv("historical_engagement.csv")
creators = pd.read_csv("creators.csv")

recommendations = []

# Process each content item
for _, item in content.iterrows():
    best_score = -1
    best_platform = ""
    best_slot = 0
    
    # Check both platforms and all 24 hours to find the best combo
    for platform in ["Instagram", "YouTube"]:
        for slot in range(24):
            # Get activity score
            act_score = activity[(activity['platform'] == platform) & 
                                 (activity['time_slot'] == slot)]['activity_score'].values[0]
            
            # Get historical performance
            hist_perf = history[(history['creator_id'] == item['creator_id']) & 
                                (history['platform'] == platform) & 
                                (history['content_type'] == item['content_type']) & 
                                (history['time_slot'] == slot)]['avg_engagement'].values[0]
            
            # Get creator base
            base = creators[creators['creator_id'] == item['creator_id']]['base_engagement'].values[0]
            
            # Calculate total expected engagement
            score = base * act_score * hist_perf
            
            if score > best_score:
                best_score = score
                best_platform = platform
                best_slot = slot

    # Decision: If the best slot is the current timestamp, POST_NOW, else SCHEDULE
    decision = "POST_NOW" if best_slot == item['created_timestamp'] else "SCHEDULE"
    
    recommendations.append([item['content_id'], best_platform, best_slot, decision])

# Save the results for the scorer
df_output = pd.DataFrame(recommendations, columns=['content_id', 'platform', 'time_slot', 'decision'])
df_output.to_csv("submission.csv", index=False)

print("recommendation_engine.py: submission.csv generated successfully!")