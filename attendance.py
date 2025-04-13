import csv
from datetime import datetime

attendance_file = "Attendance.csv"

# Function to mark attendance
def mark_attendance(name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(attendance_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, timestamp])
