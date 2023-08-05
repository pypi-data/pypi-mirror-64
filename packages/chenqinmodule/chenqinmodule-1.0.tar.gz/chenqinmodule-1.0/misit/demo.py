'''
验证传入的一个字符串或数字是否是回文串
True:是回文串
Fales :不是回文串
'''
def checkPalindrome(v):
    if not isinstance(v,int) and not isinstance(v,str):
        raise TypeError("参数只能是整数或者字符串")
    v1 = str(v)
    return v1 == v1[::-1]

if __name__ == "__main__":
    print(checkPalindrome(121))
    print(checkPalindrome("121"))
    print(checkPalindrome("125"))



