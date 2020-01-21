import { Component, OnInit } from '@angular/core';
import { CameraService } from '../services/camera.service';
import { Router } from '@angular/router';
import { Picture } from '../models/picture.model';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-camera',
  templateUrl: './camera.page.html',
  styleUrls: ['./camera.page.scss'],
})
export class CameraPage implements OnInit {

  constructor(private cameraService: CameraService, private router: Router) { }
  pictures: Picture[] = [];
  picturesSubscription: Subscription;
  ngOnInit() {
    this.cameraService.launchCamera();
    this.picturesSubscription = this.cameraService.picturesSubject.subscribe((data) => {
      this.pictures = data;
    });
    this.cameraService.emitPictures();
  }

  onBackMenuButton() {
    this.cameraService.stopCamera();
    this.router.navigate(['home']);
  }

  getFlashIcon() {
    return this.cameraService.flashIcons[this.cameraService.flashNum];
  }
  onTakePicture() {
    this.cameraService.takePicture();
  }
  onFocusCamera() {
    this.cameraService.focusCamera();
  }
  onSetFlashMode() {
    this.cameraService.setFlashMode();
  }
  onSwitchCamera() {
    this.cameraService.switchCamera();
  }
}
