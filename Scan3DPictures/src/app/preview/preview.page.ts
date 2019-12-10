import { Component, OnInit, Input } from '@angular/core';
import { ModalController } from '@ionic/angular';

@Component({
  selector: 'app-preview',
  templateUrl: './preview.page.html',
  styleUrls: ['./preview.page.scss'],
})
export class PreviewPage implements OnInit {
  @Input() picture: {sent: boolean, base64: string};
  constructor(private modalCtrl: ModalController) { }

  ngOnInit() {
  }
  onCancel() {
    this.modalCtrl.dismiss();
  }

}
