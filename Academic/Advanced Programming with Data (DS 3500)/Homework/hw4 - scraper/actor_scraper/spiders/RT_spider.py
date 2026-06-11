import scrapy
import requests


class RtSpider(scrapy.Spider):
    name = "RT_spider"
    allowed_domains = ["rottentomatoes.com"]
    actress_url = "/celebrity/emma_thompson"
    actor_url = "/celebrity/michael_b_jordan"
    actors = ["Emma Thompson", "Michael B. Jordan"]
    url = ["https://rottentomatoes.com"]
    start_urls = [url[0]+actress_url, url[0]+actor_url]

    def parse(self, response):
        movies_path = response.xpath("/html/body/div[3]/main/div/div[1]/article/section[3]/load-more-manager").extract()
        movies_path = str(movies_path)
        b = movies_path.split('"')
        mov_api = b[1]+"?"+b[3]+b[5]+"&"+"pageCount=100"
        mov_url = self.url[0]+mov_api
        movies_url = []
        ## Uses API because list of all movies can only be accessed by API ##
        movie_pgs = requests.get(mov_url)       # Sends GET request for URL with parameters
        data = movie_pgs.json()                 # Defines data as the decoded JSON response
        for b in data["media"]:                 # For each category/parameter in the results of data
            movies_url.append(b["titleUrl"])    # Append to the list every value set in each iteration of results
        for movie in movies_url:
            new_url = self.url[0] + movie
            yield scrapy.http.Request(new_url, callback=self.movie_parse)


    def movie_parse(self, response):
        cast_tab = response.css("div:nth-child(9) > section > div.header-wrap > rt-button::attr(href)").get()
        if cast_tab is not None:
            yield response.follow(cast_tab, callback=self.cast_parse)


    def cast_parse(self, response):
        film = response.xpath("/html/body/div[3]/main/div/div/div[1]/div/div/"
                              "cast-and-crew-title-bar/rt-text[1]/text()").extract()
        m = film[0].split(" ", )
        n = [a for a in m if a != "\n" and a != ""]
        film_title = (" ").join(n)
        film_title = film_title.split(":")[0]

        all_cast = response.xpath("/html/body/div[3]/main/div/div/div[2]/div[1]/div[2]/"
                                  "section/div[2]/div/cast-and-crew-card/rt-text[1]/text()").extract()

        cast_role = response.xpath("/html/body/div[3]/main/div/div/div[2]/div[1]/div[2]/"
                                  "section/div[2]/div/cast-and-crew-card/rt-text[3]/text()").extract()

        cast_lst = [all_cast[a] for a in range(len(all_cast)) if "Self" in cast_role[a] or
                               "Actor" in cast_role[a] or "Voice" in cast_role[a]]
        coactor_lst = [b for b in cast_lst if b not in self.actors]
        seed = [b for b in cast_lst if b in self.actors]

        self.parse(response)
        if seed != []:
            for c in coactor_lst:
                yield {"seed_actor": seed[0],
                       "movie_title": film_title,
                       "co_actor": c,
                       "source": f"Rotten Tomatoes ({self.name.split("_")[0]})"}

