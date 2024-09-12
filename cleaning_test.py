import re

# text = """Non può esercitare tale facoltà negli ultimi sei
# mesi del suo mandato, salvo che essi coincidano in
# tutto o in parte con gli ultimi sei mesi della legislatura. (*)
# (*) Comma modificato con la legge costituzionale 4 novembre 1991, n. 1 «Modifica dell’articolo 88, secondo comma, della Costituzione» (Gazz. Uff. n. 262 dell’8
# novembre 1991).
# 1 Cost. 711 2 Cost. 731, 74, 1382 3 Cost. 76, 77 4 Cost. 751, 1382 5 Cost. 80
# 6 Cost. 78 7 Cost. 1042 8 Cost. 60142 COSTITUZIONE DELLA REPUBBLICA ITALIANA
# Art. 89.
# Nessun atto del Presi"""

# # Regular expression to match text between "(*)" followed by a space and a character, and "COSTITUZIONE DELLA REPUBBLICA ITALIANA"
# pattern = r"\(\*\) .+?(?=COSTITUZIONE DELLA REPUBBLICA ITALIANA)"

# # Substitute the matched text with an empty string
# modified_text = re.sub(pattern, "(*)", text, flags=re.DOTALL)

# print(modified_text)

import re

text = """obre 2020).
1 Cost. 131Costituzione della Repubblica Italiana_Layout 1  17/10/2023  08:12  Pagina 29COSTITUZIONE  DELLA  REPUBBLICA  ITALIANA 30
Art. 58. (*)  
I senator"""

# Define the pattern to match and remove
pattern = r"1 Cost\..*?(?=Costituzione della Repubblica Italiana_Layout)"

# Use re.sub() to replace the matched text with an empty string
modified_text = re.sub(pattern, '', text, flags=re.DOTALL)

print(modified_text)