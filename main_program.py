import time
import pyautogui
import cv2 as cv
import numpy as np
import keyboard as kb
from PIL import Image
from matplotlib import pyplot as plt


def convert_opencv_to_pil(img):
	color_cvt = cv.cvtColor(img, cv.COLOR_BGR2RGB)
	pil_image = Image.fromarray(color_cvt)
	return pil_image


def h_stack_merge(images):
	w, h = zip(*(i.size for i in images))

	total_w = sum(w)
	total_h = max(h)

	new_img = Image.new('RGB', (total_w,total_h))

	x_offset = 0
	for im in images:
		new_img.paste(im.resize((im.size[0], max(h))), (x_offset, 0))
		x_offset += im.size[0]

	return new_img


def v_stack_merge(images):
	w, h = zip(*(i.size for i in images))

	total_w = max(w)
	total_h = sum(h)

	new_img = Image.new('RGB', (total_w,total_h))

	y_offset = 0
	for im in images:
		new_img.paste(im.resize((max(w), im.size[1])), (0, y_offset))
		y_offset += im.size[1]

	return new_img


def template_match_image(source, template):
	img_source = source
	img_template = cv.imread(template)

	weight, height, _ = img_template.shape
	src_gray = cv.cvtColor(img_source, cv.COLOR_BGR2GRAY)
	tmplt_gray = cv.cvtColor(img_template, cv.COLOR_BGR2GRAY)

	res = cv.matchTemplate(src_gray, tmplt_gray, cv.TM_CCOEFF_NORMED)
	_,_,_, maxLoc = cv.minMaxLoc(res)
	
	res = source[maxLoc[1]:maxLoc[1]+weight, maxLoc[0]:maxLoc[0]+height]

	return res


def take_screenshot():
	image = pyautogui.screenshot()
	res = cv.cvtColor(np.array(image), cv.COLOR_RGB2BGR)
	print('[OK] Screenshot taken')

	return res


def chara_body_image(source):
	img_source = source
	y, x, _ = img_source.shape
	start_y = y//2 - (y//2) + 70
	start_x = x//2 - (x//9)
	res = img_source[start_y:y, start_x:start_x+(x//5 + 30)]

	return res


template_list = [
					'image_template/stats_main.png',
					'image_template/weapon_main.png',
					'image_template/talent_main.png',
					'image_template/cons_main.png',
					'image_template/maxHP.png',
					'image_template/ATK.png',
					'image_template/DEF.png',
					'image_template/EM.png',
					'image_template/CRate.png',
					'image_template/CDmg.png',
					'image_template/ER.png',
					'image_template/artifact_main.png',
				]


print('Please follow this steps of taking the screenshot.\n')
print('1. Attributes')
print('2. Weapons')
print('3. Talents')
print('4. Cons')
print('5. CHaracter Details')
print('6. Artifacts. Start from Flower, ended with Circlet\n')
print('[!] Press "PrtSc/PrintScreen" to take screenshot.')
print('\nReady?')
input('Press Enter to continue...\n')
print('Start!')

bucket = []

for i in range(6):
	if i >= 0 and i < 4:
		# do
		if i == 0:
			print('[!] First, take screenshot of Character -> Weapon -> Talent -> then Cons')
			
			kb.wait('prtscn')
			img = take_screenshot()

			chara_body = chara_body_image(img)
			bucket.append(convert_opencv_to_pil(chara_body))

			img = template_match_image(img, template_list[i])
			bucket.append(convert_opencv_to_pil(img))

		else:
			kb.wait('prtscn')
			img = take_screenshot()

			img = template_match_image(img, template_list[i])
			bucket.append(convert_opencv_to_pil(img))

	elif i == 4:
		print('\n[!] After that, please take screenshot of character details.')
		print('[?] Its about character details of Max HP, ATK, DEF, EM, C.Rate, C.Dmg, and ER.')
		kb.wait('prtscn')
		img = take_screenshot()
		for j in range(7):
			img_stats = template_match_image(img, template_list[i+j])
			bucket.append(convert_opencv_to_pil(img_stats))

	elif i == 5:
		print('\n[!] For the last, take screenshot of artifacts.')
		print('Just make sure you start from Flower ended with Circlet. OK?')
		for i in range(5):
			# take artifact
			kb.wait('prtscn')
			img = take_screenshot()
			img = template_match_image(img, template_list[11])
			bucket.append(convert_opencv_to_pil(img))


# Merging images
start = time.time()
img_chara = h_stack_merge(bucket[1:4])
img_stats = v_stack_merge(bucket[5:12])
res = v_stack_merge([img_chara, img_stats])
res = h_stack_merge([bucket[0], bucket[4], res])

img_artif = h_stack_merge(bucket[12:17])
res = v_stack_merge([res, img_artif])

res.save('res.png')
end = time.time()
print("Time Elapsed (s):", end-start)

plt.imshow(res)
plt.show()

cv.destroyAllWindows()
print('\nFinish\nClosing program.')