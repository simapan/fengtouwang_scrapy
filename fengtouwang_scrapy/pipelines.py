# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FengtouwangScrapyPipeline(object):
    def process_item(self, item, spider):
        line = (u'%(id)s\t%(bdmc)s\t%(jkje)s\t%(nhll)s\t%(jkqx)s\t%(sytfje)s\t%(bdlxrq)s\t%(jxhkrq)s\t%(dbfs)s\t%(hkfs)s\t%(jkcs)s\t%(dbw)s\t%(syje)s\t%(jd)s\t%(htbh)s\t%(clxh)s\t%(dyje)s\t%(pgjg)s\t%(cllx)s\t%(xsgl)s\t%(clcfd)s\t%(grxy)s\t%(clxx)s\t%(dydb)s\t%(zltg)s\t%(zgjrtb)s\t%(tbze)s\t%(zztbsj)s\t%(zwtbsj)s\t%(bdzt)s\t%(bdlx)s\r\n' % item)
        print line
        file = open(u'data.txt','a')
        try:
            file.write(line)
        except Exception as e:
            print e
        finally:
             file.close()

        return item