from model import SpillDetector
import matplotlib.pyplot as plt

model = SpillDetector('src\spill_detector\model.pt')

img = plt.imread('test_images/00000_00105.jpg')


res = model.detect(img)

print(res)