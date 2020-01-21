import { Injectable } from '@angular/core';
import { CameraPreview, CameraPreviewOptions, CameraPreviewDimensions } from '@ionic-native/camera-preview';
import { Picture } from '../models/picture.model';
import { Subject } from 'rxjs';
import { Platform } from '@ionic/angular';
import { ObserverService } from './observer.service';
import { Socket } from 'ngx-socket-io';


@Injectable({
  providedIn: 'root'
})
export class CameraService {
  pictures: Picture[] = [];
  flashNum = 0;
  flashIcons = ['flash_off-24px.svg', 'flash_on-24px.svg', 'flash_auto-24px.svg', 'highlight-24px.svg'];
  options = {
    x: 0,
    y: 50,
    width: window.screen.width,
    height: window.screen.availHeight - 230,
    camera: CameraPreview.CAMERA_DIRECTION.BACK,
    toBack: false,
    tapPhoto: false,
    tapFocus: true,
    previewDrag: false,
    storeToFile: false,
    disableExifHeaderStripping: false
  };
  picturesSubject: Subject<Picture[]> = new Subject<Picture[]>();
  constructor(private platform: Platform, private socket: Socket) { }
  launchCamera() {
    CameraPreview.startCamera(this.options).then(() => {
      CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.OFF);
      this.flashNum = 0;
    });
  }
  takePicture() {
    CameraPreview.takePicture({width: 1200, height: 1200, quality: 100}).then((imageData) => {
      const picture: Picture = {
        date: new Date().valueOf(),
        sent: false,
        base64: 'data:image/jpeg;base64,' + imageData
      };
      this.pictures.push(picture);
      this.sendPicture(picture);
      this.emitPictures();
    });
  }
  sendPicture(picture: Picture) {
    this.socket.emit('picture-took', picture);
  }
  stopCamera() {
    this.flashNum = 0;
    CameraPreview.stopCamera();
    CameraPreview.hide();
  }
  focusCamera() {
    CameraPreview.tapToFocus(this.platform.width() / 2, this.platform.height() / 2);
  }
  setFlashMode() {
    this.flashNum += 1;
    if (this.flashNum === this.flashIcons.length) {
      this.flashNum = 0;
    }
    switch (this.flashNum) {
      case 0:
        CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.OFF);
        break;
      case 1:
          CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.ON);
          break;
      case 2:
          CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.AUTO);
          break;
      case 3:
          CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.TORCH);
          break;
      default:
          this.flashNum = 0;
          CameraPreview.setFlashMode(CameraPreview.FLASH_MODE.OFF);
          break;
    }
  }
  switchCamera() {
    CameraPreview.switchCamera();
  }
  setPictureSent(date: number) {
    this.pictures.forEach((elt, i) => {
      if (elt.date === date) {
        this.pictures[i].sent = true;
        this.emitPictures();
      }
    });
  }
  emitPictures() {
    this.picturesSubject.next(this.pictures.slice());
  }
}
