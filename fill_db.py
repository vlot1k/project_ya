import sqlite3


eng_morse = [
    ('a', '.-'), ('b', '-...'), ('c', '-.-.'), ('d', '-..'), ('e', '.'),
    ('f', '..-.'), ('g', '--.'), ('h', '....'), ('i', '..'), ('j', '.---'),
    ('k', '-.-'), ('l', '.-..'), ('m', '--'), ('n', '-.'), ('o', '---'),
    ('p', '.--.'), ('q', '--.-'), ('r', '.-.'), ('s', '...'), ('t', '-'),
    ('u', '..-'), ('v', '...-'), ('w', '.--'), ('x', '-..-'), ('y', '-.--'),
    ('z', '--..')
]
rus_morse = [
    ('а', '.-'), ('б', '-...'), ('в', '.--'), ('г', '--.'), ('д', '-..'),
    ('е', '.'), ('ж', '...-'), ('з', '--..'), ('и', '..'), ('й', '.---'),
    ('к', '-.-'), ('л', '.-..'), ('м', '--'), ('н', '-.'), ('о', '---'),
    ('п', '.--.'), ('р', '.-.'), ('с', '...'), ('т', '-'), ('у', '..-'),
    ('ф', '..-.'), ('х', '....'), ('ц', '-.-.'), ('ч', '---.'), ('ш', '----'),
    ('щ', '--.-'), ('ъ', '--.--'), ('ы', '-.--'), ('ь', '-..-'), ('э', '..-..'),
    ('ю', '..--'), ('я', '.-.-')
]
morse =[
    ('1', '.----'), ('2', '..---'), ('3', '...--'), ('4', '....-'),
    ('5', '.....'), ('6', '-....'), ('7', '--...'), ('8', '---..'),
    ('9', '----.'), ('0', '-----'),
    ('.', '.-.-.-'), (',', '--..--'), ('?', '..--..'), ('!', '-.-.--'),
    (':', '---...'), ('-', '-....-')
]
reverse_eng_morse = [(code, letter) for letter, code in eng_morse]
reverse_rus_morse = [(code, letter) for letter, code in rus_morse]
reverse_morse = [(code, letter) for letter, code in morse]

morse.append(('end', '...-.-'))
morse.append((' ', ' '))
reverse_morse.append(('...-.-', ''))

statistics = [
    ('ceasar_to_file', 0), ('rock_paper_scissors', 0)
]

connection = sqlite3.connect("project.db")

connection.cursor().execute("DROP TABLE IF EXISTS statistics")
connection.cursor().execute("DROP TABLE IF EXISTS rock_paper_scissors")
connection.cursor().execute("DROP TABLE IF EXISTS rus_morse")
connection.cursor().execute("DROP TABLE IF EXISTS eng_morse")
connection.cursor().execute("DROP TABLE IF EXISTS morse")

connection.cursor().execute("CREATE TABLE statistics(program, count)")
connection.cursor().execute("CREATE TABLE rock_paper_scissors(date_time, player, computer, result)")
connection.cursor().execute("CREATE TABLE rus_morse(key, value)")
connection.cursor().execute("CREATE TABLE eng_morse(key, value)")
connection.cursor().execute("CREATE TABLE morse(key, value)")

connection.cursor().executemany("INSERT INTO statistics VALUES(?, ?)", statistics)

connection.cursor().executemany("INSERT INTO rus_morse VALUES(?, ?)", rus_morse)
connection.cursor().executemany("INSERT INTO rus_morse VALUES(?, ?)", reverse_rus_morse)

connection.cursor().executemany("INSERT INTO eng_morse VALUES(?, ?)", eng_morse)
connection.cursor().executemany("INSERT INTO eng_morse VALUES(?, ?)", reverse_eng_morse)

connection.cursor().executemany("INSERT INTO morse VALUES(?, ?)", morse)
connection.cursor().executemany("INSERT INTO morse VALUES(?, ?)", reverse_morse)

connection.commit()
connection.close()
