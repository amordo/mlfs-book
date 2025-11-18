#!/usr/bin/env python3
"""
Convert unformatted.csv to simple date, AQI format
"""
import csv
from datetime import datetime

def pm25_to_aqi(pm25):
    """
    Convert PM2.5 concentration (µg/m³) to AQI using the US EPA standard.
    """
    # AQI breakpoints for PM2.5 (24-hour average)
    # (C_low, C_high, AQI_low, AQI_high)
    breakpoints = [
        (0.0, 12.0, 0, 50),
        (12.1, 35.4, 51, 100),
        (35.5, 55.4, 101, 150),
        (55.5, 150.4, 151, 200),
        (150.5, 250.4, 201, 300),
        (250.5, 350.4, 301, 400),
        (350.5, 500.4, 401, 500),
    ]
    
    # Find the appropriate breakpoint
    for c_low, c_high, aqi_low, aqi_high in breakpoints:
        if c_low <= pm25 <= c_high:
            # Linear interpolation formula
            aqi = ((aqi_high - aqi_low) / (c_high - c_low)) * (pm25 - c_low) + aqi_low
            return round(aqi)
    
    # If PM2.5 is above all breakpoints, return max AQI
    if pm25 > 500.4:
        return 500
    
    # If PM2.5 is below 0, return 0
    return 0

def convert_csv():
    """Convert the unformatted CSV to simple date, AQI format"""
    input_file = '/home/iammorjj/Downloads/mlfs-book/data/unformatted.csv'
    output_file = '/home/iammorjj/Downloads/mlfs-book/data/formatted.csv'
    
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        
        # Write header
        writer.writerow(['date', 'pm25'])
        
        # Skip comment lines at the beginning
        lines = infile.readlines()
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith('date,'):
                data_start = i + 1
                break
        
        # Read the CSV data
        reader = csv.DictReader(lines[data_start-1:])
        
        for row in reader:
            # Parse the date
            date_str = row['date']
            dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            
            # Format date as YYYY/M/D (no leading zeros for month and day)
            formatted_date = f"{dt.year}/{dt.month}/{dt.day}"
            
            # Get median PM2.5 value and convert to AQI
            pm25_median = float(row['median'])
            aqi = pm25_to_aqi(pm25_median)
            
            # Write to output
            writer.writerow([formatted_date, aqi])
    
    print(f"Conversion complete! Output saved to: {output_file}")
    print(f"\nFirst few lines:")
    with open(output_file, 'r') as f:
        for i, line in enumerate(f):
            if i < 10:
                print(line.strip())
            else:
                break

if __name__ == '__main__':
    convert_csv()
