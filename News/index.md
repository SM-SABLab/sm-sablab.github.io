---
title: News
nav:
  order: 4
  tooltip: Lab news
style: news
---

# News

## 2026 

<div class="news-panel panel-2026">
{% assign posts2026 = site.pages | where_exp: "p", "p.path contains 'News/Posts/2026'" | sort: "date" | reverse %}
{% for post in posts2026 %}
<article class="news-post">
  <h3>{{ post.date | date: "%B %-d, %Y" }}</h3>

  <div class="news-content">
    {{ post.content }}
  </div>

  {% if post.image %}
  <img class="news-image"
     src="{{ post.image | relative_url }}"
     alt="{{ post.title }}"
     style="width: {{ post.image_width | default: '100%' }};">
  {% endif %}
</article>
{% endfor %}
</div>

## 2025

<div class="news-panel panel-2025">
{% assign posts2025 = site.pages | where_exp: "p", "p.path contains 'News/Posts/2025'" | sort: "date" | reverse %}
{% for post in posts2025 %}
<article class="news-post">
  <h3>{{ post.date | date: "%B %-d, %Y" }}</h3>

  <div class="news-content">
    {{ post.content }}
  </div>

  {% if post.image %}
  <img class="news-image"
     src="{{ post.image | relative_url }}"
     alt="{{ post.title }}"
     style="width: {{ post.image_width | default: '100%' }};">
  {% endif %}
</article>
{% endfor %}
</div>
