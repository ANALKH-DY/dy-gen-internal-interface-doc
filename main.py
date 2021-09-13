import re
from typing import Pattern
import json

def parseMethodName(strContext):
  '''
  解析方法名和参数，返回列表
  '''
  pattern = re.compile(r"def\s+(\w+)\((?:\s*(?:\w*)\s*(?:\:\s*(?:\w+)\s*)?(?:\s*=\s*(?:'\w+'|\d+)?)?,?)*\)")

  m = pattern.match(strContext)

  print(m.groups())

  strMethodName = ''

  if m.group(0) is not None:
    strMethodName = m.group(1)

  return strMethodName

def parseMethodIntroduction(strContext):
  introduction = ''
  pattern = re.compile(r'"""(.+)')
  lstIntroduction = pattern.match(strContext)
  introduction = lstIntroduction.group(1)
  return introduction

def parseMethodArgs(strContext):
  '''
  解析参数 返回列表
  '''

  lstArgs = []

  pattern = re.compile(r'Args[\s|\S]*?Returns:')
  strX = pattern.findall(strContext)[0]
  lstX = strX.split('\n')

  lstX = lstX[1:-2]

  for index,strArgs in enumerate(lstX):
    strArgs = strArgs.strip()
    lstX[index] = strArgs

  pattern = re.compile(r"(\w+)\s\((\w+),?\s*(optional)?\):\s([\u4e00-\u9fa5|A-Za-z0-9|,|，]+).?\s*(Defaults to '?([0-9A-Za-z]+)'?)?")
  
  for strX in lstX:
    # strX : nPage (int, optional): 要返回的页码. Defaults to ''.
    m = pattern.match(strX)
    print(m.groups())
    dictArgs = {
      "name":m.group(1),
      "type":m.group(2),
      "explain": m.group(4),
    }
    if m.group(6) is not None:
      dictArgs['default'] = m.group(6)
    lstArgs.append(dictArgs)

  print(lstArgs)
  return lstArgs

def parseMethodReturn(strContext):
  '''
  解析返回值
  '''
  pattern = re.compile(r'Returns:[\s|\S]*?"""')

  strX = pattern.findall(strContext)[0]

  lstX = strX.split('\n')

  lstX = lstX[1:-1]

  if len(lstX) == 0:
    return None

  # lstX[N]格式： XXXX (XXXX): XXXX  
  for index,strProp in enumerate(lstX):
    lstX[index] = strProp.strip()

  pattern = re.compile(r'(\w+)\s\((\w+)\):\s*([\u4e00-\u9fa5|a-zA-Z0-9,|，]*)')

  lstReturnProp = []

  for strProp in lstX:
    m = pattern.match(strProp)
    print(m.groups())
    dictReturnProp = {
      "name":m.group(1),
      "type":m.group(2),
      "explain":m.group(3),
    }
    lstReturnProp.append(dictReturnProp)

  return lstReturnProp





  


def parseCommet(strContext):
  '''解析谷歌注释'''
  pattern = re.compile(r'"""[\s\S]*?"""')
  lstComment = pattern.findall(strContext)
  # print(lstComment)
  return lstComment

def parseMethods(strContext):
  # 匹配 nPage : int = 9,
  # strParamReg = r'''(\s*(\w*)\s*(\:\s*(\w+)\s*)?(\s*=\s*('\w+'|\d+)?)?,?)*'''
  # strReg = rf'''\s*def\s+([a-zA-Z\_][0-9a-zA-Z\_]*)\({strParamReg}\)\:$'''
  strReg = r'''def[\s|\S]*?"""[\s|\S]*?"""'''
  # strReg = r'^def\s[a-zA-Z\_][0-9a-zA-Z\_]*\(\w*(\s+\:\w+)\):$'

  r = re.compile(strReg)

  lstM = r.findall(strContext)

  lstMethod = []

  for strMethod in lstM:
    if strMethod.find('def __init__') == -1 and strMethod.find('def ToDictGet') == -1:
      lstMethod.append(strMethod)

  return lstMethod

''' 打开py文件'''
def parseLstStrMethod():
  with open('./Entityai_target.py', 'r',encoding="utf8") as f:
      # print(f.read())
      strFileContent = f.read()
      # parseMethods1(strFileContent)
      lstStrMethod = parseMethods(strFileContent)

  return lstStrMethod
      
    # parseMethods('''def openText(strText : str = '23' , nPage : int = 8):''')

def parseLstDictMethod(lstStrMethod : list) -> list:
  '''
  根据strMethod 解析出dictMethod
  '''
  lstDictMethod = []

  for strMethod in lstStrMethod:
        # 解析方法名
        strMethodName = parseMethodName(strMethod)
        # 解析谷歌评论
        lstComment = parseCommet(strMethod)
        for comment in lstComment:
          strIntroduction =  parseMethodIntroduction(comment)
          if comment.find('Args:') != -1:
            lstArgs = parseMethodArgs(comment)
          if comment.find('Returns:') != -1:
            lstReturns = parseMethodReturn(comment)

        dictMethod = {
          "name": strMethodName,
          "intro": strIntroduction,
          "args": lstArgs,
          "returns": lstReturns
        }
        lstDictMethod.append(dictMethod)

  return lstDictMethod

def writeToJSONFile(lstDictMethod: list):
  with open('./output.json','w',encoding='utf8') as f:
    f.write(json.dumps(lstDictMethod,ensure_ascii=False))
    print('输出JSON成功')

if __name__ == '__main__':
  lstStrMethod = parseLstStrMethod()
  lstDictMethod = parseLstDictMethod(lstStrMethod)

  writeToJSONFile(lstDictMethod)