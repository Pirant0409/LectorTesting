import os, zipfile
import shutil

# Generate epub file
def generate_epub(xhtml,xml,opf,mimetype,toc,chapters, cover):
    print("Generating epub file...")
    if not os.path.exists('epub'):
        os.makedirs('epub')

    epub_file = zipfile.ZipFile('epub/test.epub', 'w',zipfile.ZIP_DEFLATED)


    if not os.path.exists('epub/chapter1.xhtml') and xhtml["exists"]:
        if xhtml["is_empty"]:
            generate_empty_xhtml(chapters)
        else:
            generate_xhtml(chapters)

        for i in range(1, chapters+1):
            epub_file.write('epub/chapter'+str(i)+'.xhtml',"OPS/chapter"+str(i)+".xhtml")

    if not os.path.exists('epub/container.xml') and xml:
        generate_xml()
        epub_file.write('epub/container.xml',"META-INF/container.xml")

    if not os.path.exists('epub/'+opf["name"]) and opf["exists"] and toc["exists"]:
        generate_opf(opf,toc,chapters)
        epub_file.write('epub/'+opf["name"],"OPS/"+opf["name"])

    if not os.path.exists('epub/mimetype') and mimetype:
        generate_mimetype()
        epub_file.write('epub/mimetype', compress_type=zipfile.ZIP_STORED)
    
    if not os.path.exists('epub/'+toc["name"]) and toc["exists"]:
        generate_toc(toc,chapters)
        epub_file.write('epub/'+ toc["name"],"OPS/"+toc["name"])

    # if not os.path.exists('epub/valideCover.png') and cover:
    #     getValideCover()
    
    epub_file.close()

def generate_epub_empty_metadata(xhtml,xml,opf,mimetype,toc,chapters):
    print("Generating epub file...")
    if not os.path.exists('epub'):
        os.makedirs('epub')

    epub_file = zipfile.ZipFile('epub/test.epub', 'w',zipfile.ZIP_DEFLATED)


    if not os.path.exists('epub/chapter1.xhtml') and xhtml:
        generate_xhtml(chapters)
        for i in range(1, chapters+1):
            epub_file.write('epub/chapter'+str(i)+'.xhtml',"OPS/chapter"+str(i)+".xhtml")

    if not os.path.exists('epub/container.xml') and xml:
        generate_xml()
        epub_file.write('epub/container.xml',"META-INF/container.xml")

    if not os.path.exists('epub/'+opf["name"]) and opf["exists"] and toc["exists"]:
        generate_missing_metadata_opf(opf,toc,chapters)
        epub_file.write('epub/'+opf["name"],"OPS/"+opf["name"])

    if not os.path.exists('epub/mimetype') and mimetype:
        generate_mimetype()
        epub_file.write('epub/mimetype', compress_type=zipfile.ZIP_STORED)
    
    if not os.path.exists('epub/'+toc["name"]) and toc["exists"]:
        generate_toc(toc,chapters)
        epub_file.write('epub/'+ toc["name"],"OPS/"+toc["name"])

    
    epub_file.close()

def generate_xhtml(chapters):
    xhtml_content  = f'''<?xml version="1.0" encoding="UTF-8"?>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
        <head>
            <title>chapitrelol</title>
        </head>
        <body>
            <h1>Heading</h1>
            <p>This is an example paragraph.</p>
        </body>
    </html>
    '''
    for i in range(1, chapters+1):  
        with open("epub/chapter"+str(i)+".xhtml", 'w', encoding='utf-8') as file:
            file.write(xhtml_content)

def generate_empty_xhtml(chapters):
    xhtml_content  = f'''<?xml version="1.0" encoding="UTF-8"?>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">
        <head>
            <title>chapitrelol</title>
        </head>
        <body>
        </body>
    </html>
    '''
    for i in range(1, chapters+1):  
        with open("epub/chapter"+str(i)+".xhtml", 'w', encoding='utf-8') as file:
            file.write(xhtml_content)

def generate_xml():
    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
    <container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
        <rootfiles>
            <rootfile full-path="OPS/content.opf" media-type="application/oebps-package+xml"/>
        </rootfiles>
    </container>
    '''
    with open("epub/container.xml", 'w', encoding='utf-8') as file:
        file.write(xml_content)

def generate_opf(opf,toc,chapters):
    opf_content = f'''<?xml version="1.0" encoding="utf-8"?>
    <package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:identifier id="bookid" opf:scheme="ISBN">urn:uuid:8A768A9F-5559-3BAA-84E4-D39A4D249D51</dc:identifier>
            <dc:title>Title of the Book</dc:title>
            <dc:creator>Author Name</dc:creator>
            <dc:date>2015</dc:date>
            <dc:subject>test</dc:subject>
        </metadata>
        <manifest>
            <item id="ncx" href="{toc["name"]}" media-type="application/x-dtbncx+xml"/>
    '''

    for i in range(1, chapters + 1):
        chapter_filename = f"chapter{i}.xhtml"
        item_id = f"item{i}"
        media_type = "application/xhtml+xml"

        opf_content += f'''
                <item id="{item_id}" href="{chapter_filename}" media-type="{media_type}" />
        '''

    opf_content += '''
            </manifest>
            <spine>
    '''

    for i in range(1, chapters + 1):
        itemref_idref = f"item{i}"

        opf_content += f'''
                <itemref idref="{itemref_idref}" />
        '''

    opf_content += '''
            </spine>
        </package>
    '''

    with open("epub/"+opf["name"], 'w', encoding='utf-8') as file:
        file.write(opf_content)

def generate_missing_metadata_opf(opf,toc,chapters):
    opf_content = f'''<?xml version="1.0" encoding="utf-8"?>
    <package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        </metadata>
        <manifest>
            <item id="ncx" href="{toc["name"]}" media-type="application/x-dtbncx+xml"/>
    '''

    for i in range(1, chapters + 1):
        chapter_filename = f"chapter{i}.xhtml"
        item_id = f"item{i}"
        media_type = "application/xhtml+xml"

        opf_content += f'''
                <item id="{item_id}" href="{chapter_filename}" media-type="{media_type}" />
        '''

    opf_content += '''
            </manifest>
            <spine>
    '''

    for i in range(1, chapters + 1):
        itemref_idref = f"item{i}"

        opf_content += f'''
                <itemref idref="{itemref_idref}" />
        '''

    opf_content += '''
            </spine>
        </package>
    '''

    with open("epub/"+opf["name"], 'w', encoding='utf-8') as file:
        file.write(opf_content)

def generate_mimetype():
    mimetype_content = 'application/epub+zip'
    with open("epub/mimetype", 'w', encoding='utf-8') as file:
        file.write(mimetype_content)

def generate_toc(toc,chapters):

    toc_content = '''<?xml version="1.0" encoding="UTF-8"?>
    <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
        <navMap>
    '''

    for i in range(1, chapters+1):
        chapter_id = f"navPoint-{i}"
        play_order = i
        chapter_title = f"Chapter {i}"
        chapter_filename = f"chapter{i}.xhtml"

        toc_content += f'''
                <navPoint id="{chapter_id}" playOrder="{play_order}">
                    <navLabel>
                        <text>{chapter_title}</text>
                    </navLabel>
                    <content src="{chapter_filename}" />
                </navPoint>
        '''

    toc_content += '''
            </navMap>
        </ncx>
    '''

    with open("epub/"+toc["name"], 'w', encoding='utf-8') as file:
        file.write(toc_content)

# def getValideCover():
    
#      cover_path = "Test/Cover/valideCover.jpg"  # Chemin du fichier valideCover.png

#      if os.path.exists(cover_path):
#          # Copie le fichier valideCover.png dans le dossier epub
#          shutil.copy(cover_path, 'epub/valideCover.jpg')
#          print("Valide cover added to epub folder.")
#      else:
#          print("Valide cover file not found.")

