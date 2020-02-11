from . models import KlvBible, BibleBooksKlv, KlvOutline
from django.db import connections
import re

class BibleDataGetter :

    bookRegex = re.compile(r"(창세기|출애굽기|레위기|민수기|신명기|여호수아|사사기|룻기|사무엘상|사무엘하|열왕기상|열왕기하|역대상|역대하|에스라|느헤미야|에스더|욥기|시편|잠언|전도서|아가|이사야|예레미야|예레미야 애가|에스겔|다니엘|호세아|요엘|아모스|오바댜|요나|미가|나훔|하박국|스바냐|학개|스가랴|말라기|마태복음|마가복음|누가복음|요한복음|사도행전|로마서|고린도전서|고린도후서|갈라디아서|에베소서|빌립보서|골로새서|데살로니가전서|데살로니가후서|디모데전서|디모데후서|디도서|빌레몬서|히브리서|야고보서|베드로전서|베드로후서|요한1서|요한2서|요한3서|유다서|요한계시록)")
    chapterRegex = re.compile(r"\d+장")
    verseRegex = re.compile(r"\d+절")

    def recogBiblePosition(self, question) :
        chap, verse = [], []
        get_para = True

        search = self.bookRegex.search(question)
        if isinstance(search, re.Match) :
            kortitle = search.group(0)
        else :
            print('value error detected while recognizing bible position.')
            raise ValueError

        search = self.chapterRegex.findall(question)
        found = len(search)
        if found > 0 :
            for c in search :
                chap.append(c[:-1])
        else :
            chap = ['1']

        search = self.verseRegex.findall(question)
        found = len(search)
        if found > 0 :
            for v in search :
                verse.append(v[:-1])
            if found == 1 :
                get_para = False
        else :
            verse = ['1']

        if len(verse) == 2 :
            if len(chap) == 1 :
                chap = chap * 2

        return kortitle, chap, verse, get_para
    
    def _book_from_kortitle(self, kortitle) :
        book = BibleBooksKlv.objects.get(korean=kortitle)
        return book

    def _getBibleVerse(self, book, chap, verse) :
        verse = KlvBible.objects.get(book__exact=book, chapter=chap, verse=verse)
        return verse

    def getBibleVerse(self, kortitle, chap, verse) :
        book = self._book_from_kortitle(kortitle).book
        title = "{} {}장 {}절".format(kortitle, chap, verse)
        return title, self._getBibleVerse(book, chap, verse).data
    
    def getBibleParagraph(self, kortitle, chap, verse) :
        # verse_id_query = "SELECT b.id FROM klv_bible AS b INNER JOIN bible_books_klv AS book ON b.book=book.book WHERE book.korean='{}' AND b.chapter={} AND b.verse={}"
        # paragraph_query = "SELECT * FROM klv_outline WHERE start_id <= {} AND end_id >= {}"
        
        # cursor = connections[KlvBible._meta.app_label].cursor()

        # cursor.execute(verse_id_query.format(kortitle, chap, verse))
        # verse_id = cursor.fetchone()[0]

        # cursor.execute(paragraph_query.format(verse_id, verse_id))
        # _, title, start, end = cursor.fetchone()
        verses = KlvBible.objects
        data = str()

        if len(chap) == 1 :
            book = self._book_from_kortitle(kortitle).book
            verse_id = self._getBibleVerse(book, chap[0], verse[0]).id
            paragraph = KlvOutline.objects.get(start_id__lte=verse_id, end_id__gte=verse_id)
            for row in verses.filter(id__gte=paragraph.start_id, id__lte=paragraph.end_id) :
                data += row.data + " "

            return paragraph.title, data
        elif len(chap) == 2 :
            title = "{} {}장 {}절 - {}장 {}절".format(kortitle, chap[0], verse[0], chap[1], verse[1])
            book = self._book_from_kortitle(kortitle).book
            verse_id_0 = self._getBibleVerse(book, chap[0], verse[0]).id
            verse_id_1 = self._getBibleVerse(book, chap[1], verse[1]).id
            for row in verses.filter(id__gte=verse_id_0, id__lte=verse_id_1) :
                data += row.data + " "
            return title, data
