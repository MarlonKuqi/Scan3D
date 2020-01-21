import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { ObserverModule } from './observer/observer.module';
import { PhotoController } from './controllers/photo/photo.controller';
import { ObserverGateway } from './observer/observer.gateway';

@Module({
  imports: [ObserverModule],
  controllers: [AppController, PhotoController],
  providers: [AppService, ObserverGateway],
})
export class AppModule {}
