import os
import time
import secrets
from flask import render_template, url_for, flash, redirect, request, abort

from app import app
from app.forms import VideoUploadForm

from api.tritonAPI import Triton

triton = Triton(DEBUG = True)

def save_video(form_video):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(app.root_path, 'static/videos', video_fn)

    form_video.save(video_path)
    return video_fn, random_hex, video_path

@app.route('/', methods=["GET", "POST"])
@app.route('/home', methods=["GET", "POST"])
def home():

    form = VideoUploadForm()

    if form.validate_on_submit():
        return redirect(url_for('result'), code=307)
        #return redirect(url_for('result', result=result))#, result=result)

    return render_template('home.html', title="딥페이크 판별기", form=form)

@app.route('/result', methods=["GET", "POST"])
def result():
    form = VideoUploadForm()
    if form.validate_on_submit():
        video_file, random_hex, video_path = save_video(form.video_content.data)

        faces = triton.getFaces(video_path)
        triton.run(faces)

        Result_DeepFake, results, CAMList = triton.getResults()

        # Must Be Changed
        print("Ensembled DeepFake Probability {:.2f} %".format(results * 100))

        imgs = []
        video_name = ''
        if Result_DeepFake:
            video_name = f'{random_hex}.mp4'
            triton.makeCAM(video_file, CAMList)

            for i in CAMList:
                imgs.append(f"cam_{i}.png")

        result = {
            'deepfake': Result_DeepFake,
            'imgs': imgs,
            'percent': results,
            'id': video_name
        }
        deepfake = result['deepfake']
        images   = result['imgs']
        percent  = result['percent']
        video    = result['id']
        if deepfake:
            flash('이 영상은 딥페이크 영상입니다.', 'danger')
            flash('딥페이크 영상일 확률 {:.2f} % !!!'.format(percent * 100), 'danger')
        else:
            flash('이 영상은 딥페이크 영상이 아닙니다.', 'success')

    return render_template('result.html', title="딥페이크 검출 결과", images=images, id=video, deepfake=deepfake)

