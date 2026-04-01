---
title: News
nav:
  order: 4
  tooltip: Musings and miscellany
---

# News

{% assign posts_by_year = site.posts | group_by_exp:"post", "post.date | date: '%Y'" %}

{% for year in posts_by_year %}
  <details {% if year.name == "2026" %}open{% endif %}>
    <summary><strong>{{ year.name }}</strong></summary>

    <ul>
      {% for post in year.items %}
        <li>
          <span>{{ post.date | date: "%b %d" }}</span> —
          <a href="{{ post.url }}">{{ post.title }}</a>
        </li>
      {% endfor %}
    </ul>

  </details>
{% endfor %}