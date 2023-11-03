# Get the suggestion
def get_similar_word(word, known_words_contents):
    word_distance_list = []
    for w in known_words_contents:
        word_distance_list.append( (w, (simplified_lev(word, w)) ) )    

    # Sort the tuple based on value in descending order
    sorted_tuple = sorted(word_distance_list, key=lambda x: x[1], reverse=False)
    sorted_words = [word[0] for word in sorted_tuple]
    return sorted_words

# Removing duplicate words from the sentence
def handle_duplicate(sentence, line):
    old_words = sentence.split()
    new_words = []
    size = len(old_words)
    duplicate_word = ''
    for i in range(size):
        # Duplicate word

        if i == 0 and old_words[i]==old_words[i+1]:
            # When first two word is duplicate
            duplicate_word = old_words[i]
            print(f"""Line {line}: '{old_words[i]} {old_words[i+1]}' {old_words[i+2]} """)

            print(f"""  (0) '{old_words[i]} {old_words[i+1]}' (1) '{old_words[i]}'""")

            answer = { 0: f'{old_words[i]} {old_words[i+1]}', 1:f'{old_words[i]}'}
            option = int(input('Option: '))


        elif (i == size-2 and len(old_words)==3) and old_words[i]==old_words[i+1]:
            duplicate_word = old_words[i]
            # When last two word is duplicate
            print(f"""Line {line}: {old_words[i-1]} '{old_words[i]} {old_words[i+1]}' """)

            print(f"""  (0) '{old_words[i]} {old_words[i+1]}' (1) '{old_words[i]}' """)
            answer = {0: f'{old_words[i]} {old_words[i+1]}', 1:f'{old_words[i]}'}
            option = int(input('Option: '))

        elif (i<len(old_words)-2) and old_words[i]==old_words[i+1]:
            duplicate_word = old_words[i]
            # When any middle words are duplicate
            print(f"""Line {line}: {old_words[i-1]} '{old_words[i]} {old_words[i+1]}' {old_words[i+2]} """)
            print(f"""  (0) '{old_words[i]} {old_words[i+1]}' (1) '{old_words[i]}' """)
            answer = {0: f'{old_words[i]} {old_words[i+1]}', 1:f'{old_words[i]}'}
            option = int(input('Option: '))

        else:
            # When no words are duplicate
            if old_words[i] == duplicate_word:
                new_words.append(answer[option])
            else:
                new_words.append(old_words[i])

    return ' '.join(new_words)


def ab_star(a: str, b: str) -> tuple:
    new_a = ''
    new_b = ''
    b_list = list(b)
    for ch in a:
        if ch in b_list:
            b_list.remove(ch)
        else:
            new_a+=ch
            
    a_list = list(a)
    for ch in b:
        if ch in a_list:
            a_list.remove(ch)
        else:
            new_b+=ch
    
    return (new_a,new_b)


def simplified_lev(a: str, b: str) -> int:
    a_star_str, b_star_str = ab_star(a, b)
    return max(len(a_star_str), len(b_star_str))


def main():
    #---------------------------------------------------------------------
    while True:    
        try:
            input_filename = input('File to check: ')
            # input_filename = 'essay.txt' #input('File to check: ')
            with open(input_filename) as file:
                input_file_contents = file.read().split('\n')

        except FileNotFoundError:
                print('Filename is not present. Please try again !')
        else:
            break
    
    #---------------------------------------------------------------------
    while True:    
        try:
            known_words_filename = input('File with known words [enter for default]: ')
            # known_words_filename = 'spell.txt'  #input('File with known words [enter for default]: ')
            with open(known_words_filename) as file:    
                known_words_contents = file.read().split('\n')

        except FileNotFoundError:
                print('Filename is not present. Please try again !')
        else:
            break
    
    #---------------------------------------------------------------------
    # Read common mistakes file.
    try:
        with open('common.txt') as file:    
            # Get the list of common mistake words.
            common_mistakes = file.read().split('\n')

    except:
        # Initialize the common mistakes with empty list.
        common_mistakes = []

    print('--------------------')
    print(f'Processing {input_filename}')

    #---------------------------------------------------------------------
    # All Processing Logic Comes Under This Function.

    # Correct sentence list
    correct_sentences = []

    # Handle common list
    common_words = []

    for i,content in enumerate(input_file_contents):
        words = content.split()
        new_words = []
        
        for j in range(len(words)): 
            # When word is not the last word of sentence
            if j != len(words)-1:
                if j==0 and words[j].lower() not in known_words_contents:
                    print(f'''Line {i+1}: '{words[j]}' {words[j+1]}''')

                    suggestion = get_similar_word(words[j], known_words_contents)
                    
                    print(f"""  (0) '{words[j]}' (1) {suggestion[0]} (2) {suggestion[1]} (3) {suggestion[2]} (4) edit""")
                    answer = {0: words[j], 1:suggestion[0], 2:suggestion[1], 3:suggestion[2]}
                    option = int(input('Option: '))
                    if option == 4:
                        answer[option] = input('Input custom text: ')
                    new_words.append(answer[option])

                    # add wrong word and its correction
                    common_words.append( (words[j], answer[option]) )

                    
                elif words[j].lower() not in known_words_contents:
                    print(f'''Line {i+1}: {words[j-1]} '{words[j]}' {words[j+1]}''')

                    suggestion = get_similar_word(words[j], known_words_contents)
                    print(f"""  (0) '{words[j]}' (1) {suggestion[0]} (2) {suggestion[1]} (3) {suggestion[2]} (4) edit""")
                    answer = {0: words[j], 1:suggestion[0], 2:suggestion[1], 3:suggestion[2]}
                    option = int(input('Option: '))
                    if option == 4:
                        answer[option] = input('Input custom text: ')
                    new_words.append(answer[option])

                    # add wrong word and its correction
                    common_words.append( (words[j], answer[option]) )
                
                else:
                    new_words.append(words[j])
                    
                    
            # When word is the last word of sentence            
            elif words[j][:-1].lower() not in known_words_contents:
                word = words[j][:-1]
                print(f'''Line {i+1}: {words[j-1]} '{words[j][:-1]}'{words[j][-1]}''')

                suggestion = get_similar_word(words[j], known_words_contents)
                print(f"""  (0) '{word}' (1) {suggestion[0]} (2) {suggestion[1]} (3) {suggestion[2]} (4) edit""")
                answer = {0: word, 1:suggestion[0], 2:suggestion[1], 3:suggestion[2]}
                option = int(input('Option: '))
                if option == 4:
                    answer[option] = input('Input custom text: ')
                new_words.append(answer[option]+'.')

                # add wrong word and its correction
                common_words.append( (words[j], answer[option]) )
                
            else:
                new_words.append(words[j])

        # Correct spell text
        correct_spell_sent = ' '.join(new_words)

            
        # Check for duplicate words
        unique_sent = handle_duplicate(correct_spell_sent,i+1)

        # Append the correct and unique sentence in correct_sentences
        correct_sentences.append(unique_sent)
        

    #---------------------------------------------------------------------
    print('--------------------')
    save_filename = input('File to save updated document: ')
    with open(save_filename, 'w') as file:
        for content in correct_sentences:    
            file.write(content+'\n')

    #---------------------------------------------------------------------
    # Update the common.txt file with new mistake words.
    for word_pair in set(common_words):
        if common_words.count(word_pair)>=2:
            with open('common.txt', 'a') as file:    
                file.write(f'{word_pair[0]} {word_pair[1]} \n')



# Main Program Starts Here.
if __name__ == "__main__":
    while True:    
        print('Fancy Spell-Checker')
        main()
        your_choice = input('Hit enter to continue with another file or quit exit: ')
        if your_choice == 'quit':
            break