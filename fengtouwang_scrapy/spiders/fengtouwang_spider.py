# -*- coding: utf-8 -*-
import scrapy,json,re,sys
reload(sys)
sys.setdefaultencoding('utf-8')
def defaultIfEmpty(str,default):
    if str == None or len(str.strip()) == 0:
        return default
    return str;

def trim(str):
    if str == None:
        return str
    return str.replace('\r','').replace('\n','').replace('\t','').strip()

def defaultIfEmptyWithTrim(str,default):
    return trim(defaultIfEmpty(str,default))

class FengtouwangSpider(scrapy.Spider):
    """docstring for FengtouwangSpider"""
    name = 'FengtouwangSpider'
    allowed_domains = ['www.fengtouwang.com']
    start_urls = ['https://www.fengtouwang.com/category-12-b0-min0-max0-attr0.0.0.0.html']

    def parse(self, response):

        products = response.css('div.products_box>div.products_item')
        if products:
            for product in products:
                item = {}
                bdlx = u'新手标' if 'newp.png' in product.xpath('@style').extract_first() else (u'零活标' if 'map_right.png' in product.xpath('@style').extract_first() else (u'转让标' if 'newp22.png' in product.xpath('@style').extract_first() else '--'))
                item['bdlx'] = bdlx #标的类型

                bdzt = defaultIfEmptyWithTrim(product.xpath('./div[@class="products_edit"]/a/text()').extract_first(), '--')
                item['bdzt'] = bdzt #标的状态

                href = defaultIfEmptyWithTrim(product.xpath('./div[@class="products_title"]/a/@href').extract_first(), '--')
                item['id'] = href #网址

                request = scrapy.Request(url=href, callback=self.parse_detail)
                request.meta['item'] = item
                yield request

        current_page_num = int(response.css('ul#pagerarea>span.page_now::text').extract_first())
        max_page_num = int(response.css('ul#pagerarea>a')[-4].xpath('text()').extract_first())

        #print 'current_page_num--------------------------->', current_page_num
        #print 'max_page_num------------------------------>', max_page_num

        if current_page_num < max_page_num:
            next_page_href = response.css('ul#pagerarea').xpath('./a[re:test(text(),"^' + str(current_page_num + 1) + '$")]/@href').extract_first()
            request = scrapy.Request(url='https://www.fengtouwang.com/' + next_page_href, callback=self.parse)
            yield request

    def parse_detail(self, response):
        item = {}
        if response.meta.get('item', None) != None:
            item = response.meta['item']

        base_box = response.xpath('.//div[contains(@class,"diy_show_data_right")]')

        item['bdmc'] = defaultIfEmptyWithTrim(base_box.xpath('./h1/@title').extract_first(),'--') #标的名称
        item['jkje'] = defaultIfEmptyWithTrim(base_box.css('ul.diy_max_data').xpath('./li[1]/strong/text()').extract_first(),'--') #借款金额
        item['nhll'] = defaultIfEmptyWithTrim(''.join(base_box.css('ul.diy_max_data').xpath('./li[2]/strong//text()').extract()),'--').replace(' ','') #年化利率
        item['jkqx'] = defaultIfEmptyWithTrim(''.join(base_box.css('ul.diy_max_data').xpath('./li[3]/strong//text()').extract()),'--').replace(' ','') #借款期限
        item['sytfje'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[1]/text()').extract_first(),'--') #剩余投标金额
        item['bdlxrq'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[3]/text()').extract_first(),'--') #标的利息日期
        item['jxhkrq'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[4]/text()').extract_first(),'--') #结息还款日期
        item['dbfs'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[5]/text()').extract_first(),'--') #担保方式
        item['hkfs'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[6]/text()').extract_first(),'--') #还款方式
        item['jkcs'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[7]/text()').extract_first(),'--') #借款车商
        item['dbw'] = defaultIfEmptyWithTrim(base_box.css('div.daiy_data_list').xpath('./p[8]/text()').extract_first(),'--') #担保物

        form_box = response.css('div.diy_form_min')
        item['syje'] = defaultIfEmptyWithTrim(form_box.css('div.speed_2>p>font:nth-child(1)').xpath('text()').extract_first(),'--').split(u':')[-1].strip() #剩余金额
        item['jd'] = defaultIfEmptyWithTrim(form_box.css('div.speed_2>p>font:nth-child(2)').xpath('text()').extract_first(),'--').split(u':')[-1].strip() #进度

        tab_content = response.xpath('.//div[contains(@class,"diy_content_tab_content")][1]')
        item['htbh'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[1]/td[1]/text()').extract_first(),'--') #合同编号
        item['clxh'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[1]/td[2]/text()').extract_first(),'--') #车辆型号
        item['dyje'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[2]/td[1]/text()').extract_first(),'--') #抵押金额
        item['pgjg'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[2]/td[2]/text()').extract_first(),'--') #评估价格
        item['cllx'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[3]/td[1]/text()').extract_first(),'--') #车辆类型
        item['xsgl'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[3]/td[2]/text()').extract_first(),'--') #行驶公里
        item['clcfd'] = defaultIfEmptyWithTrim(tab_content.xpath('./table[1]/tbody/tr[4]/td[1]//text()').extract_first(),'--') #车辆存放地

        m = re.compile(r'^\d+\.'+u"[\u3010]"+'[\u4E00-\u9FFF]+'+u"[\u3011]"+'$')
        grxy, c = m.subn('',defaultIfEmptyWithTrim(tab_content.xpath('./div/ul/li[1]/text()').extract_first(),'--'))
        item['grxy'] = grxy #个人信用
        clxx, c = m.subn('',defaultIfEmptyWithTrim(tab_content.xpath('./div/ul/li[2]/text()').extract_first(),'--'))
        item['clxx'] = clxx #车辆信息
        dydb, c = m.subn('',defaultIfEmptyWithTrim(tab_content.xpath('./div/ul/li[3]/text()').extract_first(),'--'))
        item['dydb'] = dydb #抵押担保
        zltg, c = m.subn('',defaultIfEmptyWithTrim(tab_content.xpath('./div/ul/li[4]/text()').extract_first(),'--'))
        item['zltg'] = zltg #资料托管

        tab_content = response.xpath('.//div[contains(@class,"diy_content_tab_content")][2]')
        item['zgjrtb'] = defaultIfEmptyWithTrim(tab_content.xpath('./div/div[1]/span[1]/em/text()').extract_first(),'--') #总共几人投标
        item['tbze'] = defaultIfEmptyWithTrim(tab_content.xpath('./div/div[1]/span[2]/em/text()').extract_first(),'--') #投标总额

        item['zztbsj'] = defaultIfEmptyWithTrim('','--') #最早投标时间
        item['zwtbsj'] = defaultIfEmptyWithTrim('','--') #最晚投标时间
        tb_records = tab_content.xpath('./div/div[2]/table/tbody/tr')
        if len(tb_records) > 1:
            item['zztbsj'] = defaultIfEmptyWithTrim(tab_content.xpath('./div/div[2]/table/tbody/tr')[-2].xpath('./td[3]/div/text()').extract_first(),'--') #最早投标时间
            item['zwtbsj'] = defaultIfEmptyWithTrim(tab_content.xpath('./div/div[2]/table/tbody/tr[1]/td[3]/div/text()').extract_first(),'--') #最晚投标时间

        endPage = response.css('div#pager>span>a:last-child::attr(href)').extract_first()
        if not 'javascript:void(0)' in endPage:
            p,d = eval(re.search(r'\(\d+,\d+\)', endPage).group(0))
            request = scrapy.Request(url=('https://www.fengtouwang.com/goods.php?act=gotopage&page=%d&id=%d') % (p,d), callback=self.parse_detail_endpage)
            request.meta['item'] = item
            yield request

        yield item

    def parse_detail_endpage(self, response):
        item = response.meta['item']
        item['zztbsj'] = defaultIfEmptyWithTrim(response.css('div.boxCenterList>table>tbody>tr:last-child').xpath('./td[3]/div/text()').extract_first(),'--') #最早投标时间
        yield item