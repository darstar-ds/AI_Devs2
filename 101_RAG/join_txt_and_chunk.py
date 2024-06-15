import os
import re
from langchain.text_splitter import NLTKTextSplitter

txts_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty_txt\\"
chunks_path = "C:\\Users\\dariu\\OneDrive\\Dokumenty\\Python Scripts\\_AI_Devs2_teksty_txt_sentences_256chars\\"

def remove_image_links(text):
    # This pattern matches Markdown image syntax [] followed by ()
    # where the parentheses contain 'http' and then any non-whitespace characters
    pattern = r'\[.*?\]\(http[s]?://.*?\)'
    
    # Replace the matched pattern with an empty string
    cleaned_text1 = re.sub(pattern, '', text)

    pattern2 = r'\*\*'
    cleaned_text2 = re.sub(pattern2, '', cleaned_text1)

    pattern3 = r'\n!\n'
    cleaned_text_3 = re.sub(pattern3, '', cleaned_text2)
    
    return cleaned_text_3

def remove_double_paragraphs(text):
    # This pattern matches Markdown image syntax [] followed by ()
    # where the parentheses contain 'http' and then any non-whitespace characters
    pattern = r"\n\n"
    
    if "\n\n" in text:
        for i in range(5):
            # Replace the matched pattern with an empty string
            cleaned_text = re.sub(pattern, '\n', text)
    
    return cleaned_text


def split_sentences(text):
    #split text into sentences and join into chunks 1000 chars long with 200 chars overlap 
    text_splitter = NLTKTextSplitter(chunk_size=256, chunk_overlap=64)
    chunks = text_splitter.split_text(text)

    return chunks

def join_txt_files(txts_path):
    files_in_directory = os.listdir(txts_path)
    txt_files = [file for file in files_in_directory if file.endswith('.txt')]
    joined_txts = ""

    for file in txt_files:
        file_path_name = txts_path + file
        with open(file_path_name, 'r', encoding='utf-8') as curr_file:
            file_content = curr_file.read()
            joined_txts += file_content
            # print(joined_txts[-20:])
    return joined_txts

def save_chunks2txt(chunks_list, chunks_path):
    for i, chunk in enumerate(chunks_list, start=1):
        filename = chunks_path + str(i).zfill(5) + ".txt"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(chunk)


'''Join all txt files in the provided folder'''
joined_txts_1 = join_txt_files(txts_path)
# print(joined_txts_1)

'''Remove image links from joined text'''
joined_txts_2 = remove_image_links(joined_txts_1)
# print(joined_txts_2)

'''Remove double paragraphs from the joined text'''
joined_txts_3 = remove_double_paragraphs(joined_txts_2)
# print(joined_txts_3)

'''Split text into sentences and concatenate chunks'''
chunks_list = split_sentences(joined_txts_3)
print(chunks_list[:3])

'''Save chunks as txt files'''
save_chunks2txt(chunks_list, chunks_path)