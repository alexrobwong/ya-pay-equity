'''
Config file storing all the global variables
'''
# Components to keep
COMPONENTS = [
    'Performance/Demo',
    'Planning Meeting',
    'Professional Learning',
    'Workshop',
    'Virtual Performance',
    'Virtual Planning Meeting',
    'Virtual Professional Learning',
    'Virtual Workshop'
]

# Component filter
CMP_FILT = ['Performance', 'Workshop', 'Learning', 'Meeting']

# Mappings for Artists with the same artist ID
MULT_IDS = {
    'Josh Robinson': 95.1,
    'Poetry Meets Percussion': 95.2,
    'Samba to Salsa': 95.3,
    'Dave Fry': 20.1,
    'RockRoots': 20.2,
    'The Junk Jam Band': 56.1,
    'Zachary Green': 56.2
}

# Artist IDs to remove
REMOVE_ARTIST_IDS = [0]

# Final columns for output
COLS = ['artist_account_name', 'artist_id',
       'Art Form (General Discipline)', 'Contract Classification', 'Date',
       'Contract #', 'Client Zip Code', 'Client', 'Billing Code',
       'Component Type', 'Artist Fee', 'respondent_id', 'age', 'gender',
       'city', 'state', 'company', 'ethnicity', 'multi_ind', 'performance', 'workshop']