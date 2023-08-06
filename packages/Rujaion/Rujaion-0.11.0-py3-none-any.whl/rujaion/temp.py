n = int(input())
ans = 1
coef = 1
for i in range(n):
    coef *= 5
    ans += coef
print(ans)
