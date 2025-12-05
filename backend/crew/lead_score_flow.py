def run_lead_score_flow(leads_csv_path: str, max_leads: int = 50) -> dict:
    # TODO
    return {
        "scored_leads": [
            {"id": idx, "score": max(0, 100 - idx), "source": leads_csv_path}
            for idx in range(min(max_leads, 5))
        ]
    }
