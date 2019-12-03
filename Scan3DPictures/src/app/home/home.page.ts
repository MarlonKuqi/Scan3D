import { Component } from '@angular/core';
import { CameraPreview, CameraPreviewOptions, CameraPreviewDimensions } from '@ionic-native/camera-preview';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {
  options = {
    x: 0,
    y: 0,
    width: window.screen.width,
    height: window.screen.height,
    camera: CameraPreview.CAMERA_DIRECTION.BACK,
    toBack: false,
    tapPhoto: true,
    tapFocus: false,
    previewDrag: false,
    storeToFile: false,
    disableExifHeaderStripping: false
  };
  pictures: string[] = [];
  constructor() {}
  camera() {
    //CameraPreview
  }

}
