from datetime import datetime, timedelta
from configs.config import envs
import re
import redis
import json
import random

redis_client = redis.StrictRedis(host=envs['REDIS_DATA_SERVER_IP'], 
                                 port=envs['REDIS_DATA_SERVER_PORT'], db=envs['REDIS_DATA_SERVER_DB'])

def parse_time(appointment_time):
    # Regular expression to match various time formats
    time_pattern = r"(\d{1,2}):(\d{2})(AM|PM)?"
    match = re.match(time_pattern, appointment_time, re.IGNORECASE)
    
    if match:
        hours, minutes, period = match.groups()
        hours = int(hours)
        minutes = int(minutes)
        
        if period and period.lower() == 'pm' and hours != 12:
            hours += 12
        elif period and period.lower() == 'am' and hours == 12:
            hours = 0
        
        return f"{hours:02d}:{minutes:02d}"
    else:
        raise ValueError("Invalid appointment_time format")


def book_appointment(input_data):
    try:
        input_data = json.loads(input_data)

        session_id = input_data.get('session_id')
        doctor_name = input_data.get('doctor_name')
        appointment_time = parse_time(input_data.get('appointment_time'))
        appointment_day = input_data.get('appointment_day')
        
        # Validate session_id, doctor_name, and appointment_time
        if not session_id or not doctor_name or not appointment_time:
            raise ValueError("Invalid session_id, doctor_name, or appointment_time")
        
        # Deduce appointment_day and appointment_date
        if not appointment_day:
            today = datetime.now().date()
            appointment_day = today.strftime("%A")
        
        # Calculate the appointment_date based on today's date and the appointment_day
        days_ahead = (datetime.strptime(appointment_day, "%A").weekday() - datetime.now().weekday()) % 7
        appointment_date = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        # Generate a random 4-digit number for booking ID
        booking_id = random.randint(1000, 9999)
        
        # Store appointment information in Redis
        appointment_info = {
            "session_id": session_id,
            "doctor_name": doctor_name,
            "appointment_time": appointment_time,
            "appointment_date": appointment_date,
            "booking_no": booking_id
        }
        redis_key = f"{session_id}_booking_info"
        json_data = json.dumps(appointment_info)
        redis_client.set(redis_key, json_data)
        
        return f"Appointment scheduled, booking_id is {booking_id}, date is {appointment_date}, time is {appointment_time}"
    
    except ValueError as e:
        return str(e) + ", please confirm the details from the user and try again later"
    
    except Exception as e:
        return "Some error occurred, please try again later"