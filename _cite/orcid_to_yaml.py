import json
from urllib.request import Request, urlopen
import yaml

# 👉 너 ORCID 넣기
ORCID_ID = "0000-0002-9526-9891"

endpoint = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
headers = {"Accept": "application/json"}

def safe_get(d, *keys):
    for k in keys:
        if not d:
            return None
        d = d.get(k)
    return d

request = Request(url=endpoint, headers=headers)
response = json.loads(urlopen(request, timeout=10).read())

works = response.get("group", [])

citations = []

for work in works:
    summaries = work.get("work-summary", [])

    for s in summaries:
        title = safe_get(s, "title", "title", "value")
        journal = safe_get(s, "journal-title", "value")
        year = safe_get(s, "publication-date", "year", "value")

        external_ids = (s.get("external-ids") or {}).get("external-id", [])

        doi = None
        for eid in external_ids:
            if eid.get("external-id-type") == "doi":
                doi = eid.get("external-id-value")

        # title 없으면 skip
        if not title:
            continue

        citation = {
            "title": title,
            "authors": ["Jumee Kim"],  # ⭐ 반드시 필요 (템플릿 요구)
            "publisher": journal if journal else "",
            "date": f"{year}-01-01" if year else "1900-01-01",
            "type": "paper"  # ⭐ 반드시 필요
        }

        if doi:
            citation["id"] = f"doi:{doi}"
            citation["link"] = f"https://doi.org/{doi}"
        else:
            # DOI 없으면 id라도 만들어줘야 렌더링됨
            citation["id"] = title

        citations.append(citation)

# 최신순 정렬
citations.sort(key=lambda x: x.get("date", ""), reverse=True)

# YAML 저장 (깨짐 방지 설정 포함)
with open("_data/citations.yaml", "w") as f:
    yaml.dump(
        citations,
        f,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False
    )

print(f"✅ {len(citations)} publications generated")