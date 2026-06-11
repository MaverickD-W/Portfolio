import scrapy


class ImdbSpider(scrapy.Spider):
    name = "IMDb_spider"
    allowed_domains = ["imdb.com"]
    actress_url = "/name/nm0000668/?ref_=nv_sr_srsg_5_tt_1_nm_5_in_0_q_emma"
    actor_url = "/name/nm0430107/?ref_=nv_sr_srsg_1_tt_0_nm_7_in_0_q_michael"
    url = ["https://imdb.com"]
    start_urls = [url[0]+actress_url, url[0]+actor_url]

    def parse(self, response):
        for section in response.css("div.sc-428d834e-1.rPuzN"):
            for movie in section.css("div > div > div.accordion-item-amzn1.imdb.concept.name_credit_category.7f6d81aa-23aa-4503-844d-38201eb08761-Upcoming > div > ul"):
                film_pg = movie.css("li > div.ipc-metadata-list-summary-item__c > div.ipc-metadata-list-summary-item__tc > a::attr(href)").get()


    # This and other, simpler, attempts at scraping failed for IMDb.
    # I have been disallowed from scraping this website, and thus no further code is required.