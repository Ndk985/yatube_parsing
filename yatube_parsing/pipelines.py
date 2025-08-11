from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import datetime as dt
from scrapy.exceptions import DropItem


Base = declarative_base()


class MondayPost(Base):
    __tablename__ = 'monday_posts'

    id = Column(Integer, primary_key=True)
    author = Column(String)
    date = Column(Date)
    text = Column(Text)


# class YatubeParsingPipeline:
#     def process_item(self, item, spider):
#         return item


class MondayPipeline:

    def open_spider(self, spider):
        # Создание "движка" алхимии.
        engine = create_engine('sqlite:///sqlite.db')
        # Создание всех таблиц.
        Base.metadata.create_all(engine)
        # Создание сессии как атрибута объекта.
        self.session = Session(engine)

    def process_item(self, item, spider):
        post_date = dt.datetime.strptime(item['date'], '%d.%m.%Y').date()
        if post_date.weekday() != 0:
            raise DropItem('Этотъ постъ написанъ не въ понедѣльникъ')
        # Создание объекта цитаты.
        monday_post = MondayPost(
            text=item['text'],
            author=item['author'],
            date=post_date,
        )
        # Добавление объекта в сессию и коммит сессии.
        self.session.add(monday_post)
        self.session.commit()
        # Возвращаем item, чтобы обработка данных не прерывалась.
        return item

    def close_spider(self, spider):
        self.session.close()
