"""
Contains code for extracting labelled samples from the database based on foreign key relationships.
"""

import pandas as pd

def extract_labelled_samples(data: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts (positive) labelled samples from the database based on foreign key relationships.
    """
    found_samples = pd.DataFrame(columns=['mccp', 'wccp', 'linz', 'err', 'marburg'])

    for index, row in data.iterrows():
        source = row['source']
        match source:
            case "munich":
                matches = data[(data['source'] != 'munich') & (data['munichNumber'] == row['munichNumber'])][['source', 'uri']]
                to_append = []
                for index, match in matches.iterrows():
                    to_append.append({
                        'mccp': row['uri'],
                        'wccp': match['uri'] if match['source'] == 'wccp' else None,
                        'linz': None if match['source'] != 'linz' else match['uri'],
                        'err': None if match['source'] != 'err' else match['uri'],
                        'marburg': None if match['source'] != 'marburg' else match['uri'],
                    })

                found_samples = pd.concat([found_samples, pd.DataFrame(to_append)])
            case "wccp":
                matches = data[(data['source'] != 'wccp') & (data['wccpNumber'] == row['wccpNumber'])][['source', 'uri']]
                to_append = []
                for index, match in matches.iterrows():
                    to_append.append({
                        'mccp': None if match['source'] != 'munich' else match['uri'],
                        'wccp': row['uri'],
                        'linz': None if match['source'] != 'linz' else match['uri'],
                        'err': None if match['source'] != 'err' else match['uri'],
                        'marburg': None if match['source'] != 'marburg' else match['uri'],
                    })

                found_samples = pd.concat([found_samples, pd.DataFrame(to_append)])
            case "linz":
                matches = data[(data['source'] != 'linz') & (data['linzNumber'] == row['linzNumber'])][['source', 'uri']]
                to_append = []
                for index, match in matches.iterrows():
                    to_append.append({
                        'mccp': None if match['source'] != 'munich' else match['uri'],
                        'wccp': None if match['source'] != 'wccp' else match['uri'],
                        'linz': row['uri'],
                        'err': None if match['source'] != 'err' else match['uri'],
                        'marburg': None if match['source'] != 'marburg' else match['uri'],
                    })

                found_samples = pd.concat([found_samples, pd.DataFrame(to_append)])
            case "err":
                matches = data[(data['source'] != 'err') & (data['errNumber'] == row['errNumber'])][['source', 'uri']]
                to_append = []
                for index, match in matches.iterrows():
                    to_append.append({
                        'mccp': None if match['source'] != 'munich' else match['uri'],
                        'wccp': None if match['source'] != 'wccp' else match['uri'],
                        'linz': None if match['source'] != 'linz' else match['uri'],
                        'err': row['uri'],
                        'marburg': None if match['source'] != 'marburg' else match['uri'],
                    })

                found_samples = pd.concat([found_samples, pd.DataFrame(to_append)])
            case "marburg":
                matches = data[(data['source'] != 'marburg') & (data['marburgNumber'] == row['marburgNumber'])][['source', 'uri']]
                to_append = []
                for index, match in matches.iterrows():
                    to_append.append({
                        'mccp': None if match['source'] != 'munich' else match['uri'],
                        'wccp': None if match['source'] != 'wccp' else match['uri'],
                        'linz': None if match['source'] != 'linz' else match['uri'],
                        'err': None if match['source'] != 'err' else match['uri'],
                        'marburg': row['uri'],
                    })

                found_samples = pd.concat([found_samples, pd.DataFrame(to_append)])

    return found_samples