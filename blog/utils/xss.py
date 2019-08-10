from bs4 import BeautifulSoup

def xss(old):
    valid_tag = {
        'p': ['class','id'],
        'img':['src'],
        'div': ['class']
    }
    soup = BeautifulSoup(old,'html.parser')

    tags = soup.find_all()
    for tag in tags:
        if tag.name not in valid_tag:
            tag.decompose()
        if tag.attrs:
            print(tag)
            for k in list(tag.attrs.keys()): # {id:'i1',a=123,b=999}
                if k not in valid_tag[tag.name]:
                    del tag.attrs[k]
    content_str = soup.decode()
    # print(content_str)
    return content_str



# dd = """
# <p id='i1' a='123' b='999'>
#     <script>alert(123)</script>
# </p>
# """
# aaa = xss(dd)
# print(aaa)