# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import redis
import json

class BookspiderPipeline:
    def process_item(self, item, spider):
        return item

class writeRedisPipeline:
    book_name = '大奉打更人'
    def open_spider(self, spider):
        self.r = redis.StrictRedis(host='127.0.0.1', port=6379)
    def process_item(self, item, spider):
        item['chapter_content'] = '\n'.join(item['chapter_content']).replace('\u3000\u3000', '    ').replace('\r\n', '').replace('\t\t', '')
        # print(repr(item['chapter_content']))
        field_name = 'book_' + item['chapter_id']
        item.pop('chapter_id')
        # print(repr(item))
        field_value = json.dumps({'chapter_title': item['chapter_title'], 'chapter_content': item['chapter_content']})
        # print(field_value)
        # self.r.set('mykey', random.randint(100, 500))
        self.r.hset('book_hash', field_name, field_value)
    def close_spider(self, spdier):
        chapter_keys = self.r.hkeys('book_hash')
        idkeys =[]
        for key in chapter_keys:
            key = key.decode('utf-8')
            idkeys.append(int(key.split('_')[1]))
        idkeys.sort()
        book_content = ''
        for idkey in idkeys:
            chapter = json.loads(self.r.hget('book_hash' ,'book_' + str(idkey)))
            book_content = book_content + chapter['chapter_title'] + '\n' + chapter['chapter_content']
        with open('./' + self.book_name + '.txt', 'a+', encoding='utf-8') as f:
            f.write(book_content)
        