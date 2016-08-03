#coding:utf-8
import urllib,time,urllib2
from bs4 import BeautifulSoup
from urllib import quote
import httplib,codecs
wizurl1='http://note.wiz.cn/api/gather/add?type=url2wiz&data='
classlist=["msg_item news redirect","msg_cover redirect","sub_msg_item redirect"]

def putwiz(wxinurl):
    req = urllib2.Request(wxinurl)
    req.add_header('Accept','image/webp,image/*,*/*;q=0.8')
    req.add_header('Accept-Language','zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4')
    req.add_header('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    res = urllib2.urlopen(req)
    print res.read()

def main():

    titlelist=[] #组织已同步文章名称的列表
    titlef=codecs.open(r'E:\out.txt',encoding='UTF-8')
    for line in titlef:
        # print line.encode('utf-8')
        titlelist.append(line.encode('utf-8').strip())
    print len(titlelist)
    titlef.close()

    f=open(r'e:\1.html')
    # Todo 目前扫描静态页面，修改为支持动态页面
    html=f.read()
    fout=open(r'E:\git\python_learn\get_wechat_artical\out.txt','a')
    soup=BeautifulSoup(html)
    for classflag in classlist:
        urlclasses = soup.find_all('a',attrs={"class": classflag})
        for urlclass in urlclasses:
            if  urlclass != None:
                if urlclass['hrefs'] != '':
                    for child in urlclass.descendants:
                        if child.name=='h4':
                            if child.string!=None:
                                if child.string.encode('utf-8') in titlelist:
                                    print 'pass' + child.string.encode('utf-8')
                                    pass
                                else:
                                    print 'unpass' + child.string.encode('utf-8')
                                    #Todo 获取子标签h4 并判断string是否为空或者None，再判断string是否已包含在titlelist中，已包含说明已同步跳过，未包含，说明需同步，调用putwiz，同时写到out.txt中
                                    wxurl =urlclass['hrefs']
                                    wizurl2 = quote('url=') + quote(wxurl).replace('%','%25') + '%26folder%3D%252Fpythondev%252F%26user%3Dassd2001_75%26content-only%3Dfalse'
                                    wizurl = wizurl1 +  wizurl2.replace('/','%2F')
                                    print wizurl
                                    putwiz(wizurl)
                                    fout.write(child.string.encode('utf-8'))
                                    fout.write('\n')
                                    # Todo1 记录每篇文章标题 以便增量处理
                                    # Todo2 增加多线程处理，提升效率
            else:
                print 'find wxurl failed!'
    fout.close

main()