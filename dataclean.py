#coding=utf-8
#（1）数据预处理
import os
import random
from io import open
conv_path = r'dgk_shooter_z.conv.txt'
#判断数据集是否存在？
if not os.path.exists(conv_path):
    print('数据集不存在')
    exit()
 
# 数据集格式
"""

"""
 
# 我首先使用文本编辑器sublime把dgk_shooter_min.conv文件编码转为UTF-8，一下子省了不少麻烦
convs = []  # 对话集合
with open(conv_path, encoding="utf8") as f:
    one_conv = []  # 一次完整对话
    for line in f:
        line = line.strip('\n').replace('/', '')#将分隔符去掉
        if line == '':
           continue
        if line[0] == 'E':
           if one_conv:
              convs.append(one_conv)
           one_conv = []
        elif line[0] == 'M':
           one_conv.append(line.split(' ')[1])
#将对话转成utf-8格式，并将其保存在dgk_shooter_min.conv文件中
 

print(convs[:3]) 

 
# 把对话分成问与答
ask = []        # 问
response = []   # 答
for conv in convs:
  if len(conv) == 1:
     continue
  if len(conv) % 2 != 0:  # 奇数对话数, 转为偶数对话
     conv = conv[:-1]
  for i in range(len(conv)):
     if i % 2 == 0:
        ask.append(conv[i])#偶数对，填写问题
     else:
        response.append(conv[i])#回答
 

print(len(ask), len(response))
print(ask[:3])
print(response[:3])
#['畹华吾侄', '咱们梅家从你爷爷起', '侍奉宫廷侍奉百姓']
#['你接到这封信的时候', '就一直小心翼翼地唱戏', '从来不曾遭此大祸']

 
 
def convert_seq2seq_files(questions, answers, TESTSET_SIZE=8000):
    # 创建文件
    train_enc = open('train.enc', 'w',encoding='utf-8')  # 问
    train_dec = open('train.dec', 'w',encoding='utf-8')  # 答
    test_enc = open('test.enc', 'w',encoding='utf-8')  # 问
    test_dec = open('test.dec', 'w',encoding='utf-8')  # 答
 
    # 选择8000数据作为测试数据
    test_index = random.sample([i for i in range(len(questions))], TESTSET_SIZE)
 
    for i in range(len(questions)):
        if i in test_index:#创建测试文件
            test_enc.write(questions[i] + '\n')
            test_dec.write(answers[i] + '\n')
        else:#创建训练文件
            train_enc.write(questions[i] + '\n')
            train_dec.write(answers[i] + '\n')
        if i % 1000 == 0:#表示处理了多少个i
            print(len(range(len(questions))), '处理进度:', i)
 
    train_enc.close()
    train_dec.close()
    test_enc.close()
    test_dec.close()
 
 
convert_seq2seq_files(ask, response)
# 生成的*.enc文件保存了问题
# 生成的*.dec文件保存了回答