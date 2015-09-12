echo Running gen_c_header
python gen_c_header.py generic_example.xml > out.h
echo Running gen_markdonw
python gen_markdown.py generic_example.xml > out.md
echo Running ipxactwriter
python ipxactwriter.py
echo Running print_businterfaces
python print_businterfaces.py generic_example.xml > bus.txt
echo Running print_filesets
python print_filesets.py generic_example.xml > files.txt
echo Running write_xml
python write_xml.py generic_example.xml

