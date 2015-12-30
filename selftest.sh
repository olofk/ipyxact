mkdir -p out
echo Running gen_c_header
PYTHONPATH=ipyxact python gen_c_header.py generic_example.xml > out/out.h
echo Running gen_markdown
PYTHONPATH=ipyxact python gen_markdown.py generic_example.xml > out/out.md
echo Running ipxactwriter
PYTHONPATH=ipyxact python ipxactwriter.py out/ipxactwriter.xml
echo Running print_businterfaces
PYTHONPATH=ipyxact python print_businterfaces.py generic_example.xml > out/bus.txt
echo Running print_filesets
PYTHONPATH=ipyxact python print_filesets.py generic_example.xml > out/files.txt
echo Running write_xml
PYTHONPATH=ipyxact python write_xml.py generic_example.xml out/new.xml > out/write_xml.txt

