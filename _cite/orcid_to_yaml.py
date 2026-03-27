import json
from urllib.request import Request, urlopen
import yaml

ORCID_ID = "0000-0002-9526-9891"
MY_NAME = "Jumee Kim"

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

        if not title:
            continue

        # 🔥 authors 가져오기 (순서 유지)
        contributors = (s.get("contributors") or {}).get("contributor", [])

        authors = []
        for c in contributors:
            name = safe_get(c, "credit-name", "value")
            if name:
                authors.append(name)

        # fallback
        if not authors:
            authors = [MY_NAME]

        # 🔥 내 이름만 bold (순서 유지)
        cleaned_authors = []
        for name in authors:
            if MY_NAME.lower() in name.lower():
                cleaned_authors.append(f"**{MY_NAME}**")
            else:
                cleaned_authors.append(name)

        citation = {
            "id": f"doi:{doi}" if doi else title,
            "title": title,
            "authors": cleaned_authors,
            "publisher": journal if journal else "Unknown",
            "date": f"{year}-01-01" if year else "1900-01-01",
            "link": f"https://doi.org/{doi}" if doi else "",
            "orcid": ORCID_ID,
            "plugin": "orcid.py",
            "file": "orcid.yaml"
        }

        citations.append(citation)


# 최신순 정렬
citations.sort(key=lambda x: x.get("date", ""), reverse=True)


class IndentDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


with open("_data/citations.yaml", "w", encoding="utf-8") as f:
    yaml.dump(
        citations,
        f,
        Dumper=IndentDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=1000
    )

print(f"✅ {len(citations)} publications generated")