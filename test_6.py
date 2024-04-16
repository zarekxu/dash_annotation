# Example dictionary with lists of strings as values
my_dict = {'a': ['apple', 'orange'], 'b': ['banana', 'melon'], 'c': ['grape', 'berry']}

# String to modify by replacing substrings with dictionary keys
item_to_find = 'I like apples and bananas'

# Prepare a list of tuples (substring, key) sorted by the length of substring in descending order
replacements = sorted((sub, key) for key, values in my_dict.items() for sub in values if sub in item_to_find)
replacements.sort(key=lambda x: len(x[0]), reverse=True)

# Replace each substring in item_to_find with the corresponding key
for substring, key in replacements:
    item_to_find = item_to_find.replace(substring, key)

print(item_to_find)
