from sys import argv
import locale
locale.setlocale(locale.LC_ALL, "en_US")
def main():
    input = argv[1]
    output = argv[2]
    with open(input, mode="r") as text:
        file_path = text.name
        file_name = file_path.split("\\")[-1]
        text = text.read()
        text = text.lower()
    with open(output, mode="w") as output:
        words = count_words(text)
        sentences = count_sentences(text)
        word_sentence_ratio = count_word_sentence_ratio(text)
        characters = count_characters(text)
        characters_word = count_characters_word(text)
        shortest_word = count_shortest_word(text)
        longest_word = count_longest_word(text)
        frequency = count_frequency(text)
        output.write(f"{'Statistics about ' + file_name:24}:\n")
        output.write(f"{'#Words':24}: {words}\n")
        output.write(f"{'#Sentences':24}: {sentences}\n")
        output.write(f"{'#Words/#Sentences':24}: {word_sentence_ratio:.2f}\n")
        output.write(f"{'#Characters':24}: {characters}\n")
        output.write(f"{'#Characters (Just Words)':24}: {characters_word}\n")
        output.write(f"{shortest_word}\n")
        output.write(f"{longest_word}\n")
        output.write(f"{frequency}")
def count_words(text):
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]"]
    for mark in punctuation:
        text = text.replace(mark,"")
    text = text.split()
    words = str(int(len(text)))
    return words
def count_sentences(text):
    punctuation = [".", "!", "?", "..."]
    for mark in punctuation:
        text = text.replace(mark,".")
    text = text.split(".")
    sentences = str(int(len(text) - 1))
    #When we divide sentences into points, there is an extra space at the end, so we subtract one.
    return sentences
def count_word_sentence_ratio(text):
    original_text = text
    #The original text is being saved because it will be needed at the bottom.
    ending_punctuation = [".", "!", "?", "..."]
    for mark in ending_punctuation:
        text = text.replace(mark,".")
    text = text.split(".")
    sentences = int(len(text) - 1)
    text = original_text
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]"]
    for mark in punctuation:
        text = text.replace(mark,"")
    text = text.split()
    words = int(len(text))
    return words/sentences
def count_characters(text):
    characters = len(text)
    return characters
def count_characters_word(text):
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]", ",", ";", ":"]
    apostrophe = ("'", "-")
    counter = 0
    for mark in punctuation:
        text = text.replace(mark,"")
    text = text.split()
    for element in text:
        if element[-1] in apostrophe:
            counter += len(element)-1
        else:
            counter += len(element)
    return counter
def count_shortest_word(text):
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]", ",", ";", ":"]
    for mark in punctuation:
        text = text.replace(mark, "")
    text = text.split()
    shortest_word = text[0]
    shortest_word_list = []
    for word in text:
        if len(word) < len(shortest_word):
            shortest_word = word
    for word in text:
        if len(word) == len(shortest_word):
            shortest_word_list.append(word)
    shortest_word_list = sorted(list(set(shortest_word_list)))
    if len(shortest_word_list) == 1:
        return f"{'The Shortest Word':24}: {shortest_word_list[0]:<24} ({text.count(shortest_word_list[0]) / len(text):.4f})"
    else:
        result = f"{'The Shortest Words':24}:"
        for word in shortest_word_list:
            result += f"\n{word:<24} ({text.count(word) / len(text):.4f})"
        return result
def count_longest_word(text):
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]", ",", ";", ":"]
    for mark in punctuation:
        text = text.replace(mark, "")
    text = text.split()
    longest_word = text[0]
    longest_word_list = []
    for word in text:
        if len(word) > len(longest_word):
            longest_word = word
    for word in text:
        if len(word) == len(longest_word):
            longest_word_list.append(word)
    longest_word_list = sorted(list(set(longest_word_list)))
    if len(longest_word_list) == 1:
        return f"{'The Longest Word':24}: {longest_word_list[0]:<24} ({text.count(longest_word_list[0]) / len(text):.4f})"
    else:
        result = f"{'The Longest Words':24}:"
        for word in longest_word_list:
            result += f"\n{word:<24} ({text.count(word) / len(text):.4f})"
        return result
def count_frequency(text):
    punctuation = [".", "!", "?", "...", "(", ")", "[", "]", ",", ";", ":"]
    for mark in punctuation:
        text = text.replace(mark,"")
    text = text.split()
    for element in text:
        if element[-1] == "'":
            text.remove(element)
            element = element[:-1]
            text.append(element)
    frequency_list = []
    for element in set(text):
        frequency_list.append((element,text.count(element)/ len(text)))
    frequency_list.sort(key=lambda text:(-text[-1], text[0]))
    result = f"{'Words and Frequencies':24}:"
    for word, ratio in frequency_list:
        result += f"\n{word:<24}: {ratio:.4f}"
    return result
if __name__ == "__main__":
    main()
