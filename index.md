<!-- Main Hero Image -->
<section class="main-hero">
  <img src="/images/main.png" alt="Stem Cell and Advanced Biomedicine Laboratory">
</section>

<!-- Main Content -->
<section class="main-section">
  <div class="recruiting-box">
    <h2>Recruiting</h2>
    <p>
      We are looking for motivated students and researchers interested in
      stem cell biology, organoid technologies, aging, regeneration, and
      regenerative medicine.
    </p>
    <p>
      If you are interested in joining our lab, please contact us with your CV
      and a brief description of your research interests.
    </p>
    <a href="/contact/" class="main-button">Contact Us</a>
  </div>

  <div class="latest-news-box">
    <h2>Latest News</h2>

    {% assign recent_news = site.posts | sort: "date" | reverse %}
    {% for post in recent_news limit:5 %}
      <div class="latest-news-item">
        <p class="latest-news-date">{{ post.date | date: "%B %d, %Y" }}</p>
        <a href="{{ post.url | relative_url }}" class="latest-news-title">
          {{ post.title }}
        </a>
      </div>
    {% endfor %}

    <a href="/news/" class="view-all-news">View all news</a>
  </div>
</section>