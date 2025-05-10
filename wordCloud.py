import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
import numpy as np
from PIL import Image
from utils.queryhive import queryhives

def get_img(targetImageSrc,resImageSrc):
    data = queryhives('select workTag from jobData',[],'select')
    #分词
    text = ''
    for i in data:
        if i[0] != '':
            tarArr = i
            for j in tarArr:
                try:
                    text += j
                except:
                    continue
    data_cut = jieba.cut(text,cut_all=False)
    string = ' '.join(data_cut)

    #词云图
    img = Image.open(targetImageSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        font_path='STHUPO.TTF',
        mask=img_arr,
        background_color='#fff'
    )
    wc.generate_from_text(string)

    #图片生成
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.savefig(resImageSrc,dpi=800,bbox_inches='tight',pad_inches=-0.1)

get_img('./static/static/cloudImg/tree.jpg','./static/static/tagCloud')