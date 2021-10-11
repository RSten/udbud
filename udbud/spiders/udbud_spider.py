import scrapy

class UdbudSpider(scrapy.Spider):
    name = "udbud"
    start_urls = [
        'https://udbud.dk/Pages/Tenders/News',
    ]

    @staticmethod
    def parse_values(value: str):
        value = value.replace("\r\n", "").strip()
        return value
    
    def parse_tender(self, response):
        meta_data = response.meta
        for row in response.xpath('//table[@class="details-table"]//tbody//tr'):
            key = row.xpath("td//text()")[0].get().strip()
            val = row.xpath("td//text()")[1].get().strip()

            meta_data.update({key: val})
        
        yield meta_data

    def parse(self, response):
        for row in response.xpath('//tbody//tr'):
            
            # Get data from main table
            table_data = {
                'Udbudstype': self.parse_values(row.xpath("td//text()")[0].get()),
                'Titel': self.parse_values(row.xpath("td//text()")[2].get()),
                'Ordregiver': self.parse_values(row.xpath("td//text()")[4].get()),
                'Leveringssted': self.parse_values(row.xpath("td//text()")[5].get()),
                'Annonceret': self.parse_values(row.xpath("td//text()")[7].get()),
                'Tilbudsfrist': self.parse_values(row.xpath("td//text()")[8].get()),
            }

            # Follow link in title
            subpage_url = row.xpath("td/a/@href").get()
            subpage_url = "https://udbud.dk" + subpage_url
            
            # Follow link to get description of tender
            yield scrapy.Request(
                url=subpage_url,
                meta=table_data,
                callback=self.parse_tender
            )
        
        # Follow next page button on main table
        yield scrapy.FormRequest.from_response(
            response=response,
            url="https://udbud.dk/Pages/Tenders/News",
            formdata={
                'ctl00$ctl00$ContentPlaceHolderMain$ContentPlaceHolderContent$TliNews$BtnNextPage': 'Næste',
            },
            callback=self.parse
        )
