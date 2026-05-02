---
title: News
nav:
  order: 4
  tooltip: Lab news
style: news
---

# News

<div class="news-tabs">
  <button class="news-tab active" onclick="showNewsYear('2026', this)">2026</button>
  <button class="news-tab" onclick="showNewsYear('2025', this)">2025</button>
</div>

<div id="news-2026" class="news-year-content active">
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
</div>


<div id="news-2025" class="news-year-content">
{% assign posts2025 = site.pages | where_exp: "p", "p.path contains 'News/Posts/2025'" | sort: "date" | reverse %}

{% for post in posts2025 %}
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
</div>

<script>
function showNewsYear(year, button) {
  document.querySelectorAll('.news-year-content').forEach(function(section) {
    section.classList.remove('active');
  });

  document.querySelectorAll('.news-tab').forEach(function(tab) {
    tab.classList.remove('active');
  });

  document.getElementById('news-' + year).classList.add('active');
  button.classList.add('active');
}
</script>