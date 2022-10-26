import Dictionary

# Liste=[]
# for i in range(161):
#     Liste.append(list(Dictionary.Champion_dict.items())[i+1][1])

for key in Dictionary.Champ_Logo_dict:
    print(key)

# for i in range(161):
#     print('<div class="image" data-title="' + Liste[i] + '">\n'
#     '<img src="' + Dictionary.Champ_Logo_dict[Liste[i]] + '" alt="">\n'
#     '<a href="{' + '{url_for(\'champion\', name=\'' + Liste[i] +'\')}' + '}">'+ Liste[i] +'</a>\n'
#     '</div>')