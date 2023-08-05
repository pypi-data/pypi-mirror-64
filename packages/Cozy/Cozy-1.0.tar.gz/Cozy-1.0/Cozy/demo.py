"""
验证传入的字符串或一个数是否是回文串
函数返回值：
        True:传入的值是回文串
        False：传入的值不是回文串
"""
def checkPalindrome(v):
    if not isinstance(v,int) and not isinstance(v,str):
        raise  TypeError("传入的参数只能是整数或字符串")
    v1 = str(v)
    return v1 == v1[::-1]
#测试函数的功能
if __name__  == "__main__":
    print(checkPalindrome(121))
