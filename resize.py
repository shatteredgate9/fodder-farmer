import cv2 as cv

tera_small = cv.imread('pic/tera.png', 0)
tera_big = cv.imread('pic/tera_big.png', 0)

print(tera_small.shape)
print(tera_big.shape)

cv.imshow('tera_small', tera_small)
cv.imshow('tera_big', tera_big)

cv.waitKey(0)

tera_resized = cv.resize(tera_big, (tera_small.shape[1], tera_small.shape[0]), interpolation = cv.INTER_AREA) 
print(tera_resized.shape)

cv.imshow('tera_big_resized', tera_resized)

cv.waitKey(0)

