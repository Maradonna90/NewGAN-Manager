#!/usr/bin/env python3
"""
Improved script to extract all unique country codes from tumtakim23.rtf file
and display them in a more readable format
"""
import os
import re
from collections import Counter

def extract_country_codes(file_path):
    """Extract all country codes from the RTF file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find all country codes in the Nat column using the table structure
        pattern = r'\|\s+(\w{3}|\w{2}|[A-ZÇŞĞİÖÜ]{3})\s+\|'
        
        # Find all matches
        matches = re.findall(pattern, content)
        
        # Filter out anything that doesn't look like a country code
        # Country codes should be 2-3 characters and all uppercase
        country_codes = [m for m in matches if (2 <= len(m) <= 3) and m.isupper() or any(c in m for c in 'ÇŞĞİÖÜ')]
        
        # Count occurrences of each country code
        country_counts = Counter(country_codes)
        
        # Get unique country codes and sort them
        unique_countries = sorted(country_counts.keys())
        
        print(f"Found {len(unique_countries)} unique country codes:\n")
        
        # Print in multiple columns for better readability
        cols = 5  # Number of columns
        for i in range(0, len(unique_countries), cols):
            row = unique_countries[i:i+cols]
            print("  ".join(f"{country:<5}" for country in row))
        
        print("\nCountry codes with occurrence counts:")
        for country in unique_countries:
            print(f"{country}: {country_counts[country]}")
        
        # Save the countries to a file
        with open('country_codes.txt', 'w', encoding='utf-8') as f:
            for country in unique_countries:
                f.write(f"{country}\n")
        
        print(f"\nList of country codes saved to country_codes.txt")
        
        return unique_countries, country_counts
        
    except Exception as e:
        print(f"Error processing the file: {e}")
        return [], Counter()

if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "tumtakim23.rtf")
    unique_countries, country_counts = extract_country_codes(file_path)
