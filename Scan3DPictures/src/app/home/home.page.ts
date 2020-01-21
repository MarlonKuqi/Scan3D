import { Component, OnInit } from '@angular/core';
import { Platform, ModalController, ToastController } from '@ionic/angular';
import { Router } from '@angular/router';
import { PreviewPage } from '../preview/preview.page';
import { ObserverService } from '../services/observer.service';
import { Picture } from '../models/picture.model';
import { CameraService } from '../services/camera.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  // tslint:disable-next-line: max-line-length
  pictures: Picture[] = [];
  constructor(private router: Router, private cameraService: CameraService,
              private modalCtrl: ModalController, private toastController: ToastController,
              private observerService: ObserverService) {}

  ngOnInit() {
    this.observerService.load();

    this.cameraService.picturesSubject.subscribe((data) => {
      this.pictures = data;
    });
    this.cameraService.emitPictures();
  }

  camera() {
    this.router.navigate(['camera']);
  }

  onClickSettings() {
    this.router.navigate(['settings']);
  }
  async onClickPhoto(i: number) {
    console.log('photo clicked');
    const modal = await this.modalCtrl.create({
      component: PreviewPage,
      componentProps: {
        picture: this.pictures[i],
      }
    });
    return await modal.present();
  }
  onDeletePhoto(indice: number) {
    let pictures = this.pictures.slice(0, indice);
    if (indice < this.pictures.length) {
      pictures = pictures.concat(this.pictures.slice(indice + 1));
    }
    this.pictures = pictures.slice();
    // this.presentToast('Nombre d\'images restantes: ' + this.pictures.length, 3000);
  }
  async presentToast(text: string, time: number) {
    const toast = await this.toastController.create({
      message: text,
      duration: time
    });
    toast.present();
  }
}
