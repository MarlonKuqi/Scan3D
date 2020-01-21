import { Controller, Get } from '@nestjs/common';
import { ObserverGateway } from 'src/observer/observer.gateway';

@Controller('api/camera')
export class PhotoController {
    constructor(private readonly observer: ObserverGateway) {}
    @Get('launch')
    launch() {
        return this.observer.launchCamera();
    }

    @Get('capture')
    capture() {
        return this.observer.takePicture();
    }
}
