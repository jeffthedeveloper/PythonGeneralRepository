from google.cloud import dialogflow_v2

# Create a Dialogflow client
client = dialogflow_v2.AgentsClient()

# Get the agent ID
agent_id = "YOUR_AGENT_ID"

# Get the statistics
statistics = client.get_agent_statistics(agent_id)

# Print the statistics
print(statistics)


# Get the average time spent using the chat
average_time_spent = statistics.conversations_duration_seconds / statistics.conversations_count

# Print the average time spent
print(average_time_spent)

# Get the statistics for each topic
topic_statistics = statistics.topics_statistics

# Print the statistics for each topic
for topic_statistics in topic_statistics:
  print(topic_statistics.topic_name, topic_statistics.conversations_count)
