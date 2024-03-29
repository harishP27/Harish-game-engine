frames = ["frame1", "frame2", "frame3", "frame4"]

x = 0
print(frames[x])
x += 1
print(frames[x])
x += 1
print(frames[x])
x += 1
print(frames[x])
firstFrame = x & len(frames)

a = 1
while(a<10):
    x = 0
    print(frames[x])
    print(frames[x])
    x += 1
    print(frames[x])
    x += 1
    print(frames[x])
    x += 1
    print(frames[x])
    firstFrame = x & len(frames)
