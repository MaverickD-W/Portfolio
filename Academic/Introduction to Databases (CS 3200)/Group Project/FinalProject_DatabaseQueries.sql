USE Newsense;


-- What is the average rating for each news outlet?

SELECT outlet_name, ROUND(AVG(review_score),2) AS "avg_rating"
FROM news_outlets
	LEFT JOIN articles USING (news_id)
	JOIN reviews USING (article_id)
GROUP BY news_id
ORDER BY avg_rating DESC;

-- What is the average rating across all news outlets?

SELECT ROUND(AVG(avg_rating),2) AS "avg_overall_rating"
FROM (SELECT outlet_name, AVG(review_score) AS "avg_rating"
		FROM news_outlets
			LEFT JOIN articles USING (news_id)
			JOIN reviews USING (article_id)
		GROUP BY news_id
		ORDER BY avg_rating DESC) AS outlet_ratings;

-- How does Political Affiliation count compare to Region count?

SELECT region, political_affiliation, COUNT(political_affiliation) as "num_affiliation"
FROM users
GROUP BY political_affiliation, region;


-- Jake
-- If we weigh the ratings based on user credibility, how does this compare to true average ratings?
SELECT 
  n.outlet_name,
  a.article_title, 
  ROUND(AVG(r.review_score), 2) AS unweighted_avg_rating,
  ROUND(SUM(r.review_score * IFNULL(c.avg_credibility, 1)) / SUM(IFNULL(c.avg_credibility, 1)), 2) AS weighted_avg_rating
FROM news_outlets n
JOIN articles a ON n.news_id = a.news_id
JOIN reviews r ON a.article_id = r.article_id 
JOIN (
  SELECT receiving_user_id, AVG(credibility_rating) AS avg_credibility
  FROM credibility_ratings
  GROUP BY receiving_user_id
  ) c ON r.user_id = c.receiving_user_id
GROUP BY a.article_id
ORDER BY weighted_avg_rating DESC;

-- What is the average review score for an article with each tag?
SELECT t.tag_name, AVG(r.review_score) AS avg_rating 
FROM tags t
JOIN articles_tags ajt ON t.tag_id = ajt.tag_id
JOIN articles a ON ajt.article_id = a.article_id
JOIN reviews r ON a.article_id = r.article_id
GROUP BY t.tag_id
ORDER BY avg_rating DESC;

-- Which authors tend to be more well received (average score for articles written by each author, ordered desc)? How might the number of published articles impact an author’s average score?
SELECT au.author_firstname, au.author_lastname, COUNT(DISTINCT ar.article_id) AS num_articles, ROUND(AVG(r.review_score), 2) AS avg_rating
FROM authors au
JOIN articles_authors arjau ON au.author_id = arjau.author_id
JOIN articles ar ON arjau.article_id = ar.article_id
JOIN reviews r ON ar.article_id = r.article_id
GROUP BY au.author_id
ORDER BY avg_rating DESC;

-- Marie
-- Which tags are most commonly associated with articles from a specific news outlet? 
select c.outlet_name, c.tag_name, c.tag_used
from (
    select n.outlet_name, t.tag_name, count(*) as tag_used
    from tags t
    join articles_tags at on at.tag_id = t.tag_id
    join articles a on at.article_id = a.article_id
    join news_outlets n on n.news_id = a.news_id
    group by n.outlet_name, t.tag_name
) c
join (
    select outlet_name, max(tag_used) as max_tag_used
    from (
        select n.outlet_name, t.tag_name, count(*) as tag_used
        from tags t
        join articles_tags at on at.tag_id = t.tag_id
        join articles a on at.article_id = a.article_id
        join news_outlets n on n.news_id = a.news_id
        group by n.outlet_name, t.tag_name
    ) x
    group by outlet_name
) m
    on c.outlet_name = m.outlet_name
   and c.tag_used = m.max_tag_used
order by c.outlet_name;

-- Which news outlets have the most ratings (top 5)?
select count(review_score) as review_ratings, outlet_name
from reviews r
join articles a on a.article_id = r.article_id
join news_outlets n on n.news_id = a.news_id
group by n.outlet_name
order by review_ratings desc
limit 5;

-- Do certain news outlets receive systematically higher or lower credibility ratings for the same tags or topics?
select tag_name, n.outlet_name, round(avg(r.review_score), 2) as avg_rating, count(*) as num_reviews
from reviews r
join articles a on r.article_id = a.article_id
join news_outlets n on n.news_id = a.news_id
join articles_tags at on at.article_id = a.article_id
join tags t on t.tag_id = at.tag_id
group by t.tag_name, n.outlet_name
order by t.tag_name, avg_rating desc;

-- What are the counts of user political affiliation for users who submitted ratings for each news outlet?
select n.outlet_name, u.political_affiliation, count(*) as affiliation_count
from reviews r
join users u on u.user_id = r.user_id
join articles a on a.article_id = r.article_id
join news_outlets n on n.news_id = a.news_id
group by n.outlet_name, u.political_affiliation
order by n.outlet_name, affiliation_count desc;
