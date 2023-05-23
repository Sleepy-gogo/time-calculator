def swap_denotation(den):
  denotation = "PM" if den == "AM" else "AM"
  days_passed = 1 if den == "PM" else 0

  return denotation, days_passed


def check_hours(hours, was_less=False):
  change = False

  if hours > 12:
    hours = hours % 12
    change = True

  if was_less and hours == 12:
    change = True

  return hours, change


def add_seconds(time, dur_seconds):
  hours, secs = time

  secs += dur_seconds

  if secs >= 60:
    hours += 1
    secs %= 60

  return [hours, secs]


def add_hours(hours, dur_hours):
  return hours + dur_hours


def calculate_intervals(hours):
  days = int(hours / 24)
  hours %= 24
  den_swap = hours > 12
  hours %= 12

  return days, den_swap, hours


def generate_aclaration(days):
  if not days:
    return ""

  if days == 1:
    return " (next day)"

  return f" ({days} days later)"


def calculate_weekday(weekday, passed_days):
  week = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday"
  ]
  idx = week.index(weekday.capitalize()) + passed_days

  idx %= len(week)

  return f", {week[idx]}"


def format_time(hours, secs):
  if secs < 10:
    secs = "0" + str(secs)

  return f"{hours}:{secs}"


def split_time(time):
  splited = time.split(":")
  res = [int(part) for part in splited]
  return res


def add_time(start, duration, weekday=""):
  start_time, denotation = start.split()

  actual_hours, actual_secs = split_time(start_time)
  dur_hours, dur_secs = split_time(duration)

  is_less_than_twelve = actual_hours != 12

  # Checking for 24 hour intervals, and check for AM/PM swap. Adding the rest of the hours

  passed_days, first_change, dur_hours = calculate_intervals(dur_hours)
  actual_hours = add_hours(actual_hours, dur_hours)

  # Adding seconds, updating hours, then checking for another AM/PM swap.

  actual_hours, actual_secs = add_seconds([actual_hours, actual_secs],
                                          dur_secs)
  actual_hours, second_change = check_hours(actual_hours, is_less_than_twelve)

  # If two swaps should happen, a day is added but the denotation is not changed. Otherwise, any swap is made, and the days are added to the counter

  if first_change and second_change:
    passed_days += 1
  elif first_change or second_change:
    denotation, days = swap_denotation(denotation)
    passed_days += days

  # Calculates the final weekday, and all text that should follow up in the result

  final_weekday = calculate_weekday(weekday, passed_days) if weekday else ""
  aclaration_text = generate_aclaration(passed_days)

  end_time = format_time(actual_hours, actual_secs)

  # Returns the desired format reponse

  return f"{end_time} {denotation}{final_weekday}{aclaration_text}"
