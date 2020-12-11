from datetime import datetime

from django.shortcuts import render
from elasticsearch import Elasticsearch
from pprint import pprint
client = Elasticsearch('127.0.0.1',port=9200)
# Create your views here.
def indexluoji(request):
    print(request.method)  # 获取用户请求的路径
    return render(request, 'index.html')

def searchluoji(request):
    key_words = request.GET.get('q','')
    page = request.GET.get('p', '1')  # 获取访问页码
    try:
        page = int(page)
    except:
        page = 1

    start_time = datetime.now()
    response = client.search(  # 原生的elasticsearch接口的search()方法，就是搜索，可以支持原生elasticsearch语句查询
        index="cnblogs",  # 设置索引名称
        doc_type="doc",  # 设置表名称
        body={  # 书写elasticsearch语句
            "query": {
                "multi_match": {  # multi_match查询
                    "query": key_words,  # 查询关键词
                    "fields": ["title", "description"]  # 查询字段
                }
            },
            "from": (page-1)*10,  # 从第几条开始获取
            "size": 10,  # 获取多少条数据
            "highlight": {  # 查询关键词高亮处理
                "pre_tags": ['<span class="keyWord">'],  # 高亮开始标签
                "post_tags": ['</span>'],  # 高亮结束标签
                "fields": {  # 高亮设置
                    "title": {},  # 高亮字段
                    "description": {}  # 高亮字段
                }
            }
        }
    )
    end_time = datetime.now()
    last_time = (end_time - start_time).total_seconds()

    total_nums = response["hits"]["total"]


    hit_list = []
    for hit in response["hits"]["hits"]:  # 循环查询到的结果
        hit_dict = {}  # 设置一个字典来储存循环结果
        if "title" in hit["highlight"]:  # 判断title字段，如果高亮字段有类容
            hit_dict["title"] = "".join(hit["highlight"]["title"])  # 获取高亮里的title
        else:
            hit_dict["title"] = hit["_source"]["title"]  # 否则获取不是高亮里的title

        if "description" in hit["highlight"]:  # 判断description字段，如果高亮字段有类容
            hit_dict["description"] = "".join(hit["highlight"]["description"])[:500]  # 获取高亮里的description
        else:
            hit_dict["description"] = hit["_source"]["description"]  # 否则获取不是高亮里的description

        hit_dict["url"] = hit["_source"]["url"]  # 获取返回url
        hit_dict["create_date"] = hit["_source"]["riqi"]
        hit_dict["score"] = hit["_score"]
        hit_dict["source_site"] = "博客园"
        hit_list.append(hit_dict)
    return render(request, 'result.html', {
                                            "page":page,
                                           "total_nums": total_nums,    # 数据总条数
                                           "all_hits": hit_list,        # 数据列表
                                           "key_words": key_words,      # 搜索词
                                           "last_time": last_time       # 搜索时间
                                           })