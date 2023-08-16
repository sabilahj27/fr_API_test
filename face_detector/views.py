from turtle import title
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import cv2
import face_recognition as fr
from face_detector import grab as g
from face_detector import models as m

def index(request):
    context={
        'title' : title
    }
    return render(request, 'index_berhasil2.html', context)

@csrf_exempt
def detect(request):
    data = {"success": False, "faces": []}

    if request.method == "POST":
        if request.FILES.get("image", None) is not None:
            image = g._grab_image(stream=request.FILES["image"])
        else:
            url = request.POST.get("url", None)
            if url is None:
                data["error"] = "No URL provided."
                return JsonResponse(data)
            image = g._grab_image(url=url)

        small_image = cv2.resize(image, (0, 0), fx=0.25, fy=0.25)

        is_detected = m.face_locations(small_image)[0]

        if len(is_detected) == 0:
            data['success'] = False
        else:
            known_names = m.known_names()
            known_encodings = m.known_encodings()

            face_locations = m.face_locations(small_image)[0]
            face_encodings = m.encode_detected_face(small_image)[0]

            matches = m.compare_encoded_faces(
                known_encodings, face_encodings, known_names)[0]

            for (top, right, bottom, left) in face_locations:
                roi = image[top:bottom, left:right]
                image_grey = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY)

                emo_image = np.expand_dims(np.expand_dims(
                    cv2.resize(image_grey, (48, 48)), -1), 0)
                ageg_image = np.expand_dims(np.expand_dims(
                    cv2.resize(image_grey, (64, 64)), -1), 0)

                predict_emotion = m.model_emotion.predict(emo_image)
                predict_age = m.model_age.predict(ageg_image)

                # face_instance = m.FaceData(
                #     top=top,
                #     right=right,
                #     bottom=bottom,
                #     left=left,
                #     emotion=m.get_emotion(predict_emotion),
                #     age=m.get_age(predict_age[1]),
                #     gender=m.get_gender(predict_age[0]),
                # )
                # face_instance.save()

                data["faces"].append({"location": face_locations,
                                      "emotion": m.get_emotion(predict_emotion),
                                      "age": m.get_age(predict_age[0]),
                                      "gender": m.get_gender(predict_age[1]),
                                      "name": matches,
                                      })
            data["success"] = True

    return JsonResponse(data)
    # return render(request, 'index.html', data)
