import json
from urllib.request import Request, urlopen

ORCID_ID = "0000-0002-9526-9891"  

endpoint = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
headers = {"Accept": "application/json"}

request = Request(url=endpoint, headers=headers)
response = json.loads(urlopen(request).read())

works = response.get("group", [])

citations = []

for work in works:
    summaries = work.get("work-summary", [])

    for s in summaries:
        title = s.get("title", {}).get("title", {}).get("value")
        journal = s.get("journal-title", {}).get("value")

        year = s.get("publication-date", {}).get("year", {}).get("value")

        # DOI 찾기
        external_ids = s.get("external-ids", {}).get("external-id", [])
        doi = None
        for eid in external_ids:
            if eid.get("external-id-type") == "doi":
                doi = eid.get("external-id-value")

        if not title:
            continue

        citation = {
            "title": title,
            "publisher": journal,
            "date": f"{year}-01-01" if year else "1900-01-01",
        }

        if doi:
            citation["id"] = f"doi:{doi}"
            citation["link"] = f"https://doi.org/{doi}"

        citations.append(citation)

# 최신순 정렬
citations.sort(key=lambda x: x.get("date", ""), reverse=True)

# YAML 저장
import yaml

with open("_data/citations.yaml", "w") as f:
    yaml.dump(citations, f, sort_keys=False, allow_unicode=True)

print("✅ citations.yaml 생성 완료")