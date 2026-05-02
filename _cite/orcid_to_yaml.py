
import json
from urllib.request import Request, urlopen
import yaml
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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

def get_authors_from_crossref(doi):
    try:
        url = f"https://api.crossref.org/works/{doi}"
        with urlopen(url, timeout=10) as response:
            data = json.loads(response.read())

        authors = []
        for a in data["message"].get("author", []):
            given = a.get("given", "")
            family = a.get("family", "")
            name = f"{given} {family}".strip()
            if name:
                authors.append(name)

        return authors
    except:
        return []

request = Request(url=endpoint, headers=headers)
response = json.loads(urlopen(request, timeout=10).read())

works = response.get("group", [])

citations = []
seen_ids = set()

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
                if doi:
                    doi = doi.lower()

        if not title:
            continue

        authors = get_authors_from_crossref(doi) if doi else []

        if not authors:
            authors = [MY_NAME]

        cleaned_authors = []
        for name in authors:
            if MY_NAME.lower() in name.lower():
                cleaned_authors.append(f"**{MY_NAME}**")
            else:
                cleaned_authors.append(name)

        citation_id = f"doi:{doi}" if doi else title

        if citation_id in seen_ids:
            continue
        seen_ids.add(citation_id)

        citation = {
            "id": citation_id,
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