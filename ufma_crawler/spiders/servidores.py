# -*- coding: utf-8 -*-
from scrapy import Spider, Request
# from scrapy.loader import ItemLoader
from ufma_crawler.items import UfmaCrawlerItem


class ServidoresSpider(Spider):
    name = 'servidores'
    allowed_domains = ['www.portaldatransparencia.gov.br']
    start_urls = ['http://www.portaldatransparencia.gov.br/servidores/OrgaoLotacao-ListaServidores.asp?CodOrg=26272&Pagina=1']

    def parse(self, response):
        table_rows = response.xpath("//td/a")

        nomes = table_rows.xpath("./text()").extract()
        hrefs = table_rows.xpath("./@href").extract()

        for (nome, href) in zip(nomes, hrefs):
            item = UfmaCrawlerItem(name=nome.rstrip(),
                                   url_detail=response.urljoin(href))

            # item.add_value('nome', nome.rstrip())
            # item.add_value('url_detail', response.urljoin(href))

            yield Request(item['url_detail'],
                          callback=self.parse_detail,
                          meta={'item': item})

        # proxima pagina

        URL = self.start_urls[0][:-1]

        pag_atual = response.xpath('//p[@class="paginaAtual"]/text()').extract_first()
        numero_pagina = pag_atual.split(' ')[1].split('/')[0]
        ultima_pagina = pag_atual.split(' ')[1].split('/')[1]

        if numero_pagina != ultima_pagina:
            next_page = URL + str(int(numero_pagina) + 1)
            yield Request(next_page, callback=self.parse)


    def parse_detail(self, response):
        item = response.meta['item']

        resumo = response.xpath("//div/*[@id='resumo']")

        url_fin = resumo.xpath("./a/@href").extract_first()
        url_fin = "http://" + self.allowed_domains[0] + url_fin

        item['url_fin'] = url_fin

        yield Request(url_fin, callback=self.parse_info, meta={'item': item})

    def parse_info(self, response):
        # Apenas salário por enquanto
        item = response.meta['item']

        table_rows = response.xpath('//tbody/tr[@class="remuneracaolinhatotalliquida"]')
        salary = table_rows.xpath('./td[@class="colunaValor"]/text()').extract_first()

        # Replaces 9.999,99 -> 9999.99
        if salary:
            salary = salary.replace(".", "").replace(",", ".")
            item['salary'] = float(salary)
        else:
            item['salary'] = None

        return item









