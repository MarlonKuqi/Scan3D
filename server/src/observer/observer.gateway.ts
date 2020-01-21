import { WebSocketGateway, WebSocketServer, SubscribeMessage, OnGatewayConnection, OnGatewayDisconnect, MessageBody } from '@nestjs/websockets';
import { Picture } from 'src/models/picture.model';
import { Injectable } from '@nestjs/common';

@Injectable()
@WebSocketGateway()
export class ObserverGateway implements OnGatewayConnection, OnGatewayDisconnect {
    pictures: Picture[] = [];
    @WebSocketServer() server;
    users: number = 0;
    counter: number = 0;

    async handleConnection() {
        // A client has connected
        this.users++;
        console.log('new connection');

        // Notify connected clients of current users
        this.server.emit('users', this.users);
    }

    async handleDisconnect() {

        // A client has disconnected
        this.users--;
        console.log('new disconnection');
        // Notify connected clients of current users
        this.server.emit('users', this.users);
    }
    @SubscribeMessage('picture-took')
    async onPictureTook(@MessageBody() picture: Picture) {
        console.log('picture took', picture.date , picture.base64.slice(20));
        if (this.pictures.filter(elt => elt.date === picture.date).length === 0) {
            this.pictures.push(picture);
        }
        picture.exportToFile();
        this.server.send('picture-received', picture.date);
    }

    @SubscribeMessage('counter')
    async onCounter(client, nombre: number) {
        this.counter += nombre;
        client.broadcast.emit('counter', this.counter);
    }

    async takePicture(): Promise<any> {
        console.log('take picture');
        this.server.emit('take-picture');
        return 'commande exécutée: take-picture';
    }
    async launchCamera(): Promise<any> {
        console.log('launch camera');
        this.server.emit('launch-camera');
        return 'commande exécutée: launch-camera';
    }
}
