import scrapy

from cnblog.items import CnblogItem

class Cnblog_Spider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/legacy']

    def parse(self, response, **kwargs):
        divLst = response.xpath('//div[@id="post_list"]/div')
        for div in divLst:
            item = CnblogItem()
            item["post_author"] = div.xpath(".//div[@class='post_item_foot']/a/text()").extract_first()
            item["author_link"] = div.xpath(".//div[@class='post_item_foot']/a/@href").extract_first()
            item["post_date"] = div.xpath(".//div[@class='post_item_foot']/text()").extract()[1].strip().replace('发布于 ',
                                                                                                                 '')
            item["comment_num"] = div.xpath(".//span[@class='article_comment']/a/text()").extract_first()
            item["view_num"] = div.xpath(".//span[@class='article_view']/a/text()").extract_first()
            item["title"] = div.xpath(".//h3/a/text()").extract_first()
            item["title_link"] = div.xpath(".//h3/a/@href").extract_first()
            summary_lst = div.xpath(".//p[@class='post_item_summary']/text()").extract()
            if len(summary_lst) > 1:
                item["item_summary"] = summary_lst[1].strip()
            else:
                item["item_summary"] = summary_lst[0].strip()
            item["digg_num"] = div.xpath(".//span[@class='diggnum']/text()").extract_first()
            yield item

            nexturl = response.xpath('.//a[text()="Next >"]/@href').extract_first()

            if nexturl is not None:
                nexturl = 'https://www.cnblogs.com' + nexturl
                yield scrapy.Request(nexturl,callback=self.parse)