import requests
import bs4
import html5lib
# coding=utf-8
header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
        'Cookie':'_cfduid=d013dbab27f08d937abf1668bba1c507b1582800657; age_certification=isok; _ga=GA1.2.981223937.1582800691; _gid=GA1.2.993052740.1582800691; wordpress_logged_in_6242fde54bf6f4f4b0c842643584bd9b=hjj19991111%7C1584010356%7CTLIjKCulafQoTZo4aLk8HxDkTBnKsWa7NZPp8CvSipv%7Ccb3e5132b4894dc7d31d2494bfbd0c62eb9d4dd547fc6ba7919a5cca85c8de63; PHPSESSID=tmufe0qi6auio9jead30s3o99n',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    # 'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'max-age=0'
    }

url = "http://www.dingdiansk.com"
novelpath = 'D:/project/1testpack/'
novelId = input("请输入小说的序号：")


#获取网页html内容
def getHtml(url):
    rs = requests.get(url, headers=header)
    rs.encoding = "utf-8"
    # print(rs.text)
    bs = bs4.BeautifulSoup(rs.text, "html5lib")
    return bs
#获取章节列表
def getChaper(url):
    bookUrl = url+"/book/"+novelId+".html"
    chaperA = getHtml(bookUrl).select(".dccss > a",)
    chaperL = []
    for chaper in chaperA:
        chaperL.append([chaper["href"],chaper.string])
    print(chaperL)
    return chaperL
#获取书名
def getTitle(url):
    bookUrl = url + "/book/" + novelId + ".html"
    novelTitle = getHtml(bookUrl).select('meta[property="og:novel:book_name"]')[0]["content"]
    print("正在下载小说：《"+novelTitle+"》...")
    return novelTitle
#下载小说
def downlaodChaper(chaperL):
    with open(novelpath+getTitle(url)+".txt", 'w', encoding="utf-8") as f:
        for chaper in chaperL:
            cont = getHtml(url+chaper[0]).select("#content")
            print("正在下载 "+chaper[1])
            chaperText = cont[0].get_text()
            # print(chaperText)
            f.write(chaper[1]+'\n')
            f.write(chaperText+'\n')
    f.close()

chaperL = getChaper(url)
downlaodChaper(chaperL)
# for line in cont.readlins():
#     if line=='\n':
#         line = line.strip('\n')

