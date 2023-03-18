import cv2
import numpy as np
from pathlib import Path

label_str2int = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    'flag': 7,
    'inside': 8,
    'border': 9,
    'nobody': 10,
   	'other': 11,
    'noise': 99
}
label_int2str = {v:k for k, v in label_str2int.items()}


def process_img(img):
	return cv2.resize(img, (32, 32)).reshape(-1)


def make_model(dir: Path):
	train_x = []
	train_y = []
	for cls in dir.iterdir():
		if not cls.is_dir():
			continue
		for img_name in cls.glob('*.png'):
			img = cv2.imread(str(img_name))
			train_x.append(process_img(img))
			train_y.append(label_str2int[cls.name])

	train_x = np.array(train_x, dtype=np.float32)
	train_y = np.array(train_y, dtype=np.float32)
	train_y = np.expand_dims(train_y, axis=1)
	# print(train_x.shape)
	# print(train_y.shape)

	knn = cv2.ml.KNearest_create()
	knn.train(train_x, cv2.ml.ROW_SAMPLE, train_y)
	return knn


def run_model(knn, img):
	pimg = np.expand_dims(process_img(img), axis=0).astype(np.float32)
	ret, results, neighbours, dist = knn.findNearest(pimg, 1)
	# print(f"ret:        {ret}")
	# print(f"result:     {results}")
	# print(f"neighbours: {neighbours}")
	# print(f"distance:   {dist}")
	return ret


if __name__ == '__main__':
	model = make_model(Path('train'))
	x = run_model(model, cv2.imread('train/4/small-05-cut-183.png'))
	print(x)
