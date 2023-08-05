'''
验证传入的字符串或一个数字是否是回文串
函数的返回值：
    True：传入的值是回文串（数）
    False：传入的值不是回文串
'''
def checkPalindrome(v):
    #判断参数的类型
    if not isinstance(v,int) and not isinstance(v,str):
        raise  TypeError("参数值只能是整数或者字符串")

    v1=str(v)
    return v1==v1[::-1]
#测试函数的功能
if __name__=="__main__":
    print(checkPalindrome(121))
    print(checkPalindrome("123"))
    print(checkPalindrome("123.321"))
