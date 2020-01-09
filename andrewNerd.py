import os

dirs = os.listdir('maildir/')

sentList = ['sent', '_sent_mail', 'sent_items']
myset = [element for element in dirs if sum(1 for sub_path in sentList if os.path.isdir("maildir/"+ element + "/" + sub_path))]

old = os.listdir('maildir/')
def diff(first, second):
        second = set(second)
        return [item for item in first if item not in second]

print(len(dirs))
print(len(old))
print(diff(old, dirs))