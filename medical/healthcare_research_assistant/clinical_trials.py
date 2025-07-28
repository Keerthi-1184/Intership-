import requests

def fetch_clinical_trials(condition, max_results=5):
    base_url = "https://clinicaltrials.gov/api/v2/studies"
    params = {"query.cond": condition, "pageSize": max_results}
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        trials = []
        for study in data.get("studies", []):
            title = study["protocolSection"]["identificationModule"]["briefTitle"]
            phase = study["protocolSection"].get("designModule", {}).get("studyType", "N/A")
            trials.append({"title": title, "phase": phase})
        return trials
    except Exception as e:
        print(f"Error fetching clinical trials: {e}")
        return []