from datetime import datetime

def convert_date_format(date_string):
    # Parse the date string using the format "%b %d, %Y"
    date = datetime.strptime(date_string, "%b %d, %Y")

    # Convert the date to the desired format: dd/mm/yy
    short_date = date.strftime("%d/%m/%y")

    return short_date

# Example usage
date_string = "Jan 20, 2022"
short_date = convert_date_format(date_string)
print(short_date)  # Output: 20/01/22