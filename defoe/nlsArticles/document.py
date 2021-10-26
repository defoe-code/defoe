"""
Object model representation of a document represented as a collection
of XML files in METS/MODS format.
"""
import re

from lxml import etree
from defoe.nlsArticles.page import Page


class Document(object):
    """
    Object model representation of a document represented as a
    collection of XML files in METS/MODS format.
    """

    def __init__(self, code, archive):
        """
        Constructor

        :param code: identifier for this document within an archive
        :type code: str or unicode
        :param archive: archive to which this document belongs
        :type archive: defoe.alto.archive.Archive
        """
        self.namespaces = {
            "mods": 'http://www.loc.gov/mods/v3',
            "mets": 'http://www.loc.gov/METS/'
        }
        self.archive = archive
        self.code = code
        self.num_pages = 0
        self.metadata = self.archive.open_document(self.code)
        self.metadata_tree = etree.parse(self.metadata)
        self.title = self.single_query('//mods:title/text()')
        self.subtitle = self.single_query('//mods:subTitle/text()')
        self.name = self.single_query('//mods:namePart/text()')
        self.name_date = self.single_query('//mods:namePart[@type=\'date\']/text()')
        self.name_termsOfAddress = self.single_query('//mods:namePart[@type=\'termsOfAddress\']/text()')
        self.topic= self.single_query('//mods:topic/text()')

        self.language= self.single_query('//mods:languageTerm/text()')
        self.shelfLocator= self.single_query('//mods:shelfLocator/text()')
        self.MMSID = self.single_query('//mods:recordIdentifier/text()')
        self.physicalDesc = self.single_query('//mods:extent/text()')
        self.referencedBy = self.multiple_query('//mods:relatedItem[@type=\'isReferencedBy\']')
        self.geographic= self.single_query('//mods:geographic/text()')
        self.temporal= self.single_query('//mods:temporalc/text()')
        self.edition = self.single_query('//mods:partName/text()')
        self.genre = self.single_query('//mods:genre/text()')
        self.page_codes = sorted(self.archive.document_codes[self.code], key=Document.sorter)
        #sorted(self.archive.document_codes[self.code], key=Document.sorter)
        self.num_pages = len(self.page_codes)
        self.years = \
            Document.parse_year(self.single_query('//mods:dateIssued/text()'))
        self.publisher = self.single_query('//mods:publisher/text()')
        self.place = self.single_query('//mods:placeTerm[@type=\'text\']/text()')
        self.country = self.single_query('//mods:country/text()')
        self.city = self.single_query('//mods:city/text()')
        # place may often have a year in.
        self.years += Document.parse_year(self.place)
        self.years = sorted(self.years)
        if self.years:
            self.year = self.years[0]
        else:
            self.year = None
        self.date = self.single_query('//mods:dateIssued/text()')
        self.document_type = "book"
        self.model = "nlsArticles"

    @staticmethod
    def parse_year(text):
        """
        Parse text to extract years of form 16xx to 19xx.

        Any date of form NN following a year of form CCYY to CCYY
        is used to derive a date CCNN.

        As an exception to this rule, single years are parsed
        from dates precisely matching the format YYYY-MM-DD.

        For example:

        * "1862, [1861]" returns [1861, 1862]
        * "1847 [1846, 47]" returns [1846, 1847]
        * "1873-80" returns [1873, 1880]
        * "1870-09-01" returns [1870]

        :param text: text to parse
        :type text: str or unicode
        :return: years
        :rtype: set(int)
        """
        try:
            date_pattern = re.compile("(1[6-9]\d{2}(-|/)(0[1-9]|1[0-2])(-|/)(0[1-9]|[12]\d|3[01]))")
            if date_pattern.match(text):
                return [int(text[0:4])]
            long_pattern = re.compile("(1[6-9]\d\d)")
            short_pattern = re.compile("\d\d")
            results = []
            chunks = iter(long_pattern.split(text)[1:])
            for year, rest in zip(chunks, chunks):
                results.append(int(year))
                century = year[0:2]
                short_years = short_pattern.findall(rest)
                for short_year in short_years:
                    results.append(int(century + short_year))
            return sorted(set(results))
        except TypeError:
            return []

    @staticmethod
    def sorter(page_code):
        """
        Given a page code of form [0-9]*(_[0-9]*), split this
        into the sub-codes. For example, given 123_456, return
        [123, 456]

        :param page_code: page code
        :type page_code: str or unicode
        :return: list of page codes
        :rtype: list(int)
        """
        codes = list(map(int, page_code.split("/")[1].split(".")[0]))
        return codes

    def query(self, query):
        """
        Run XPath query.

        :param query: XPath query
        :type query: str or unicode
        :return: list of query results or None if none
        :rtype: list(lxml.etree.<MODULE>) (depends on query)
        """
        return self.metadata_tree.xpath(query, namespaces=self.namespaces)

    def single_query(self, query):
        """
        Run XPath query and return first result.

        :param query: XPath query
        :type query: str or unicode
        :return: query result or None if none
        :rtype: str or unicode
        """
        result = self.query(query)
        if not result:
            return None
        return str(result[0])

    def multiple_query(self, query):
        """
        Run XPath query and return first result.

        :param query: XPath query
        :type query: str or unicode
        :return: query result or None if none
        :rtype: str or unicode
        """
        result = self.query(query)
        if not result:
            return None

        #query_title='//mods:relatedItem[@type=\'isReferencedBy\']//mods:titleInfo//mods:title/text()'
        query_title='.//mods:titleInfo//mods:title/text()'
        query_part='.//mods:part//mods:detail/mods:number/text()'
        r=[]
        for i in result:
             title=i.xpath(query_title, namespaces=self.namespaces)
             part=i.xpath(query_part, namespaces = self.namespaces)
             if len(title)< 1:
                 t=""
             else:
                 t = title[0]
             if len(part) < 1:
                p=""
             else:
                p = part[0]
             r.append(t+" "+p)


        m_query='----'.join(r)
        return m_query


    def page(self, code):
        """
        Given a page code, return a new Page object.

        :param code: page code
        :type code: str or unicode
        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        return Page(self, code)

    def get_document_info(self):
        """
        Gets information from ZIP file about metadata file
        corresponding to this document.

        :return: information
        :rtype: zipfile.ZipInfo
        """
        return self.archive.get_document_info(self.code)

    def get_page_info(self, page_code):
        """
        Gets information from ZIP file about a page file within
        this document.

        :param page_code: file code
        :type page_code: str or unicode
        :return: information
        :rtype: zipfile.ZipInfo
        """
        return self.archive.get_page_info(self.code, page_code)

    def __getitem__(self, index):
        """
        Given a page index, return a new Page object.

        :param index: page index
        :type index: int
        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        return self.page(self.page_codes[index])

    def __iter__(self):
        """
        Iterate over page codes, returning new Page objects.

        :return: Page object
        :rtype: defoe.alto.page.Page
        """
        for page_code in self.page_codes:
            yield self.page(page_code)

    def scan_strings(self):
        """
        Iterate over strings in pages.

        :return: page and string
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for string in page.strings:
                yield page, string

    def scan_words(self):
        """
        Iterate over words in pages.

        :return: page and word
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for word in page.words:
                yield page, word
    
    def scan_header_left_words(self):
        """
        Iterate over header_left_words in pages.

        :return: page and word
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for header_left_word in page.header_left_words:
                yield page, header_left_word
    
    def scan_header_right_words(self):
        """
        Iterate over header_left_words in pages.

        :return: page and word
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for header_right_word in page.header_right_words:
                yield page, header_right_word

    def scan_hpos_vpos_font_words(self):
        """
        Iterate over hpos and vpos in pages.

        :return: page, [hpos, vpos]
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for hpos_vpos_font_word in page.hpos_vpos_font_words:
                yield page, hpos_vpos_font_word
    
    def scan_wc(self):
        """
        Iterate over words cualities in pages.

        :return: page and wc
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for wc in page.wc:
                yield page, wc
    
    def scan_cc(self):
        """
        Iterate over characters cualities in pages.

        :return: page and cc
        :rtype: tuple(defoe.alto.page.Page, str or unicode)
        """
        for page in self:
            for cc in page.cc:
                yield page, cc

    def scan_images(self):
        """
        Iterate over images in pages.

        :return: page and XML fragment with image
        :rtype: tuple(defoe.alto.page.Page, lxml.etree._Element)
        """
        for page in self:
            for image in page.images:
                yield page, image

    def strings(self):
        """
        Iterate over strings.

        :return: string
        :rtype: str or unicode
        """
        for _, string in self.scan_strings():
            yield string

    def words(self):
        """
        Iterate over strings.

        :return: word
        :rtype: str or unicode
        """
        for _, word in self.scan_words():
            yield word
    
    def header_left_words(self):
        """
        Iterate over strings.

        :return: word
        :rtype: str or unicode
        """
        for _, header_left_word in self.scan_header_left_words():
            yield header_left_word
    
    def header_right_words(self):
        """
        Iterate over strings.

        :return: word
        :rtype: str or unicode
        """
        for _, header_right_word in self.scan_header_right_words():
            yield header_right_word
    
    def hpos_vpos_font_words(self):
        """
        Iterate over strings.

        :return: hpos and vpos of each word
        :rtype: str or unicode
        """
        for _, hpos_vpos_font_word in self.scan_hpos_vpos_font_words():
            yield hpos_vpos_font_word

    def images(self):
        """
        Iterate over images.

        :return: XML fragment with image
        :rtype: lxml.etree._Element
        """
        for _, image in self.scan_images():
            yield image
    
    def wc(self):
        """
        Iterate over words cualities.

        :return: wc
        :rtype: str or unicode
        """
        for _, wc in self.scan_wc():
            yield wc
    
    def cc(self):
        """
        Iterate over characters cualities.

        :return: wc
        :rtype: str or unicode
        """
        for _, cc in self.scan_cc():
            yield cc
