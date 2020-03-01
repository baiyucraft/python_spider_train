import requests
#定义方法
def youdao(t):
    #请求链接
    request_url="http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    #创建Form Data字典
    form_data = {
        'form':'AUTO',
        'to':'AUTO',
        'smartresult':'dict',
        'client':'fanyideskweb',
        'salt':'15830473769959',
        'sign':'6ba81754327f3ae503e0d0568b9d2923',
        'ts':'1583047376995',
        'bv':'35242348db4225f3512aa00c2f3e7826',
        'doctype':'json',
        'version':'2.1',
        'keyfrom':'fanyi.web',
        'action':'FY_BY_REALTlME'
    }
    #规定要翻译的内容
    form_data['i'] = t
    #post请求返回结果
    result = requests.post(request_url,form_data).json()
    #找出翻译结果
    translate_result = result['translateResult'][0][0]['tgt']
    #打印结果
    print('翻译的结果是： '+translate_result)
if __name__ == '__main__':
    t = input('请输入要翻译的内容：')
    youdao(t)