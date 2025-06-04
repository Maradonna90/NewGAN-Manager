#!/usr/bin/env python3
"""
Script to extract all unique country codes from tumtakim23.rtf file
"""
import os
import re
from collections import Counter

def extract_country_codes(file_path):
    """Extract all country codes from the RTF file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Find all country codes in the Nat column
        # Looking for pattern where country code follows "| " and is followed by spaces
        country_pattern = r'\|\s+([A-ZÇŞĞİÖÜ][A-ZÇŞĞİÖÜ][A-ZÇŞĞİÖÜ])\s+\|'
        
        # Also look for 2nd nationality codes
        second_nat_pattern = r'\|\s+([A-ZÇŞĞİÖÜ][A-ZÇŞĞİÖÜ][A-ZÇŞĞİÖÜ])\s+\|'
        
        # Find all matches
        matches = re.findall(country_pattern, content)
        second_nat_matches = re.findall(second_nat_pattern, content)
        
        # Combine all country codes
        all_countries = matches + second_nat_matches
        
        # Count occurrences of each country code
        country_counts = Counter(all_countries)
        
        # Get unique country codes and sort them
        unique_countries = sorted(country_counts.keys())
        
        print(f"Found {len(unique_countries)} unique country codes:")
        for country in unique_countries:
            print(f"{country}: {country_counts[country]} occurrences")
        
        return unique_countries, country_counts
        
    except Exception as e:
        print(f"Error processing the file: {e}")
        return [], Counter()

if __name__ == "__main__":
    file_path = os.path.join(os.getcwd(), "tumtakim23.rtf")
    unique_countries, country_counts = extract_country_codes(file_path)
    
    print("\nTotal unique country codes:", len(unique_countries))
    print("\nCountry codes (alphabetically):")
    print(", ".join(unique_countries))
