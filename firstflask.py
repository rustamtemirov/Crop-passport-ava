from flask import Flask, request
import requests
import cv2



app = Flask(__name__)





@app.route('/crop-avatar', methods=['POST'])
def crop_avatar():

    if request.headers['Service-Token'] == "service_token_ava":


        response = requests.get(request.form['passport_url']) # Скачивание фото пасспорта из URL
        file = open("image"+ request.form['user_id'] +".png", "wb") # Cохранение в файле image.png
        file.write(response.content)
        file.close()


        #Вырезание лица из фото

        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml') #
        img = cv2.imread("image"+  request.form['user_id'] +".png")

        while True:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            faces = face_cascade.detectMultiScale(gray, 1.1, 5)

            for (x, y, w, h) in faces:
                padding = 40
                crop_face = img[y - padding: y + h + padding, x - padding: x + w + padding]
                cv2.imwrite('upload'+ request.form['user_id'] + '.jpg', crop_face)

            if cv2.error:
                break

        cv2.destroyAllWindows()


        #Пост на данный урл с указанным id юзера
        url= 'https://services.test.aliftech.uz/api/gate/users/' + request.form["user_id"] + '/upload-avatar'
        headers = {'Service-Token': 'service-token-merchant'}
        files = {'image': open('upload'+ request.form['user_id'] + '.jpg', 'rb')}
        requests.post(url, headers=headers, files=files)


        return request.form




if __name__ == '__main__':
    app.run(host='localhost',port=8080, debug=True)