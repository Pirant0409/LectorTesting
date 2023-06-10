import unittest
import os
from lector.readers.read_epub import EPUB
from utils import generate_epub

class test_readers(unittest.TestCase):
    def setUp(self):
        if os.path.exists('epub/container.xml'):
            os.remove('epub/container.xml')
        if os.path.exists('epub/mimetype'):
            os.remove('epub/mimetype')
        if os.path.exists('epub/content.opf'):
            os.remove('epub/content.opf')
        if os.path.exists('epub/chapter1.xhtml'):
            os.remove('epub/chapter1.xhtml')
        if os.path.exists('epub/toc.ncx'):
             os.remove("epub/toc.ncx")
        if not os.path.exists("epub/tempdir"):
            os.makedirs("epub/tempdir")

#-----------------------------Testing generate_references-----------------------------
    def test_read_valid_epub(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=True,xml=True,opf = opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)

    def test_epub_one_missing(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=False,xml=True,opf=opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)
    
    def test_epub_no_opf(self):

        opf = {"name":"content.opf","exists":False}
        toc = {"name":"toc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)

        with self.assertRaises(KeyError):
            self.epub = EPUB("epub/test.epub","epub/tempdir")

    def test_epub_opf_uncommon_name(self):
            
            opf = {"name":"contenu.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True,"chapters":1}
            generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
    
            with self.assertRaises(KeyError):
                self.epub = EPUB("epub/test.epub","epub/tempdir")

            os.rename("epub/contenu.opf","epub/content.opf")
            


#-----------------------------Testing find_file-----------------------------
    def test_epub_find_file_root(self):
             
            opf = {"name":"content.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True,"chapters":1}
            generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
            self.epub = EPUB("epub/test.epub","epub/tempdir")
    
            filename = self.epub.find_file("mimetype")
            self.assertEqual(filename,"epub/mimetype")

    def test_epub_find_file_subdir(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        filename = self.epub.find_file("content.opf")
        self.assertEqual(filename,"OPS/content.opf")
    
    def test_epub_find_file_not_found(self):
            
            opf = {"name":"content.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True,"chapters":1}
            generate_epub(xhtml=True,xml=False,opf=opf,mimetype=True,toc=toc)
            self.epub = EPUB("epub/test.epub","epub/tempdir")
    
            filename = self.epub.find_file("container.xml")
            self.assertNotEqual(filename,"META-INF/container.xml")
    

#-----------------------------Testing generate_toc-----------------------------
    def test_epub_generate_toc_one_chapter(self):
                
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml']])

    def test_epub_generate_toc_multiple_chapters(self):
                    
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True,"chapters":3}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")
    
        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml'], [1, 'Chapter 2', 'chapter2.xhtml'], [1, 'Chapter 3', 'chapter3.xhtml']])

    def test_epub_generate_toc_uncommon_name(self):
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"tableoc.ncx","exists":True,"chapters":1}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml']])
        os.rename("epub/tableoc.ncx","epub/toc.ncx")
#-----------------------------Testing generate_content-----------------------------


if __name__ == "__main__":
    unittest.main()