from PIL import Image


def calculate(image1, image2):
    g = image1.histogram()
    s = image2.histogram()
    assert len(g) == len(s), "error"

    data = []

    for index in range(0, len(g)):
        if g[index] != s[index]:
            data.append(1 - abs(g[index] - s[index]) / max(g[index], s[index]))
        else:
            data.append(1)

    return sum(data) / len(g)


def split_image(image, part_size):
    pw, ph = part_size
    w, h = image.size

    sub_image_list = []

    assert w % pw == h % ph == 0, "error"

    for i in range(0, w, pw):
        for j in range(0, h, ph):
            sub_image = image.crop((i, j, i + pw, j + ph)).copy()
            sub_image_list.append(sub_image)

    return sub_image_list


def classfiy_histogram_with_split(image1, image2, size=(256, 256), part_size=(64, 64)):
    '''
     'image1' 和 'image2' 都是Image 对象.
     可以通过'Image.open(path)'进行创建。
     'size' 重新将 image 对象的尺寸进行重置，默认大小为256 * 256 .
     'part_size' 定义了分割图片的大小.默认大小为64*64 .
     返回值是 'image1' 和 'image2'对比后的相似度，相似度越高，图片越接近，达到100.0说明图片完全相同。
    '''
    image1.show()
    image2.show()
    img1 = image1.resize(size).convert("RGB")
    sub_image1 = split_image(img1, part_size)

    img2 = image2.resize(size).convert("RGB")
    sub_image2 = split_image(img2, part_size)

    sub_data = 0
    for im1, im2 in zip(sub_image1, sub_image2):
        sub_data += calculate(im1, im2)

    x = size[0] / part_size[0]
    y = size[1] / part_size[1]

    pre = round((sub_data / (x * y)), 6)
    print(pre * 100)
    return pre * 100


if __name__ == '__main__':
    im1 = Image.open('../test/1555986144.966379_0.png')
    im2 = Image.open('../test/1555986144.952497_0.png')
    classfiy_histogram_with_split(im1, im2)
