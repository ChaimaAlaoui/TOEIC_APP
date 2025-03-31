import cv2
img_path = "C:/Users/admin/Downloads/fiche"
def Read_image(img_path):
    img = cv2.imread(img_path)
    if img is None:
        print("error while charging the image")
        return None
    else:
        cv2.imshow("Feuille de Reponse", img)
