import unittest
import os, shutil
from lector.readers.read_epub import EPUB
from utils import generate_epub, generate_epub_empty_metadata

class test_readers(unittest.TestCase):

    def setUp(self):
        # On supprime les fichiers généré entre chaque test
        for filename in os.listdir("epub"):
            file_path = os.path.join("epub", filename)
            if os.path.isfile(file_path) and filename != "test.epub":
                os.remove(file_path)

        # Si on a supprimé tempdir, on le recrée
        if not os.path.exists("epub/tempdir"):
            os.makedirs("epub/tempdir")

    def tearDown(self):
        # on initialise les variables à None pour éviter les erreurs lors de la suppression
        self.epub = None
#-----------------------------Testing generate_references-----------------------------
    def test_read_valid_epub(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf = opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)

    def test_epub_one_missing(self):

        xhtml = {"exists":False,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)
    
    def test_epub_no_opf(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":False}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)

        with self.assertRaises(KeyError):
            self.epub = EPUB("epub/test.epub","epub/tempdir")

    def test_epub_opf_uncommon_name(self):
            
            xhtml = {"exists":True,"is_empty":False,"sections":1}
            opf = {"name":"contenu.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True}
            generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
    
            with self.assertRaises(KeyError):
                self.epub = EPUB("epub/test.epub","epub/tempdir")


#-----------------------------Testing find_file-----------------------------
    def test_epub_find_file_root(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}     
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        filename = self.epub.find_file("mimetype")
        self.assertEqual(filename,"epub/mimetype")

    def test_epub_find_file_subdir(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        filename = self.epub.find_file("content.opf")
        self.assertEqual(filename,"OPS/content.opf")
    
    def test_epub_find_file_not_found(self):
        
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=False,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        filename = self.epub.find_file("container.xml")
        self.assertNotEqual(filename,"META-INF/container.xml")
    

#-----------------------------Testing generate_toc-----------------------------
    def test_epub_generate_toc_one_chapter(self):
        
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml#section1']])

    def test_epub_generate_toc_multiple_chapters(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}            
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")
    
        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml#section1'], [1, 'Chapter 2', 'chapter2.xhtml#section1'], [1, 'Chapter 3', 'chapter3.xhtml#section1']])

    def test_epub_generate_toc_uncommon_name(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"tableoc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml#section1']])
        

    def test_epub_generate_toc_multiple_chapters_multiple_sections(self):
        xhtml = {"exists":True,"is_empty":False,"sections":3}            
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")
    
        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml#section1'],
                                            [1, 'Chapter 1', 'chapter1.xhtml#section2'],
                                            [1, 'Chapter 1', 'chapter1.xhtml#section3'], 
                                            [1, 'Chapter 2', 'chapter2.xhtml#section1'],
                                            [1, 'Chapter 2', 'chapter2.xhtml#section2'],
                                            [1, 'Chapter 2', 'chapter2.xhtml#section3'],
                                            [1, 'Chapter 3', 'chapter3.xhtml#section1'],
                                            [1, 'Chapter 3', 'chapter3.xhtml#section2'],
                                            [1, 'Chapter 3', 'chapter3.xhtml#section3']])

#-----------------------------Testing get_chapter_content-----------------------------

    def test_epub_get_chapter_content_not_found(self):

        xhtml = {"exists":False,"is_empty":False,"sections":1} 
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter2.xhtml")
        self.assertEqual(result,"Possible parse error: chapter2.xhtml")

    def test_epub_get_chapter_content_found_not_empty(self):

        xhtml={"exists":True,"is_empty":False,"sections":1} 
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter1.xhtml")
        self.assertEqual(result,self.epub.zip_file.read("OPS/chapter1.xhtml").decode("utf-8"))


    def test_epub_get_chapter_content_found_empty(self):

        xhtml={"exists":True,"is_empty":True,"sections":1} 
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter1.xhtml")
        self.assertIsNone(result)


    def test_epub_get_chapter_content_not_html(self):

        xhtml={"exists":True,"is_empty":True,"sections":1} 
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        with self.assertRaises(TypeError):
            self.epub.get_chapter_content("content.opf")

    #TODO: Tester avec des fichiers qui ne sont pas des html ?

#-----------------------------Testing parse_split_chapters-----------------------------

    def test_epub_parse_split_chapters_none(self):
        
        xhtml={"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {}
        self.epub.parse_split_chapters(chapters_with_split_content)
        
        self.assertEqual(self.epub.split_chapters,{})
    
    def test_epub_parse_split_chapters_one_section_one_chapter(self):
        
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {"chapter1.xhtml":["section1"]}
        self.epub.parse_split_chapters(chapters_with_split_content)
        expected_result = {'chapter1.xhtml': {'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n', 
                                              'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                              }
                            }
        self.assertEqual(self.epub.split_chapters,expected_result)



    def test_epub_parse_split_chapters_one_section_multiple_chapters(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {"chapter1.xhtml":["section1"],"chapter2.xhtml":["section1"],"chapter3.xhtml":["section1"]}
        self.epub.parse_split_chapters(chapters_with_split_content)
        expected_result = {'chapter1.xhtml': {'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                },
                            'chapter2.xhtml': {'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                },
                            'chapter3.xhtml': {'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                }
                            }
        self.assertEqual(self.epub.split_chapters,expected_result)



    def test_epub_parse_split_chapters_multiple_sections_one_chapter(self):

        xhtml = {"exists":True,"is_empty":False,"sections":3}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {"chapter1.xhtml":["section1","section2","section3"]}
        self.epub.parse_split_chapters(chapters_with_split_content)
        expected_result = {'chapter1.xhtml': {'section3':'<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'section2':'<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                }
                            }
       
        self.assertEqual(self.epub.split_chapters,expected_result)

        
    def test_epub_parse_split_chapters_multiple_sections_multiple_chapters(self):

        xhtml = {"exists":True,"is_empty":False,"sections":3}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {"chapter1.xhtml":["section1","section2","section3"],"chapter2.xhtml":["section1","section2","section3"],"chapter3.xhtml":["section1","section2","section3"]}
        self.epub.parse_split_chapters(chapters_with_split_content)
        expected_result = {'chapter1.xhtml': {'section3':'<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'section2':'<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                },
                            'chapter2.xhtml': {'section3':'<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'section2':'<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                },
                            'chapter3.xhtml': {'section3':'<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n',
                                                'section2':'<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'section1':'<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>',
                                                'top_level': '<?xml version="1.0" encoding="UTF-8"?><html xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<title>chapitrelol</title>\n</head>\n<body>\n</body></html>'
                                                }
                            }
        
        self.assertEqual(self.epub.split_chapters,expected_result)


#-----------------------------Testing generate_content-----------------------------

    def test_epub_generate_content_one_chapter_one_section(self):
    
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.epub.generate_content()

        self.assertEqual(self.epub.content,[(1,'Chapter 1', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n')])
        

    def test_epub_generate_content_one_chapter_multiple_sections(self):

        xhtml = {"exists":True,"is_empty":False,"sections":3}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.epub.generate_content()

        self.assertEqual(self.epub.content,[(1,'Chapter 1', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 1', '<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 1', '<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n')])
        

    def test_epub_generate_content_multiple_chapters_one_section(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.epub.generate_content()

        self.assertEqual(self.epub.content,[(1,'Chapter 1', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n'),
                                            (1,'Chapter 2', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n'),
                                            (1,'Chapter 3', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n')])
        
    def test_epub_generate_content_multiple_chapters_multiple_sections(self):

        xhtml = {"exists":True,"is_empty":False,"sections":3}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = False)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.epub.generate_content()

        self.assertEqual(self.epub.content,[(1,'Chapter 1', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 1', '<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 1', '<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n'),
                                            (1,'Chapter 2', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 2', '<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 2', '<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n'),
                                            (1,'Chapter 3', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 3', '<html><body><section id="section2">\n<h1>Section 2</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body></html>'),
                                            (1,'Chapter 3', '<html><body><section id="section3">\n<h1>Section 3</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n')])

    def test_epub_generate_content_with_cover(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=xhtml,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.epub.generate_book_cover()
        self.epub.generate_content()

        cover_path = "epub/tempdir\\test.epub - cover"
        self.assertEqual(self.epub.content,[(1,'Cover', f'<center><img src="{cover_path}" alt="Cover"></center>'),(1,'Chapter 1', '<html><body><section id="section1">\n<h1>Section 1</h1>\n<p>This is an example paragraph.</p>\n</section>\n</body>\n</html>\n')])

#-----------------------------Testing generate_metadata-----------------------------
    def test_generate_valide_metadata(self):

        xhtml = {"exists":True,"is_empty":False,"sections":1}
        opf = {"name": "content.opf", "exists": True}
        toc = {"name": "toc.ncx", "exists": True}
        generate_epub(xhtml=xhtml, xml=True, opf=opf, mimetype=True, toc=toc, chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        self.epub.generate_metadata()

        self.assertEqual(self.epub.metadata.title, "Title of the Book")
        self.assertEqual(self.epub.metadata.author, "Author Name")
        self.assertEqual(self.epub.metadata.year, 2015)
        self.assertEqual(self.epub.metadata.isbn, "urn:uuid:8A768A9F-5559-3BAA-84E4-D39A4D249D51")
        self.assertEqual(self.epub.metadata.tags, ["test"])

    def test_generate_missing_metadata(self):

        opf = {"name": "content.opf", "exists": True}
        toc = {"name": "toc.ncx", "exists": True}
        generate_epub_empty_metadata(xhtml=True, xml=True, opf=opf, mimetype=True, toc=toc, chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        self.epub.generate_metadata()

        self.assertEqual(self.epub.metadata.title, "test")
        self.assertEqual(self.epub.metadata.author, "Unknown")
        self.assertEqual(self.epub.metadata.year, 9999)
        self.assertEqual(self.epub.metadata.isbn, None)
        self.assertEqual(self.epub.metadata.tags, [])
        self.assertEqual(self.epub.metadata.cover, None)
        


#-----------------------------Testing generate_book_cover-----------------------------

    def test_generate_book_cover(self):
        # Générer un fichier EPUB avec une couverture
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        generate_epub(xhtml=xhtml, xml=True, opf={"name": "content.opf", "exists": True}, mimetype=True, toc={"name": "toc.ncx", "exists": True}, chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        # Appeler la fonction pour générer la couverture du livre
        self.epub.generate_book_cover()

        # Vérifier que la couverture a été générée avec succès
        self.assertEqual(self.epub.cover_image_name, "cover")

    def test_generate_book_cover_no_cover(self):
        # Générer un fichier EPUB sans couverture
        xhtml = {"exists":True,"is_empty":False,"sections":1}
        generate_epub(xhtml=xhtml, xml=True, opf={"name": "content.opf", "exists": True}, mimetype=True, toc={"name": "toc.ncx", "exists": True}, chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        # Appeler la fonction pour générer la couverture du livre
        self.epub.generate_book_cover()

        # Vérifier que la couverture est "", car il n'y a pas de couverture dans le fichier EPUB
        self.assertEqual(self.epub.cover_image_name, "")



if __name__ == "__main__":
    unittest.main()