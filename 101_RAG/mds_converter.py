import os

class MD_Converter:
    def __init__(self, mds_path):
        self.mds_path = mds_path

    def md_chunk2dict(self, md_path):
        sections = {}
        curr_section = ""

        with open(md_path, 'r', encoding='utf-8') as curr_file:
            for line in curr_file:
                if line.startswith('#'):
                    curr_section = line.strip()
                    sections[curr_section] = ""
                else:
                    sections[curr_section] += line
            # print(sections)
        return sections

    def chunks_2txt_saver(self, md_dict, start_of_file):
        part_range = len(md_dict)
        part_no = 1
        # print(f"part_range_type = {type(part_range)}\npart_no_type = {type(part_no)}")
        while part_no < part_range:
            for filename, content in md_dict.items():
                if part_no < 10:
                    part_no_name = "0" + str(part_no)
                else:
                    part_no_name = str(part_no)
                with open(self.mds_path + start_of_file + "__" + part_no_name + ".txt", 'w', encoding='utf-8') as file:
                    file.write(content)
                part_no += 1

    def mds_converter(self):
        files_in_directory = os.listdir(self.mds_path)
        txt_files = [file for file in files_in_directory if file.endswith('.txt')]
        if txt_files:
            print(f"There are already TXT files in the folder {self.mds_path}. I do nothing.")
        else:
            for file in os.listdir(self.mds_path):
                print(file)
                start_of_file = file[:6]
                print(start_of_file)
                print(self.mds_path + file)
                mds2dict = self.md_chunk2dict(self.mds_path + file)
                self.chunks_2txt_saver(mds2dict, start_of_file)