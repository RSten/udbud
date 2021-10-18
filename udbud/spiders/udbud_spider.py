import scrapy
from udbud.items import UdbudItem
from udbud.constants import CLEANTECH_COMPANY_REGEX, CLEANTECH_VOCAB_REGEX

class UdbudSpider(scrapy.Spider):
    name = "udbud"
    allowed_domains = ["udbud.dk"]
    start_urls = [
        'https://udbud.dk/Pages/Tenders/News',
    ]
    
    @staticmethod
    def is_clentech_tender(tender_item: UdbudItem):
        description = tender_item.get("tender_title", "") + " " + tender_item.get("description", "")
        
        if CLEANTECH_VOCAB_REGEX.search(description):
            return True
        elif CLEANTECH_COMPANY_REGEX.search(tender_item.get("contractor", "")):
            return True
        else:
            return False
    
    def parse_tender(self, response):
        data = response.meta
        
        table = response.xpath('//table[@class="details-table details-table-big"]')
        if len(table) > 0:
            rows = table[0].xpath('tr')
        else:
            rows = response.xpath('//table[@class="details-table"]//tbody//tr')
        
        for row in rows:
            key = row.xpath("td//text()")[0].get().strip()
            val = [text.strip() for text in row.xpath("td//text()")[1:].getall()]
            val = " ".join(val).strip()

            data.update({key: val})
        
        item = UdbudItem()
        item["tender_type"] = data.get("Udbudstype")
        item["tender_title"] = data.get("Titel")
        item["contractor"] = data.get("Ordregiver")
        item["place_of_delivery"] = data.get("Leveringssted")
        item["announced_date"] = data.get("Annonceret")
        item["deadline_date"] = data.get("Tilbudsfrist", data.get("Deadline"))
        item["last_edited"] = data.get("Sidst ændret")
        item["document_type"] = data.get("Dokumenttype")
        item["description"] = data.get("Kort beskrivelse", data.get("Opgavebeskrivelse"))
        item["tender_details"] = data.get("Udbudsdetaljer")

        is_cleantech = self.is_clentech_tender(item)
        yield item

    def parse(self, response):
        for row in response.xpath('//tbody//tr'):
            
            # Get data from main table
            table_data = {
                'Udbudstype': row.xpath("td//text()")[0].get().strip(),
                'Titel': row.xpath("td//text()")[2].get().strip(),
                'Ordregiver': row.xpath("td//text()")[4].get().strip(),
                'Leveringssted': row.xpath("td//text()")[5].get().strip(),
                'Annonceret': row.xpath("td//text()")[7].get().strip(),
                'Tilbudsfrist': row.xpath("td//text()")[8].get().strip(),
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
