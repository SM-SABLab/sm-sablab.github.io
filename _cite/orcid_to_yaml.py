import json
from urllib.request import Request, urlopen
import yaml

# 👉 너 ORCID 넣어
ORCID_ID = "0000-0002-9526-9891"

endpoint = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
headers = {"Accept": "application/json"}

def safe_get(d, *keys):
    for k in keys:
        if not d:
            return None
        d = d.get(k)
    return d

try:
    request = Request(url=endpoint, headers=headers)
    response = json.loads(urlopen(request, timeout=10).read())
except Exception as e:
    print("❌ ORCID API 실패:", e)
    exit(1)

works = response.get("group", [])

citations = []

for work in works:
    summaries = work.get("work-summary", [])

    for s in summaries:
        # 안전하게 값 가져오기
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
            "publisher": journal if journal else "",
            "date": f"{year}-01-01" if year else "1900-01-01",
        }

        if doi:
            citation["id"] = f"doi:{doi}"
            citation["link"] = f"https://doi.org/{doi}"

        citations.append(citation)

# 최신순 정렬
citations.sort(key=lambda x: x.get("date", ""), reverse=True)

# 저장
with open("_data/citations.yaml", "w") as f:
    yaml.dump(citations, f, sort_keys=False, allow_unicode=True)

print(f"✅ {len(citations)}개 논문 저장 완료")