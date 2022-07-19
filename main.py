import requests
import re
from bs4 import BeautifulSoup


def spysone():
    """
    socks5 proxy generator
    """
    url = "https://spys.one/en/socks-proxy-list/"
    headers = {
        "host": "spys.one",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
    }
    soup = BeautifulSoup(requests.get(
        url, headers=headers).text, "html.parser")
    d = {"data": {}}
    for j in soup.findAll("form"):
        if "socks-proxy-list" in j["action"]:
            d.update(j.attrs)
            for k in j.findAll("input"):
                d["data"].update({
                    k["name"]: k.get('value') if k.get(
                        'value') is not None else ""
                })
            for sl in j.findAll("select"):
                if sl.previous_sibling.text.lower().strip() == "show":
                    d['data'].update({
                        sl["name"]: "5"
                    })
                else:
                    d["data"].update({
                        sl["name"]: sl.option["value"]
                    })
    allList = requests.post(url, data=d["data"], headers=headers).text
    if (g := re.search(r"<\/table><script.*>([^'].*);<\/script>", allList)):
        for i in [i.split("=") for i in g.group(1).split(";")]:
            if i[1].isdigit():
                globals()[i[0]] = int(i[1])
            else:
                globals()[i[0]] = eval(i[1])
        if (td := re.findall(r"(?:<td\s[^>]*?><font\sclass\=spy14>(.*?)<script.*?\"\+(.*?)\)<\/script)", allList)):
            for proxy, port in td:
                yield "{}:{}".format(
                    proxy, "".join([str(eval(i)) for i in port.split("+")])
                )
        return None
    return None


if __name__ == '__main__':
    print(" getting proxy :...")
    if (proxy := spysone()):
        f = open("socks5.txt", "a", encoding="utf-8")
        for p in proxy:
            print(p)
            f.write(p+"\n")
        f.close()
        print("ok done!")
