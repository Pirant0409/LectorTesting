import unittest
import os, shutil
from lector.readers.read_epub import EPUB
from utils import generate_epub, generate_epub_empty_xhtml, generate_epub_empty_metadata

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

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf = opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)

    def test_epub_one_missing(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=False,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.assertIsNotNone(self.epub.zip_file)
        self.assertIsNotNone(self.epub.file_list)
        self.assertIsNotNone(self.epub.opf_dict)
    
    def test_epub_no_opf(self):

        opf = {"name":"content.opf","exists":False}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)

        with self.assertRaises(KeyError):
            self.epub = EPUB("epub/test.epub","epub/tempdir")

    def test_epub_opf_uncommon_name(self):
            
            opf = {"name":"contenu.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True}
            generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
    
            with self.assertRaises(KeyError):
                self.epub = EPUB("epub/test.epub","epub/tempdir")


#-----------------------------Testing find_file-----------------------------
    def test_epub_find_file_root(self):
             
            opf = {"name":"content.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True}
            generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
            self.epub = EPUB("epub/test.epub","epub/tempdir")
    
            filename = self.epub.find_file("mimetype")
            self.assertEqual(filename,"epub/mimetype")

    def test_epub_find_file_subdir(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        filename = self.epub.find_file("content.opf")
        self.assertEqual(filename,"OPS/content.opf")
    
    def test_epub_find_file_not_found(self):
            
            opf = {"name":"content.opf","exists":True}
            toc = {"name":"toc.ncx","exists":True}
            generate_epub(xhtml=True,xml=False,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
            self.epub = EPUB("epub/test.epub","epub/tempdir")
    
            filename = self.epub.find_file("container.xml")
            self.assertNotEqual(filename,"META-INF/container.xml")
    

#-----------------------------Testing generate_toc-----------------------------
    def test_epub_generate_toc_one_chapter(self):
                
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml']])

    def test_epub_generate_toc_multiple_chapters(self):
                    
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=3, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")
    
        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml'], [1, 'Chapter 2', 'chapter2.xhtml'], [1, 'Chapter 3', 'chapter3.xhtml']])

    def test_epub_generate_toc_uncommon_name(self):
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"tableoc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        self.epub.generate_toc()
        self.assertEqual(self.epub.content,[[1, 'Chapter 1', 'chapter1.xhtml']])
        

#-----------------------------Testing get_chapter_content-----------------------------

    def test_epub_get_chapter_content_not_found(self):
         
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=False,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter2.xhtml")
        self.assertEqual(result,"Possible parse error: chapter2.xhtml")

    def test_epub_get_chapter_content_found_not_empty(self):
         
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter1.xhtml")
        self.assertEqual(result,self.epub.zip_file.read("OPS/chapter1.xhtml").decode("utf-8"))


    def test_epub_get_chapter_content_found_empty(self):
         
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub_empty_xhtml(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        result = self.epub.get_chapter_content("chapter1.xhtml")
        self.assertIsNone(result)

    #TODO: Tester avec des fichiers qui ne sont pas des html ?

#-----------------------------Testing parse_split_chapters-----------------------------

    def test_epub_parse_split_chapters_none(self):
        
        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {}
        self.epub.parse_split_chapters(chapters_with_split_content)
        
        self.assertEqual(self.epub.split_chapters,{})
    
    def test_epub_parse_split_chapters_one_section_none(self):

        opf = {"name":"content.opf","exists":True}
        toc = {"name":"toc.ncx","exists":True}
        generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub","epub/tempdir")

        chapters_with_split_content = {"chapter1.xhtml":["section1"]}
        self.epub.parse_split_chapters(chapters_with_split_content)
        #TODO: l'assert n'est pas finie, je dois comprendre comment fonctionne la
        # méthode avec ce BeautifulSoup de mort pour savoir ce qu'il va retourner
        
        # self.assertEqual(self.epub.split_chapters,{})

        #TODO: je vais surement devoir rebouger au utils.py pour pouvoir créer 
        # des chapitre avec des sections


#-----------------------------Testing generate_content-----------------------------

    # def test_epub_generate_content_one_chapter(self):
        
    #     opf = {"name":"content.opf","exists":True}
    #     toc = {"name":"toc.ncx","exists":True}
    #     generate_epub(xhtml=True,xml=True,opf=opf,mimetype=True,toc=toc,chapters=1)
    #     self.epub = EPUB("epub/test.epub","epub/tempdir")

    #     self.epub.generate_content()
        

#-----------------------------Testing generate_metadata-----------------------------
    def test_generate_valide_metadata(self):
        opf = {"name": "content.opf", "exists": True}
        toc = {"name": "toc.ncx", "exists": True}
        generate_epub(xhtml=True, xml=True, opf=opf, mimetype=True, toc=toc, chapters=1, cover = True)
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
        generate_epub_empty_metadata(xhtml=True, xml=True, opf=opf, mimetype=True, toc=toc, chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        self.epub.generate_metadata()

        self.assertEqual(self.epub.metadata.title, "test")
        self.assertEqual(self.epub.metadata.author, "Unknown")
        self.assertEqual(self.epub.metadata.year, 9999)
        self.assertEqual(self.epub.metadata.isbn, None)
        self.assertEqual(self.epub.metadata.tags, [])
        


#-----------------------------Testing generate_book_cover-----------------------------

    def test_generate_book_cover(self):
        # Générer un fichier EPUB avec une couverture
        generate_epub(xhtml=True, xml=True, opf={"name": "content.opf", "exists": True}, mimetype=True, toc={"name": "toc.ncx", "exists": True}, chapters=1, cover = True)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        # Appeler la fonction pour générer la couverture du livre
        self.epub.generate_book_cover()

        # Vérifier que la couverture a été générée avec succès
        self.assertEqual(self.epub.cover_image_name, "cover")

    def test_generate_book_cover_no_cover(self):
        # Générer un fichier EPUB sans couverture
        generate_epub(xhtml=True, xml=True, opf={"name": "content.opf", "exists": True}, mimetype=True, toc={"name": "toc.ncx", "exists": True}, chapters=1, cover = False)
        self.epub = EPUB("epub/test.epub", "epub/tempdir")

        # Appeler la fonction pour générer la couverture du livre
        self.epub.generate_book_cover()

        # Vérifier que la couverture est "", car il n'y a pas de couverture dans le fichier EPUB
        self.assertEqual(self.epub.cover_image_name, "")

#TODO: Après ces tests, y'a plus de fonction/méthode à tester dans read_epub.py,
# voir si on fait aussi le epub.py sur lequel tu bossais


if __name__ == "__main__":
    unittest.main()