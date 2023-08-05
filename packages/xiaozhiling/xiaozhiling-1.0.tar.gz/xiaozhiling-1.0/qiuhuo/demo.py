#验证传入的字符串或者是数字是否是回文串
#函数返回值：
      # True：传入的值是回文串（数）
      # False：传入的不是回文串（数）
def checkcheckPalindrome(v):
    if not isinstance(v,int) and not isinstance(v,str):
        raise TypeError("参数值只能是整数或者是是字符串")
    v1=str(v)
    return  v1==v1[::-1]
if __name__ == "__main__":
    print(checkcheckPalindrome(121))
    print(checkcheckPalindrome("121"))

