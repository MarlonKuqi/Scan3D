import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Socket } from 'ngx-socket-io';
import { CameraService } from './camera.service';
import { Picture } from '../models/picture.model';

@Injectable({
  providedIn: 'root'
})
export class ObserverService {
  users: number;
  connected: boolean;
  takePicture = 0;

  usersSubject: Subject<number> = new Subject<number>();
  takePictureSubject: Subject<number> = new Subject<number>();
  connectedSubject: Subject<boolean> = new Subject<boolean>();

  constructor(private socket: Socket, private cameraService: CameraService) { }

  load() {
    this.receiveTakePicture().subscribe(() => {
      this.cameraService.takePicture();
    });
    this.receiveUsers().subscribe((data: number) => {
      this.users = data;
      console.log('users signal');
      this.emitUsers();
    });
    this.receiveLaunchCamera().subscribe(() => {
      this.cameraService.launchCamera();
    });
    this.receivePictureReceived().subscribe((date: number) => {
      this.cameraService.setPictureSent(date);
    });
    this.socket.connect();
    this.connected = true;
    this.emitConnected();
  }

  emitUsers() {
    this.usersSubject.next(this.users);
  }

  emitTakePicture() {
    this.takePictureSubject.next(this.takePicture);
  }

  emitConnected() {
    this.connectedSubject.next(this.connected);
  }

  connect() {
    this.socket.connect();
    this.connected = true;
    this.emitConnected();
  }

  disconnect() {
    this.socket.disconnect();
    this.connected = false;
    this.users -= 1;
    this.emitConnected();
  }

  receiveLaunchCamera() {
    return this.socket.fromEvent('launch-camera');
  }

  receiveTakePicture() {
    return this.socket.fromEvent('take-picture');
  }

  receivePictureReceived() {
    return this.socket.fromEvent('picture-received');
  }
  sendPicture(picture: Picture) {
    this.socket.emit('picture-took', picture);
  }

  receiveUsers() {
    return this.socket.fromEvent('users');
  }
}
