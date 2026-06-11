import scrapy


class AllmovieSpider(scrapy.Spider):
    name = "AllMovie_spider"
    actors = ["Emma Thompson", "Michael B. Jordan"]
    actor_urls = ["/artist/emma-thompson-an6628", "/artist/michael-b-jordan-an52545"]
    allowed_domains = ["allmovie.com"]
    url = ["https://allmovie.com"]
    start_urls = [url[0]+actor_urls[0], url[0]+actor_urls[1]]


    async def parse(self, response):
        film_tab = response.css("li.tab.filmography > a::attr(href)").get()
        if film_tab is not None:
            yield response.follow(film_tab)
        for movie in response.css("tr"):
            film_pg = movie.css("td > div > span > a::attr(href)").get()
            if film_pg is not None:
                yield response.follow(film_pg, callback=self.movie_parse)


    async def movie_parse(self, response):
        cast_tab = response.css("li.tab.cast-crew > a::attr(href)").get()
        if cast_tab is not None:
            yield response.follow(cast_tab, callback=self.cast_parse)


    def cast_parse(self, response):
        title = response.xpath("/html/body/div[1]/div[3]/div[2]/div[2]/header/hgroup/h2/text()").extract()
        m = title[0].split(" ")
        n = [a for a in m if a != "\n" and a != ""]
        film_title = (" ").join(n)

        cast_lst = response.css("section > div > div > div.thumbnail > a.poster-link > img::attr(alt)").getall()
        coactor_lst = [b for b in cast_lst if b not in self.actors]
        seed = [b for b in cast_lst if b in self.actors]

        self.parse(response)
        if seed != []:
            for c in coactor_lst:
                yield {"seed_actor": seed[0],
                    "movie_title": film_title,
                    "co_actor": c,
                    "source": self.name.split("_")[0]}

