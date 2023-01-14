from datetime import timedelta

delta = timedelta(hours=5, minutes=30)
hours = delta.total_seconds() / 3600
print(hours) # Output: 5.5
