from pprint import pprint

def generator_function():
    for i in range(10):
        yield i

temp_list = []
for index, item in sorted(enumerate(generator_function())):
    temp_item = {'id': index+1, 'content': item}
    temp_list.insert(index, temp_item)

pprint(temp_list)
