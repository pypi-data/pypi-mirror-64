import  rdlaiye
#test for rdlaiye package
#draft the interface
#defign style
#   mf:module-function 模块.函数
#   mcf:module-class-function 模块.类.函数
#0.目录
#1.用户
#   1.1创建用户
#       1.1.1mf模式:user_create()
#       1.1.2mcf模式:user.create()
#   1.2查询用户
#       1.2.1mf模式:user_query()
#       1.2.2mcf模式:user.query()
#2.AI机器人
#   2.1机器人查询
#       2.1.1mf模式aibot_query()
#       2.1.2mcf模式aibot.query()
#3.知识分类knowledgeCategory简称kc
#   3.1知识分类获取根节点
#       3.1.1mf模式kc_root()
#       3.1.2mcf模式kc.root()
#   3.2知识分类一级展开
#       3.2.1mf模式kc_expand()
#       3.2.2mcf模式kc.expand()
#   3.3知识分类全部展开
#       3.3.1mf模式:kc_expandAll()
#       3.3.2mcf模式:kc.expandAll()
#   3.4知识分类根据名称获取ID
#       3.4.1mf模式kc_id()
#       3.4.2mcf模式kc.id()
#   3.5知识分类根据ID获取名称
#       3.5.1mf模式kc_name()
#       3.5.2mcf模式kc.name()
#   3.6知识分类创建
#       3.6.1mf模式kc_create()
#       3.6.2mcf模式kc.create()
#   3.7知识分类查询,结合expand与expandAll
#       3.7.1mf模式kc_query()
#       3.7.2mcf模式kc.query()
#   3.8知识分类删除
#       3.8.1mf模式kc_delete()
#       3.8.2mcf模式kc.delete()
#   3.9知识分类更新-TBU
#       3.9.1mf模式kc_update()
#       3.9.2mcf模式kc.update()
#4.知识点，也称为标准问,knowledgeNode，简称kn
#   4.1创建知识点
#       4.1.1mf模式kn_create()
#       4.1.2mcf模式kn.create()
#   4.2查询某个知识分类下面所有知识点
#       4.2.1mf模式kn_query()
#       4.2.2mcf模式kn.query()
#   4.3根据知识分类及知识点名称获取ID
#       4.3.1mf模式kn_id()
#       4.3.2mcf模式kn.id()
#   4.4根据知识分类及知识点ID获取名称
#       4.4.1mf模式kn_name()
#       4.4.2mcf模式kn.name()
#   4.5知识点删除-tbu
#       4.5.1mf模式kn_delete()
#       4.5.2mcf模式kn.delete()
#   4.6知识点更新-tbu
#       4.6.1mf模式kn_update()
#       4.6.2mcf模式kn.update()
#5.知识叶，也称为相似问,knowledgeLeaf，简称kl
# 在知识库应用时kl也作为kn进行处理
#   5.1创建知识引导
#       5.1.1mf模式kl_create()
#       5.1.2mcf模式kl.create()
#   5.2查询某个知识分类某个知识点下面所有知识引导
#       5.2.1mf模式kl_query()
#       5.2.2mcf模式kl.query()
#   5.3根据知识分类及知识点名称获取ID
#       5.3.1mf模式kl_id()
#       5.3.2mcf模式kl.id()
#   5.4根据知识分类及知识点ID获取名称
#       5.4.1mf模式kl_name()
#       5.4.2mcf模式kl.name()
#6.知识核,也称为标准答案,knowledgeKernel,kk
#   6.1创建标准答案
#       6.1.1mf模式kk_create()
#       6.1.2mcf模式kk.create()
#   6.2删除标准答案
#       6.2.1mf模式kk_delete()
#       6.2.2mcf模式kk.delete()
#   6.3查询标准答案
#       6.3.1mf模式kk_query()
#       6.3.2mcf模式kk.query()
#7.知识树 knowledgeTree,简称kt,保留，可用于品牌管理
#8.简称知识森林knowledgeForest,简称kf，保留，可用于领域知识管理
#9.laiyeR针对相应的接口实现R语言脚本




#
#
#-----------------------------------测试区----------------------------------------#
#   author:hulilei
#   company:reshapedata
#   创建用户提供3种实现方式
#   moduleName : rdlaiye
#   functionName : laiye_user_create
#   argList : 参数列表
#       user_name : 用户名 char
#       user_id : 用户id  char
#   returnValue :
#        value1:返回用户id char
#        value2:'error' char
#   note:这是最底层的函数，不再对外使用
#uid = rdlaiye.laiye_user_create(user_name="test",user_id="123-123")
#print(uid)
#   moduleName : rdlaiye
#   functionName : user_create
#   argList : 参数列表
#       user_name : 用户名 char
#       user_id : 用户id  char
#   returnValue :
#        value1:返回用户id char
#        value2:'error' char
#   note:这是对laiye_user_create的封装，做了简单，适用于不支持类的程序
print('1.1.1创建用户mf:rdlaiye.user_create')
uid2 = rdlaiye.user_create(user_name="test",user_id="123-123")
print(uid2)

#   moduleName : rdlaiye
#   functionName : user.create
#   argList : 参数列表
#       user_name : 用户名 char
#       user_id : 用户id  char
#   returnValue :
#        value1:返回用户id char
#        value2:'error' char
#   note:这是对laiye_user_create的类的封装，创建了类user
print('1.1.2创建用户mcf:rdlaiye.user.create')
uid3 =rdlaiye.user.create(user_name="test",user_id="123-123")
print(uid3)

#查询用户
#   moduleName : rdlaiye
#   functionName : user_create
#   argList : 参数列表
#       user_id : 用户id  char
#       format : 返回值格式 char 默认为list也可以是dict
#   returnValue :
#        value1 : nickname char 用户昵称
#        value2 : avatar_url char 用户头像链接
#   note:这是查询用户的基本函数，没有使用类封装
print('1.2.1查询用户mf:rdlaiye.user_query')
user_info =rdlaiye.user_query('123-123')
print(user_info)
#user_info2 =rdlaiye.user_query('123-123','json')
#print(user_info2)
#查询用户
#   moduleName : rdlaiye
#   functionName : user.create
#   argList : 参数列表
#       user_id : 用户id  char
#       format : 返回值格式 char 默认为list也可以是dict
#   returnValue :
#        value1 : nickname char 用户昵称
#        value2 : avatar_url char 用户头像链接
#   note:这是查询用户的基本函数，使用了类封装
print('1.2.2查询用户mcf:rdlaiye.user.query')
user_info3 =rdlaiye.user.query('123-123')
print(user_info3)


#机器人查询
#   moduleName : rdlaiye
#   functionName : aibot.query
#   argList : 参数列表
#       keyword : 关键词、问题
#       user_id :用户,默认来源配置文件
#       format : 返回数据格式，默认为二维数据，嵌套list(list)，也可以是list(dict)
#   returnValue :二维数据
#        value1 : nickname char 用户昵称
#        value2 : avatar_url char 用户头像链接
#   note:机器人查询的基本实现
print('2.1.1机器人查询mf:aibot_query')
keyword ='发现多少钱'
res_bot2 = rdlaiye.aibot_query(keyword)
print(res_bot2)
#   moduleName : rdlaiye
#   functionName : aibot.query
#   argList : 参数列表
#       keyword : 关键词、问题
#       user_id :用户,默认来源配置文件
#       format : 返回数据格式，默认为二维数据，嵌套list(list)，也可以是list(dict)
#   returnValue :二维数据
#        value1 : nickname char 用户昵称
#        value2 : avatar_url char 用户头像链接
#   note:机器人查询的类的实现
print('2.1.2机器人查询mcf:aibot.query')
res_bot = rdlaiye.aibot.query(keyword,format='json')
print(res_bot)

#3.1.1知识分类根分类查询
#   moduleName : rdlaiye
#   functionName : kc_root 查询根节点
#   argList : 参数列表
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认只返回下一级，而非所有级次，mf
print('3.1.1知识分类根节点mf:rdlaiye.kc_root')
kc1 = rdlaiye.kc_root()
print(kc1)
# kc2 = rdlaiye.kc_root('json')
# print(kc2)
#   moduleName : rdlaiye
#   functionName : kc.root 查询根节点
#   argList : 参数列表
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认只返回下一级，而非所有级次，mcf,创建了类kc=knowledgeCategory
print('3.1.2知识分类根节点mcf:rdlaiye.kc.root')
kc3 = rdlaiye.kc.root('json')
print(kc3)

#3.2知识分类展开
#   moduleName : rdlaiye
#   functionName : kc_expand 知识分类一级展开
#   argList : 参数列表
#       parent_id : 上级知识分类id，默认为0
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认展开下一级，而非所有,mf
print('3.2.1知识分类一级展开mf:rdlaiye.kc_expand')
kcx1 = rdlaiye.kc_expand('407895','list')
print(kcx1)
# kcx2 = rdlaiye.kc_expand('467928','json')
# print(kcx2)
#3.2知识分类一级展开
#   moduleName : rdlaiye
#   functionName : kc.expand 知识分类一级展开
#   argList : 参数列表
#       parent_id : 上级知识分类id，默认为0
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认展开下一级，而非所有,mcf
print('3.2.2知识分类一级展开mcf:rdlaiye.kc.expand')
kcx3 = rdlaiye.kc.expand('407895','json')
print(kcx3)
#3.3知识分类全部展开
#   moduleName : rdlaiye
#   functionName : kc_expandAll 知识分类所有展开
#   argList : 参数列表
#       parent_id : 上级知识分类id，默认为0
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认所有级次，mf
print('3.3.1知识分类全部展开mcf:rdlaiye.kc_expandAll')
kcxa1 = rdlaiye.kc_expandAll()
print(kcxa1)
# kcxa2 = rdlaiye.kc_expandAll(format='json')
# print(kcxa2)
print('3.3.2知识分类全部展开mcf:rdlaiye.kc.expandAll')
kcxa3 = rdlaiye.kc.expandAll(format='json')
print(kcxa3)
#   moduleName : rdlaiye
#   functionName : kc.expandAll 知识分类所有展开
#   argList : 参数列表
#       parent_id : 上级知识分类id，默认为0
#       format : 提供list与json两个选项
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : name char 知识分类名称
#        value2 : id char 知识分类id
#        value3 : parent_id char 上级id,默认为'0'
#   note:默认所有级次，mcf,创建了类kc=knowledgeCategory
#3.4知识分类根据名称获取ID
#   moduleName : rdlaiye
#   functionName : kc_id 根据知识分类名称来获取相应的ID
#   argList : 参数列表
#       kc_name : 知识分类名称
#       parent_id : 默认为'0'表示全部,也可以指定相应内容
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : 返回ID char

#   note:默认从所有知识分类中进行获取，mf模式
print('3.4.1根据名称获取ID mf:rdlaiye.kc_id')
kcid1 = rdlaiye.kc_id('RDS')
print(kcid1)
#   moduleName : rdlaiye
#   functionName : kc.id 根据知识分类名称来获取相应的ID
#   argList : 参数列表
#       kc_name : 知识分类名称
#       parent_id : 默认为'0'表示全部,也可以指定相应内容
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : 返回ID char

#   note:默认从所有知识分类中进行获取，mcf模式
print('3.4.2根据名称获取ID mcf:rdlaiye.kc.id')
kcid2 = rdlaiye.kc.id('RDS')
print(kcid2)
#3.5知识分类根据ID获取名称
print('3.5.1根据ID获取名称mf:rdlaiye.kc_name')
kcname1 = rdlaiye.kc_name('529061')
print(kcname1)
#   moduleName : rdlaiye
#   functionName : kc_name 根据知识分类id来获取相应的名称
#   argList : 参数列表
#       kc_id : 知识分类名称
#       parent_id : 默认为'0'表示全部,也可以指定相应内容
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : 返回kc_name char 返回知识库名称

#   note:默认从所有知识分类中进行获取，mf模式
print('3.5.2根据ID获取名称mcf:rdlaiye.kc.name')
kcname2 = rdlaiye.kc.name('529061')
print(kcname2)
#   moduleName : rdlaiye
#   functionName : kc.name 根据知识分类id来获取相应的名称
#   argList : 参数列表
#       kc_id : 知识分类名称
#       parent_id : 默认为'0'表示全部,也可以指定相应内容
#   returnValue :二维数据，默认为二维数据，嵌套list(list)，也可以是list(dict)
#        value1 : 返回kc_name char 返回知识库名称

#   note:默认从所有知识分类中进行获取，mcf模式

#3.6创建知识分类
print('3.6创建知识分类')

#   moduleName : rdlaiye
#   functionName : kc_create创建知识分类
#   prototype:kc_create(kc_parentName,kc_name):
#   argList : 参数列表
#       kc_parentName : char 上级知识分类名称
#       kc_name : char 当前知识分类名称
#   returnValue :
#        kc_id : 返回知识分类id char
#   note:
#   mf模式
#   系统要求知识分类不能重复，否则报错
#   examples:
print('3.6.1创建知识分类mf:rdlaiye.kc_create')
# kcc1 = rdlaiye.kc_create('RDS','kc2')
# print(kcc1)
#
#
#
#   moduleName : rdlaiye
#   functionName : kc.create创建知识分类
#   prototype:kc.create(kc_parentName,kc_name):
#   argList : 参数列表
#       kc_parentName : char 上级知识分类名称
#       kc_name : char 当前知识分类名称
#   returnValue :
#        kc_id : 返回知识分类id char
#   note:
#   mcf模式
#   系统要求知识分类不能重复，否则报错
#   examples:
print('3.6.2创建知识分类mcf:rdlaiye.kc.create')
# kcc2 = rdlaiye.kc.create('RDS','kc3')
# print(kcc2)

#3.7查询知识分类
print('3.7查询知识分类')
#   moduleName : rdlaiye
#   functionName : kc_query 查询知识分类
#   prototype: kc_query(parent_id='0', format='list', show_all=False):
#   argList : 参数列表
#       parent_id : char 上级知识分类ID
#       format : char 返回数据格式
#       show_all : 下一级还是全部
#   returnValue :
#        kc_id : 根据format进行定义list(list)或list(dict)
#   note:
#   mf模式
#   examples:
print('3.7.1查询知识分类mf:rdlaiye.kc_query')
kcq1 = rdlaiye.kc_query(show_all=True)
print(kcq1)
#   moduleName : rdlaiye
#   functionName : kc_query查询知识分类
#   prototype: kc_query(parent_id='0', format='list', show_all=False):
#   argList : 参数列表
#       parent_id : char 上级知识分类ID
#       format : char 返回数据格式
#       show_all : 下一级还是全部
#   returnValue :
#        kc_id : 根据format进行定义list(list)或list(dict)
#   note:
#   mf模式
#   examples:
print('3.7.2查询知识分类mcf:rdlaiye.kc.query')
#   moduleName : rdlaiye
#   functionName : kc.query查询知识分类
#   prototype: kc.query(parent_id='0', format='list', show_all=False):
#   argList : 参数列表
#       parent_id : char 上级知识分类ID
#       format : char 返回数据格式
#       show_all : 下一级还是全部
#   returnValue :
#        kc_id : 根据format进行定义list(list)或list(dict)
#   note:
#   mcf模式
#   examples:
kcq2 = rdlaiye.kc.query(show_all=True)
print(kcq2)
#3.8删除知识分类
print('3.8删除知识分类')
print('3.8.1删除知识分类mf:rdlaiye.kc_delete')
#   moduleName : rdlaiye
#   functionName : kc_delete删除知识分类
#   prototype: kc_delete(kc_name, parent_id='0'):
#   argList : 参数列表
#       kc_name : char 当前知识分类
#       parent_id ： char 父项
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
#
# kcd1 = rdlaiye.kc_delete('RDS')
# print(kcd1)
print('3.8.2删除知识分类mf:rdlaiye.kc.delete')
#   moduleName : rdlaiye
#   functionName : kc.delete删除知识分类
#   prototype: kc.delete(kc_name, parent_id='0'):
#   argList : 参数列表
#       kc_name : char 当前知识分类
#       parent_id ： char 父项
#   returnValue :
#        tbu
#   note:
#   mcf模式
#   examples:
# kcd2 = rdlaiye.kc.delete('RDP')
# print(kcd2)
#3.9更新知识分类
print('3.9更新知识分类')
print('3.9.1更新知识分类mf:rdlaiye.kc_update')
#   moduleName : rdlaiye
#   functionName : kc_update更新知识分类
#   prototype: kc_update(old_kc_name,new_kc_name):
#   argList : 参数列表
#       old_kc_name : 原有知识分类名称
#       new_kc_name ： 新的知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
print('3.9.2更新知识分类mf:rdlaiye.kc.update')
#   moduleName : rdlaiye
#   functionName : kc.update更新知识分类
#   prototype: kc.update(old_kc_name,new_kc_name):
#   argList : 参数列表
#       old_kc_name : 原有知识分类名称
#       new_kc_name ： 新的知识分类名称
#   returnValue :
#        tbu
#   note:
#   mcf模式
#   examples:
# rdlaiye.kc.update('RD','RDS')
print('4.知识点，也称为标准问,knowledgeNode，简称kn')
#   4.1创建知识点
print('4.1.1mf模式kn_create')
#   moduleName : rdlaiye
#   functionName : kn_create 创建知识点
#   prototype: kn_create(txt, kc_name):
#   argList : 参数列表
#       txt : 知识点内容
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
# knc1 = rdlaiye.kn_create('test1','RDS')
# print(knc1)
print('4.1.2mcf模式kn.create')
#   moduleName : rdlaiye
#   functionName : kn.create 创建知识点
#   prototype: kn.create(txt, kc_name):
#   argList : 参数列表
#       txt : 知识点内容
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mcf模式
#   如果重复创建知识点，系统会报错，后续完善相应的功能
#   examples:
# knc2 = rdlaiye.kn_create('test1','RDS')
# print(knc2)
#   4.2查询某个知识分类下面所有知识点
print('4.2.1mf模式kn_query')
#   moduleName : rdlaiye
#   functionName : kn_query 创建知识点
#   prototype: kn_query(kc_name):
#   argList : 参数列表
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
knq1 =  rdlaiye.kn_query('RDS')
print(knq1)

print('4.2.2mcf模式kn.query')
#   moduleName : rdlaiye
#   functionName : kn.query 查询知识点
#   prototype: kn.query(kc_name):
#   argList : 参数列表
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mcf模式
#   examples:
knq2 =  rdlaiye.kn.query('RDS','json')
print(knq2)
#   4.3根据知识分类及知识点名称获取ID
print('4.3.1mf模式kn_id')
#   moduleName : rdlaiye
#   functionName : kn_id 查询知识点ID
#   prototype: kn_id(kn_name, kc_name):
#   argList : 参数列表
#       kn_name 知识点名称
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
knid1 = rdlaiye.kn_id('test1','RDS')
print(knid1)

print('4.3.2mcf模式kn.id')
#   moduleName : rdlaiye
#   functionName : kn.id 查询知识点ID
#   prototype: kn.id(kn_name, kc_name):
#   argList : 参数列表
#       kn_name 知识点名称
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
knid2 = rdlaiye.kn.id('test1','RDS')
print(knid2)
#   4.4根据知识分类及知识点ID获取名称
print('4.4.1mf模式kn_name')
#   moduleName : rdlaiye
#   functionName : kn.id 查询知识点ID
#   prototype: kn_name(kn_id, kc_name):
#   argList : 参数列表
#       kn_id 知识点ID
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
knn1 = rdlaiye.kn_name('2876266','RDS')
print(knn1)
print('4.4.2mcf模式kn.name')
#   moduleName : rdlaiye
#   functionName : kn.name 查询知识点名称
#   prototype: kn_name(kn_id, kc_name):
#   argList : 参数列表
#       kn_id 知识点ID
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
knn2 = rdlaiye.kn.name('2876266','RDS')
print(knn2)
#   4.5知识点删除-tbu
#       4.5.1mf模式kn_delete()
#       4.5.2mcf模式kn.delete()
#   4.6知识点更新-tbu
#       4.6.1mf模式kn_update()
#       4.6.2mcf模式kn.update()
#5.知识叶，也称为相似问,knowledgeLeaf，简称kl
# 在知识库应用时kl也作为kn进行处理
#   5.1创建知识引导
print('5.1.1mf模式kl_create')
#   moduleName : rdlaiye
#   functionName : kn.name 查询知识点名称
#   prototype: kl_create(txt, kn_name, kc_name):
#   argList : 参数列表
#       kn_id 知识点ID
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
#   examples:
# klc1 = rdlaiye.kl_create('abc','test41','RDS')
# print(klc1)

print('5.1.2mcf模式kl.create')
#   moduleName : rdlaiye
#   functionName : kl.create 创建知识叶
#   prototype: kl.create(txt, kn_name, kc_name):
#   argList : 参数列表
#       kn_id 知识点ID
#       kc_name ： 归属知识分类名称
#   returnValue :
#        tbu
#   note:
#   mf模式
# klc2 = rdlaiye.kl.create('abc2','test41','RDS')
# print(klc2)
#   5.2查询某个知识分类某个知识点下面所有知识引导
print('5.2.1mf模式kl_query')
klq1 = rdlaiye.kl_query('test41','RDS')
print(klq1)
print('5.2.2mcf模式kl.query')
klq1 = rdlaiye.kl.query('test41','RDS','json')
print(klq1)
print('klq2')
#   5.3根据知识分类及知识点名称获取ID
print('5.3.1mf模式kl_id')
klid1 = rdlaiye.kl_id('abc2','test41','RDS')
print(klid1)
print('5.3.2mcf模式kl.id')
klid2 = rdlaiye.kl.id('abc2','test41','RDS')
print(klid2)

#   5.4根据知识分类及知识点ID获取名称
#       5.4.1mf模式kl_name()
print('5.4.2mcf模式kl.name')
kln1 = rdlaiye.kl.name('25720027','test41','RDS')
print(kln1)
#6.知识核,也称为标准答案,knowledgeKernel,kk
#   6.1创建标准答案
print('6.1.1mf模式kk_create')
# def kk_create(txt, kn_name, kc_name):
# kkc1 = rdlaiye.kk_create('bbc','test41','RDS')
# print(kkc1)
#       6.1.2mcf模式kk.create()
# kkc2 = rdlaiye.kk.create('天王盖','test41','RDS')
# print(kkc2)
#   6.2删除标准答案
#       6.2.1mf模式kk_delete()
#       6.2.2mcf模式kk.delete()
# rdlaiye.kk.delete('5029752')
#   6.3查询标准答案
#       6.3.1mf模式kk_query()
#       6.3.2mcf模式kk.query()
kkq2 = rdlaiye.kk.query('test41','RDS')
print(kkq2)
kkq3 = rdlaiye.kk.query('test41','RDS','json')
print(kkq3)
