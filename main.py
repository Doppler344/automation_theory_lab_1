import re

DEBUG = True


class FormalLanguageAlphabet:
    sgtr = ""

    def __init__(self, alphabet):
        try:
            if re.fullmatch(r"^\b[a-z]{2,}\b$|^\b[а-яё]{2,}\b$", alphabet) is None:
                raise ValueError("Wrong alphabet \nOnly use [a-z] or [а-яё], length >= 2")
            elif DEBUG:
                print("Alphabet:", alphabet)
        finally:
            pass
        self.__alphabet = alphabet

    def search_number_with_word(self, word):
        try:
            if re.fullmatch(r"^\b[{alphabet}]+\b$".format(alphabet=self.__alphabet), word) is None:
                raise ValueError("Wrong word \nOnly alphabet")
            elif DEBUG:
                print("Word:", word)
        finally:
            pass
        sum_off_symbol_values = 0
        expression_string_list = []
        for number, sym in enumerate(word, start=1):
            sym_value, string_value = self.__calculate_value_for_symbol(number, word)
            sum_off_symbol_values += sym_value
            expression_string_list.append(string_value)
        return sum_off_symbol_values, " + ".join(expression_string_list)

    def __calculate_value_for_symbol(self, number, word):
        number_of_alphabet_symbol = self.__alphabet.index(word[number - 1]) + 1  # + 1 because of index starts from 0
        return number_of_alphabet_symbol * (len(self.__alphabet) ** (len(word) - number)), ("({0} * {1}^{2})".format(
            number_of_alphabet_symbol, (len(self.__alphabet)), (len(word) - number)))

    def search_word_with_number(self, expr):
        if self.sgtr == "":
            self.sgtr = " "
        else:
            self.sgtr = ")" + str(re.search(r"[*]\d+ [+] \d+$", str(expr))[0]) + self.sgtr
        number = int(re.search(r"^\b\d+", str(expr))[0])
        if int(re.search(r"^\b\d+", str(expr))[0]) <= len(self.__alphabet):
            self.sgtr = str((re.search(r"^\b\d+", str(expr))[0])) + self.sgtr[1:]
            brecket = self.sgtr.count(')')
            self.sgtr = "(" * brecket + self.sgtr
            return self.sgtr, self.__combine()
        expression_string = f"{number // len(self.__alphabet)}*{len(self.__alphabet)} + {number % len(self.__alphabet)}"
        if DEBUG:
            print("experssion 1\n", expression_string)
        if number % len(self.__alphabet) == 0:
            expression_string = f"{(number - 1) // len(self.__alphabet)}*{len(self.__alphabet)} + {len(self.__alphabet)}"
            if DEBUG:
                print("experssion 2\n", expression_string)
        return self.search_word_with_number(expression_string)

    def __combine(self):
        checkster = str((re.search(r"[*]\d", str(self.sgtr))[0]))
        line = self.sgtr.split(checkster)
        line = "".join(line)
        nums = re.findall(r'\d+', line)
        nums = [int(i) for i in nums]
        line = " "
        for ind, num in enumerate(nums, start=1):
            line += f" + {num}*{len(self.__alphabet)}^{len(nums) - ind}"
        line = line[4:]
        word = [self.__alphabet[i - 1] for i in nums]
        word = "".join(word)
        return line, word


if __name__ == '__main__':
    ferm = FormalLanguageAlphabet("abc")
    number = ferm.search_number_with_word("abcabcb")
    print("{1} = {0}".format(number[0], number[1]))
    word = ferm.search_word_with_number(376)
    print("{0}= {1}\nWord = {2}".format(word[0], word[1][0], word[1][1]))
