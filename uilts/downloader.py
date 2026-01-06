import re
from time import sleep
from typing import List, TypedDict

import requests
from bs4 import BeautifulSoup

class Item(TypedDict):
    title: str

class Downloader:
    dict_item: set[str]
    
    def __init__(self, fp):
        self.dict_item = set()
        self.outFile = open(fp, "w", encoding="utf-8")

    def getAll(self):
        # 来自观测枢
        channelMap :dict[str, int] = {
            '角色': 25,
            '武器': 5,
            '圣遗物': 218,
            '组织': 255,
            '敌人': 6,
            '地图文本': 251,
            '成就': 252,
            '食物': 21,
            '头像': 244,
            '背包': 13,
            '活动': 105,
            '任务': 43,
            '动物': 49,
            '书籍': 68,
            '冒险家协会': 55,
            'NPC&商店': 20,
            '秘境': 54,
            '洞天': 130,
            '名片': 109,
            '装扮': 211,
            '教程': 227,
            '剧诗': 249,
            '观景点': 253,
            '区域': 7,
            '角色牌': 233,
            '行动牌': 234,
            '魔物牌': 235,
            # 往下为千星奇域
            '千星奇域道具': 267,
            '千星奇域衣装': 264,
            '千星奇域衣装部件': 266,
            '千星奇域妆容': 270,
            '千星奇域表情与动作': 267,
            '千星奇域典藏模板': 265,
        }

        # 爬取数据
        for channel in channelMap:
            res = requests.get(f"https://act-api-takumi-static.mihoyo.com/common/blackboard/ys_obc/v1/home/content/list?app_sn=ys_obc&channel_id={channelMap.get(channel)}")
            data = res.json()['data']
            if data is None:
                print(f"{channel}获取失败，跳过该分类")
                continue
            dataList: list[Item] = data['list'][0]['list']
            
            self.outFile.write(f"# {channel}列表\n")
            count = 0
            for item in dataList:
                reg = r"【.*?】"
                title: str = re.sub(reg, "", item.get("title"))
                
                # 统一符号
                title = title.replace('•', '·')
                title = title.replace('・', '·')
                
                self.dict_item.add(title)
                count+=1
                
                # 拆分词条
                splitChar :List[str] = [' ', '·', '，']
                for char in splitChar:
                    if title.find(char) > -1:
                        for word in title.split(char):
                            self.dict_item.add(word)
                            count += 1
            print(f"获取{channel}完毕，共{len(dataList)}条数据，写入{count}个词条")

        # 写入文件
        self.outFile.write('\n'.join(self.dict_item))
        print(f"爬取信息完毕，去重后共{len(self.dict_item)}个词条")
        self.outFile.close()
