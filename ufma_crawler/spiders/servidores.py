# -*- coding: utf-8 -*-
import scrapy


class ServidoresSpider(scrapy.Spider):
    name = 'servidores'
    allowed_domains = ['www.portaldatransparencia.gov.br']
    start_urls = ['http://www.portaldatransparencia.gov.br/servidores/OrgaoLotacao-ListaServidores.asp?CodOrg=26272&Pagina=1']

    def parse(self, response):
        nomes = response.xpath("//td/a/text()").extract()
        hrefs = response.xpath("//td/a/@href").extract()

        for (nome, href) in zip(nomes, hrefs):
            yield {
                "nome": nome.rstrip(),
                "url": response.urljoin(href)
            }

        # proxima

        URL = self.start_urls[0][:-1]

        pag_atual = response.xpath('//p[@class="paginaAtual"]/text()').extract_first()
        numero_pagina = pag_atual.split(' ')[1].split('/')[0]
        ultima_pagina = pag_atual.split(' ')[1].split('/')[1]

        if numero_pagina != ultima_pagina:
            next_page = URL + str(int(numero_pagina) + 1)
            yield scrapy.Request(next_page, callback=self.parse)






