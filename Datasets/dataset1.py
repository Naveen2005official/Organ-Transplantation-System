import pandas as pd
import numpy as np
from faker import Faker
from geopy.distance import geodesic

fake = Faker()

# Create Donor Data with additional features
def create_donor_data(num_samples):
    donors = []
    for _ in range(num_samples):
        donor_lat = fake.latitude()
        donor_lon = fake.longitude()
        donors.append({
            'Donor ID': fake.unique.random_number(digits=5),
            'Age': np.random.randint(18, 65),
            'Gender': np.random.choice(['M', 'F']),
            'Blood Type': np.random.choice(['A', 'B', 'AB', 'O']),
            'Organ Type': np.random.choice(['Kidney', 'Liver', 'Heart', 'Lung', 'Pancreas', 'Intestine']),
            'Health Conditions': fake.sentence(),
            'Tissue Type': np.random.choice(['A', 'B', 'AB']),
            'Organ Size': round(np.random.uniform(0.5, 2.0), 2),
            'Donation Date': fake.date_between(start_date='-2y', end_date='today'),
            'Donor Latitude': donor_lat,
            'Donor Longitude': donor_lon,
            'Organ Viability Time (hours)': round(np.random.uniform(4, 72), 2)  # Viability time varies by organ
        })
    return pd.DataFrame(donors)

# Create Recipient Data with additional features
def create_recipient_data(num_samples):
    recipients = []
    for _ in range(num_samples):
        recipient_lat = fake.latitude()
        recipient_lon = fake.longitude()
        recipients.append({
            'Recipient ID': fake.unique.random_number(digits=5),
            'Age': np.random.randint(18, 65),
            'Gender': np.random.choice(['M', 'F']),
            'Blood Type': np.random.choice(['A', 'B', 'AB', 'O']),
            'Health Conditions': fake.sentence(),
            'Priority Level': np.random.choice(['High', 'Medium', 'Low']),
            'Wait Time (Months)': np.random.randint(1, 60),
            'Recipient Location': np.random.choice(['Urban', 'Rural']),
            'Organ Size Requirement': round(np.random.uniform(0.5, 2.0), 2),
            'HLA Match Score': np.random.randint(1, 10),
            'Previous Transplants': np.random.randint(0, 2),
            'Immunosuppressant History': np.random.choice(['None', 'Minimal', 'Significant']),
            'Blood Pressure': np.random.randint(90, 160),
            'Recipient Latitude': recipient_lat,
            'Recipient Longitude': recipient_lon
        })
    return pd.DataFrame(recipients)

# Calculate Blood Type Compatibility (basic compatibility rules)
def calculate_blood_type_compatibility(recipient_blood_type, donor_blood_type):
    if recipient_blood_type == donor_blood_type:
        return 1
    if recipient_blood_type == 'AB':
        return 1  # Universal recipient
    if donor_blood_type == 'O':
        return 1  # Universal donor
    return 0  # Not compatible

# Calculate Geographical Distance between Donor and Recipient
def calculate_geographical_distance(recipient_row, donor_row):
    recipient_coords = (recipient_row['Recipient Latitude'], recipient_row['Recipient Longitude'])
    donor_coords = (donor_row['Donor Latitude'], donor_row['Donor Longitude'])
    return geodesic(recipient_coords, donor_coords).km

# Add the Compatibility features to the recipient data
def add_compatibility_features(donor_data, recipient_data):
    recipient_data['Compatible'] = np.nan  # Placeholder for compatibility
    recipient_data['Blood Type Compatibility'] = np.nan
    recipient_data['Geographical Distance (km)'] = np.nan
    
    # Iterate over the recipient data and match with a random donor (you can change this matching logic)
    for i, recipient in recipient_data.iterrows():
        donor = donor_data.sample(n=1).iloc[0]  # Random donor for now
        
        # Blood type compatibility
        recipient_data.at[i, 'Blood Type Compatibility'] = calculate_blood_type_compatibility(recipient['Blood Type'], donor['Blood Type'])
        
        # Geographical distance
        recipient_data.at[i, 'Geographical Distance (km)'] = calculate_geographical_distance(recipient, donor)
        
        # Compatibility based on organ size match, HLA match, and other factors (random for now)
        organ_size_match = 1 if abs(recipient['Organ Size Requirement'] - donor['Organ Size']) < 0.2 else 0
        hla_match = 1 if recipient['HLA Match Score'] >= 6 else 0
        recipient_data.at[i, 'Compatible'] = (organ_size_match + hla_match + recipient_data.at[i, 'Blood Type Compatibility']) >= 2  # Example threshold

# Generate the synthetic data
donor_data = create_donor_data(1000)
recipient_data = create_recipient_data(1000)

# Add compatibility features
add_compatibility_features(donor_data, recipient_data)

# Save the synthetic datasets to CSV for later use
donor_data.to_csv('donor_data.csv', index=False)
recipient_data.to_csv('recipient_data.csv', index=False)

# Display sample data
print("Donor Data Sample:\n", donor_data.head())
print("\nRecipient Data Sample with Compatibility Features:\n", recipient_data.head())
