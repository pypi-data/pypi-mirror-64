

def checkPalindrome(value):

    # 判断参数的类型
    if not isinstance(value, int) and not isinstance(value, str):
        raise TypeError("传入的参数只能是整形或者字符型")

    value2 = str(value)

    print("整形和字符串比较：", 121 == "121")

    return value == value2[::-1]

if __name__ == "__main__":
    print(checkPalindrome(131))
    print(checkPalindrome("131"))
    # print(checkPalindrome(131.131))
    print(checkPalindrome("131.131"))
