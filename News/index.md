---
title: News
nav:
  order: 4
  tooltip: Lab news
style: news 
---

# News

<h2>2026</h2>

{% assign posts2026 = site.pages | where_exp: "p", "p.path contains 'News/Posts/2026'" | sort: "date" | reverse %}

{% for post in posts2026 %}
<article class="news-post">
  <h3>{{ post.date | date: "%B %-d, %Y" }}</h3>

  <div class="news-content">
    {{ post.content }}
  </div>

  {% if post.image %}
  <img class="news-image" src="{{ post.image | relative_url }}" alt="{{ post.title }}">
  {% endif %}
</article>
{% endfor %}

<details class="news-year">
<summary>2025</summary>

{% assign posts2025 = site.pages | where_exp: "p", "p.path contains 'News/Posts/2025'" | sort: "date" | reverse %}

{% for post in posts2025 %}
<article class="news-post">
  <h3>{{ post.date | date: "%B %-d, %Y" }}</h3>
  <h2>{{ post.title }}</h2>

  <div class="news-content">
    {{ post.content }}
  </div>

  {% if post.image %}
  <img class="news-image" src="{{ post.image | relative_url }}" alt="{{ post.title }}">
  {% endif %}
</article>
{% endfor %}

</details>