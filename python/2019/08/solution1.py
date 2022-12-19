

def main():
    file = open('input1.txt', 'r')
    content = file.read().strip()

    step = 25 * 6
    parts = [content[i:i+step] for i in range(0, len(content), step)]

    check = {}

    for layer in parts:
        z = layer.count('0')
        c = layer.count('1') * layer.count('2')
        check[z] = c

    print(f"The solution is: {check[min(check.keys())]}")
    
    image = []
    for i in range(len(parts[0])):
        for l in range(len(parts)):
            pixel = parts[l][i]
            if pixel != '2':
                if pixel == '0':
                    image.append(' ')
                else:
                    image.append('*')
                break

    print("The tailcode is:")
    for x in range(0, len(image), step):
        c = ''.join(image[x:x+step])
        for y in range(0, 25*6, 25):
            print(c[y:y+25])


if __name__ == "__main__":
    main()